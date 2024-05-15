from socket import *
from threading import Thread
import pygame
import sys
import tkinter as tk
from tkinter import simpledialog

# Constants
HOST = "127.0.0.1"
PORT = 8000
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 50
ENEMY_SIZE = 50
BULLET_SIZE = 50
BULLET_SPEED = 20
PLAYER_SPEED = 10
BULLET_COUNT = 3

# Globals
state = []
messages = []
specific_enemy_pos = [100]
bullet_pos = [0, 0]
bullet_state = "ready"
bullet_count = BULLET_COUNT
enemy_list = [[114, 100], [228, 100], [342, 100], [456, 100], [570, 100], [684, 100]]

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Fonts
pygame.font.init()
font = pygame.font.SysFont("monospace", 35)

# Pygame Initialization
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Star War')

# Load Assets
player_image = pygame.transform.scale(pygame.image.load('images/plane/p.png'), (PLAYER_SIZE, PLAYER_SIZE)).convert_alpha()
laser_bullet = pygame.transform.scale(pygame.image.load('images/bullet.png'), (BULLET_SIZE, BULLET_SIZE)).convert_alpha()
planets = [pygame.transform.scale(pygame.image.load(f'images/planets/{i}.png'), (ENEMY_SIZE, ENEMY_SIZE)).convert_alpha() for i in range(1, 7)]

pygame.mixer.init()
win_sound = pygame.mixer.Sound('sound/win.mp3')
lose_sound = pygame.mixer.Sound('sound/lose.mp3')
ping_sound = pygame.mixer.Sound('sound/ping.mp3')
shot_sound = pygame.mixer.Sound('sound/shot.mp3')
boom_sound = pygame.mixer.Sound('sound/boom.mp3')

# Functions
def set_host_port():
    global HOST, PORT
    HOST = simpledialog.askstring("Input", "Enter host:", parent=root)
    PORT = simpledialog.askinteger("Input", "Enter port:", parent=root)
    root.destroy()

def display_bullet_count():
    bullet_count_text = font.render("Bullets: " + str(bullet_count), True, WHITE)
    screen.blit(bullet_count_text, (10, 10))

def detect_collision(bullet_pos, enemy_pos):
    bx, by = bullet_pos
    ex, ey = enemy_pos
    if (bx >= ex and bx < (ex + ENEMY_SIZE)) or (bx + BULLET_SIZE >= ex and bx + BULLET_SIZE < (ex + ENEMY_SIZE)):
        if (by >= ey and by < (ey + ENEMY_SIZE)) or (by + BULLET_SIZE >= ey and by + BULLET_SIZE < (ey + ENEMY_SIZE)):
            return True
    return False

def show_alert(screen, message, color):
    alert_box_pos = (100, 100)
    alert_box_size = (600, 100)
    text_color = WHITE

    pygame.draw.rect(screen, color, (*alert_box_pos, *alert_box_size))
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, text_color)
    text_size = text.get_size()
    text_pos = (alert_box_pos[0] + (alert_box_size[0] - text_size[0]) / 2, alert_box_pos[1] + (alert_box_size[1] - text_size[1]) / 2)
    screen.blit(text, text_pos)
    pygame.display.flip()
    pygame.time.delay(4000)

def win():
    messages.append("win")
    win_sound.play()
    show_alert(screen, "You win!", (10, 255, 10))

def lose():
    messages.append("lose")
    lose_sound.play()
    show_alert(screen, "You Lose!", (250, 10, 10))

def client_session(connection):
    client_rcv = Thread(target=client_receive, args=(connection,))
    client_rcv.start()
    while True:
        if messages:
            connection.send(messages.pop(0).encode())

def client_receive(connection):
    global specific_enemy_pos
    while True:
        client_message = connection.recv(2048).decode()
        specific_enemy_pos.insert(0, int(client_message))

# Tkinter Setup
root = tk.Tk()
root.geometry("300x150")
root.title("server")
input_button = tk.Button(root, text="initiate server", command=set_host_port)
input_button.pack(pady=20)
root.mainloop()

# Start Server
server = socket(AF_INET, SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
connection, addr = server.accept()
client_thread = Thread(target=client_session, args=(connection,))
client_thread.start()

# Game Loop
running = True
player_pos = [WIDTH / 2, HEIGHT - 2 * PLAYER_SIZE]

while running:
    pygame.time.delay(20)
    screen.fill(BLACK)

    # Draw enemies
    for i in range(len(planets)):
        screen.blit(planets[i], enemy_list[i])
    display_bullet_count()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= PLAYER_SPEED
    if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - PLAYER_SIZE:
        player_pos[0] += PLAYER_SPEED
    if keys[pygame.K_SPACE] and bullet_count > 0 and bullet_state == "ready":
        shot_sound.play()
        bullet_state = "fire"
        bullet_pos[0] = player_pos[0] + PLAYER_SIZE / 2 - BULLET_SIZE / 2
        bullet_pos[1] = player_pos[1]
        bullet_count -= 1

    if bullet_state == "fire":
        screen.blit(laser_bullet, bullet_pos)
        bullet_pos[1] -= BULLET_SPEED
        if bullet_pos[1] < 0:
            bullet_state = "ready"

    for enemy_pos in enemy_list[:]:
        if detect_collision(bullet_pos, enemy_pos):
            if enemy_pos == specific_enemy_pos:
                win()
                pygame.quit()
                sys.exit()
            boom_sound.play()
            hit_index = enemy_list.index(enemy_pos)
            enemy_list.pop(hit_index)
            planets.pop(hit_index)
            messages.append("d" + str(enemy_pos[0]))
            if bullet_count <= 0:
                win()
                pygame.quit()
                sys.exit()
            bullet_state = "ready"

    curr_state = f"{player_pos[0]}${bullet_pos[0]}${bullet_pos[1]}${bullet_state}"
    messages.append(curr_state)
    screen.blit(player_image, player_pos)

    if bullet_count <= 0 and bullet_pos[1] <= 0:
        lose()
        pygame.quit()
        sys.exit()

    pygame.display.update()

pygame.quit()
