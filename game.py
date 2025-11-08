from pygame import Rect
from pgzero.actor import Actor
import pgzrun

WIDTH = 960
HEIGHT = 640
TITLE = "ROGUELIKE MENU"
GAME = "menu"
VOLUME = 0.1

options = ["Start Game", "Music and Sounds: On", "Quit"]
volume_on = True

menu = Actor("menu", topleft=(0,0))
bg = Actor("map", topleft=(0,0))

bottons_menu = [
    Rect((329,250),(300,70)),
    Rect((200,370),(565,75)),
    Rect((410,490),(140,70))
]

hover_index = -1  # controla o botão sob o mouse

def play_music(VOLUME):
    music.set_volume(VOLUME)
    music.play("background_music")

play_music(VOLUME)

def draw():
    screen.clear()
    if GAME == "menu":
        draw_menu()
    else:
        bg.draw()

    # desenha os botões
    for i, bot in enumerate(bottons_menu):
        color = (255, 100, 100) if i == hover_index else (255, 0, 0)
        screen.draw.rect(bot, color)

def draw_menu():    
    menu.draw()
    screen.draw.text("Rog the Game",
                      color="brown", 
                      fontsize=80, 
                      center=(WIDTH/2,HEIGHT/4.5),
                      fontname="minecraft")
    
    for i, name in enumerate(options):
        x, y = WIDTH/2, 290 + i * 120
        screen.draw.text(name, center=(x,y),
                         color="black", fontsize=50,
                         fontname="minecraft")

def on_mouse_move(pos, rel, buttons):
    global hover_index
    hover_index = -1
    for i, rect in enumerate(bottons_menu):
        if rect.collidepoint(pos):
            hover_index = i
            break

def on_mouse_down(pos):
    global GAME, volume_on, options

    for i, rect in enumerate(bottons_menu):
        if rect.collidepoint(pos):
            if i == 0:
                print("Iniciar o jogo")
                GAME = "game"
            elif i == 1:
                volume_on = not volume_on
                if volume_on:
                    music.play("background_music")
                    options[1] = "Music and Sounds: On"
                else:
                    music.stop()
                    options[1] = "Music and Sounds: Off"
            elif i == 2:
                print("Sair do jogo")
                quit()

pgzrun.go()
