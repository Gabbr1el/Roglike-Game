# __________IMPORTS__________
from random import randint
from pygame import Rect
import pgzero
import pgzrun

#____________MUSIC____________
def play_music(VOLUME):
    music.set_volume(VOLUME)
    music.play("background_music")

#_________PLAY MUSIC____________
play_music(VOLUME=0.1)

#__________CONFIGURATION_________
WIDTH = 960
HEIGHT = 640
TITLE = "ROGUELIKE GAME"

#_______________MENU________________
GAME = "menu"
VOLUME = 0.1
options = ["Start Game", "Music and Sounds: On", "Quit"]
volume_on = True
projectiles = []
enemies = []

#_________MAP AND OBJECTS_________
menu = Actor("menu", topleft=(0, 0))
bg = Actor("map", topleft=(0, 0))

obstacles = [
    Rect((898, 324), (24, 44)),
    Rect((898, 228), (24, 44)),
    Rect((31, 198), (24, 44)),
    Rect((31, 387), (24, 44)),
    Rect((642, 546), (24, 44)),
    Rect((385, 546), (24, 44)),
    Rect((130, 125), (28, 10)),
    Rect((546, 96), (28, 8)),
    Rect((34, 100), (190, 7)),
    Rect((804, 95), (84, 14)),
    Rect((98, 550), (24, 54)),
    Rect((34, 105), (24, 34)),
    Rect((900, 480), (24, 34)),
    Rect((840, 516), (90, 90)),
]

bottons_menu = [
    Rect((329, 250), (300, 70)),
    Rect((200, 370), (565, 75)),
    Rect((410, 490), (140, 70))
]

#__________CREATE A PLAYER____________
class Player:
    def __init__(self,pos):
        self.frames = {
            'bottom': ["playerdown1", "playerdown2","playerdown3", "playerdown4"],
            'up':     ["playerup1", "playerup2", "playerup3", "playerup4"],
            'left':   ["playerleft1", "playerleft2", "playerleft3", "playerleft4"],
            'right':  ["playerright1", "playerright2", "playerright3", "playerright4"]
        }

        self.actor = Actor(self.frames['bottom'][0], center=pos)
        self.direction = 'bottom'
        self.velocity = 2
        self.anim_timer = 0
        self.anim_speed = 0.08
        self.invulnerable = False
        self.stop_speed = 0.04
        self.moving = False
        self.frame = 0
        self.hp = 3
        self.max_hp = 3
        self.damage = 1  # <<-- dano dos projéteis

    def draw(self):
        self.actor.draw()
        self.draw_hearts()

    def draw_hearts(self):
        x = 770
        y = 20
        screen.draw.filled_rect(Rect((x + 5, y + 5), (150, 50)), (0, 0, 0))
        pos_x = x
        for i in range(self.max_hp):
            img = "life2" if i < self.hp else "life1"
            heart = Actor(img, topleft=(pos_x, y))
            heart.draw()
            pos_x += 50

    def move(self):
        old_x, old_y = self.actor.x, self.actor.y
        self.moving = False
        if keyboard.a:
            self.actor.x -= self.velocity
            self.direction = "left"
            self.moving = True
        if keyboard.d:
            self.actor.x += self.velocity
            self.direction = "right"
            self.moving = True
        if keyboard.w:
            self.actor.y -= self.velocity
            self.direction = "up"
            self.moving = True
        if keyboard.s:
            self.actor.y += self.velocity
            self.direction = "bottom"
            self.moving = True

        for obs in obstacles:
            if self.actor.colliderect(obs):
                self.actor.x, self.actor.y = old_x, old_y
                break

        if self.actor.left < 34: self.actor.left = 34
        if self.actor.right > WIDTH - 34: self.actor.right = WIDTH - 34
        if self.actor.top < 85: self.actor.top = 85
        if self.actor.bottom > HEIGHT - 34: self.actor.bottom = HEIGHT - 34

    def take_damage(self, amount):
        if self.invulnerable:
            return
        self.hp -= amount
        self.invulnerable = True
        clock.schedule_unique(self.remove_invulnerability, 1.0)

    def remove_invulnerability(self):
        self.invulnerable = False

    def animate(self):
        if self.moving:
            self.anim_timer += self.anim_speed
        else:
            self.anim_timer += self.stop_speed
        if self.anim_timer >= 1:
            self.anim_timer = 0
            self.frame = (self.frame + 1) % len(self.frames[self.direction])
        self.actor.image = self.frames[self.direction][self.frame]

    def update(self):
        self.move()
        self.animate()


#__________CREATE ENEMY_____________
class Enemy:
    def __init__(self, hp=4):
        self.frames = {
            'stopped': ["enemy_stopped1", "enemy_stopped2", "enemy_stopped3"],
            'walk': ["enemy_walk1","enemy_walk2","enemy_walk3"]
        }

        self.actor = Actor(self.frames["stopped"][0], center=(randint(100, WIDTH-100), randint(100, HEIGHT-100)))
        self.velocity = 1
        self.anim_speed = 0.1
        self.anim_timer = 0
        self.frame = 0
        self.state = 'stopped'    
        self.max_hp = hp
        self.hp = hp

    def draw(self):
        self.actor.draw()

    def move(self):
        old_x, old_y = self.actor.x, self.actor.y
        dx = player.actor.x - self.actor.x
        dy = player.actor.y - self.actor.y
        dist = max(1, (dx**2 + dy**2)**0.5)
        self.actor.x += (dx/dist) * self.velocity
        self.actor.y += (dy/dist) * self.velocity

        if self.actor.colliderect(player.actor):
            self.actor.x, self.actor.y = old_x, old_y
            return
        for obs in obstacles:
            if self.actor.colliderect(obs):
                self.actor.x, self.actor.y = old_x, old_y
                break

    def update(self):
        self.move()
        self.animate()

    def animate(self):
        self.anim_timer += self.anim_speed
        if self.anim_timer >= 1:
            self.anim_timer = 0
            self.frame = (self.frame + 1) % len(self.frames[self.state])
        self.actor.image = self.frames[self.state][self.frame]


#__________PROJECTILE_____________
class Projectile:
    def __init__(self, start, target):
        self.frames = ["mage_0", "mage_1", "mage_2"]
        self.frame = 0
        self.anim_timer = 0
        self.anim_speed = 0.15

        self.actor = Actor(self.frames[0])
        self.actor.pos = start

        dx = target[0] - start[0]
        dy = target[1] - start[1]
        dist = max(1, (dx**2 + dy**2)**0.5)
        self.vx = dx / dist * 6
        self.vy = dy / dist * 6
        self.alive = True

    def update(self):
        self.actor.x += self.vx
        self.actor.y += self.vy
        self.anim_timer += self.anim_speed
        if self.anim_timer >= 1:
            self.anim_timer = 0
            self.frame = (self.frame + 1) % len(self.frames)
            self.actor.image = self.frames[self.frame]

        if (self.actor.x < -50 or self.actor.x > WIDTH + 50 or
            self.actor.y < -50 or self.actor.y > HEIGHT + 50):
            self.alive = False

    def draw(self):
        self.actor.draw()


#___________INFORMATIONS__________
player = Player((WIDTH/2, HEIGHT/2))
current_wave = 1
max_waves = 10
choosing_upgrade = False
upgrade_options = ["+1 Velocidade", "+1 Dano", "Recuperar 1 de Vida"]

#_______________WAVE_____________
def spawn_wave(wave):
    enemies.clear()
    hp_for_enemy = 4 + (wave - 1) // 3
    for i in range(wave + 1):
        enemies.append(Enemy(hp=hp_for_enemy))

spawn_wave(current_wave)

#__________GAME OVER SCREEN__________
def draw_game_over():
    screen.fill((0, 0, 0))
    screen.draw.text("GAME OVER", center=(WIDTH/2, HEIGHT/3), fontsize=90, color="red", fontname="minecraft")
    screen.draw.text("Clique para reiniciar", center=(WIDTH/2, HEIGHT/1.8), fontsize=40, color="white", fontname="minecraft")

#__________WIN SCREEN__________
def draw_win_screen():
    screen.fill((0, 0, 0))
    screen.draw.text("VOCE VENCEU!", center=(WIDTH/2, HEIGHT/3), fontsize=90, color="yellow", fontname="minecraft")
    screen.draw.text("Clique para voltar ao menu", center=(WIDTH/2, HEIGHT/1.8), fontsize=40, color="white", fontname="minecraft")

#___________DRAW______________
def draw():
    screen.clear()
    if GAME == "game":
        bg.draw()
        player.draw()
        for e in enemies:
            e.draw()
        for p in projectiles:
            p.draw()
        screen.draw.text(f"Wave: {current_wave}", (20, 20), color="white", fontsize=40)
        if choosing_upgrade:
            draw_upgrade_screen()
    elif GAME == "menu":
        draw_menu()
    elif GAME == "gameover":
        draw_game_over()
    elif GAME == "win":
        draw_win_screen()

def draw_menu():
    menu.draw()
    screen.draw.text("Rog the Game", color="brown", fontsize=80, center=(WIDTH/2, HEIGHT/4.5), fontname="minecraft")
    for i, name in enumerate(options):
        screen.draw.text(name, center=(WIDTH/2, 290 + i*120), color="black", fontsize=50, fontname="minecraft")

def draw_upgrade_screen():
    screen.draw.filled_rect(Rect((0, 0), (WIDTH, HEIGHT)), (0, 0, 0))
    screen.draw.text("Escolha um Upgrade", center=(WIDTH/2, HEIGHT/4), fontsize=70, color="yellow", fontname="minecraft")
    for i, up in enumerate(upgrade_options):
        screen.draw.text(up, center=(WIDTH/2, 300 + i*100), fontsize=50, color="white", fontname="minecraft")


#___________UPDATE______________
def update():
    global GAME, current_wave, choosing_upgrade

    if GAME != "game" or choosing_upgrade:
        return

    player.update()

    for e in enemies[:]:
        e.update()
        if e.actor.colliderect(player.actor):
            player.take_damage(1)
        if e.hp <= 0:
            enemies.remove(e)

    for p in projectiles[:]:
        p.update()
        if not p.alive:
            projectiles.remove(p)
            continue
        for e in enemies[:]:
            if p.actor.colliderect(e.actor):
                e.hp -= player.damage
                projectiles.remove(p)
                if e.hp <= 0:
                    enemies.remove(e)
                break

    # próxima wave
    if not enemies and current_wave < max_waves:
        choosing_upgrade = True

    if player.hp <= 0:
        GAME = "gameover"
        music.stop()
        sounds.game_over.play()

    if not enemies and current_wave == max_waves:
        GAME = "win"
        return


#__________CLICK MOUSE__________
def on_mouse_down(pos):
    global GAME, player, volume_on, current_wave, choosing_upgrade

    if GAME == "gameover":
        player = Player((WIDTH/2, HEIGHT/2))
        current_wave = 1
        spawn_wave(current_wave)
        GAME = "game"
        play_music(VOLUME=0.1)
        return
    if GAME == "win":
        GAME = "menu"
        player = Player((WIDTH/2, HEIGHT/2))
        current_wave = 1
        spawn_wave(current_wave)
        play_music(VOLUME=0.1)  
        return

    if choosing_upgrade:
        for i, up in enumerate(upgrade_options):
            area = Rect((WIDTH/2 - 200, 250 + i*100), (400, 80))
            if area.collidepoint(pos):
                if i == 0:
                    player.velocity += 1
                elif i == 1:
                    player.damage += 1
                elif i == 2:  # <<-- Recupera 1 de vida (sem aumentar o máximo)
                    if player.hp < player.max_hp:
                        player.hp += 1
                choosing_upgrade = False
                current_wave += 1
                spawn_wave(current_wave)
                break
        return

    if GAME == "game":
        projectiles.append(Projectile(player.actor.pos, pos))
        sounds.magic_missil.play()
        return


    for i, rect in enumerate(bottons_menu):
        if rect.collidepoint(pos):
            if i == 0:
                GAME = "game"
            elif i == 1:
                volume_on = not volume_on
                music.set_volume(0.1 if volume_on else 0)
                options[1] = "Music and Sounds: On" if volume_on else "Music and Sounds: Off"
            elif i == 2:
                exit()


pgzrun.go()