import pygame
import sys
from socket import *
from threading import Thread
import tkinter as tk
from tkinter import simpledialog

# Constants
HOST = '127.0.0.1'
PORT = 8888

# Initialize game state variables
selected_planet = 0
iswin = False
islose = False
new_bullet_pos = []
selected = False
new_player_pos = 0.0
bullet_state = "ready"

# Initialize Tkinter for input
def set_host_port():
    global HOST, PORT
    HOST = simpledialog.askstring("Input", "Enter host:", parent=root)
    PORT = simpledialog.askinteger("Input", "Enter port:", parent=root)
    root.destroy()

root = tk.Tk()
root.geometry("300x150")
root.title("Client")
input_button = tk.Button(root, text="Connect to server", command=set_host_port)
input_button.pack(pady=20)
root.mainloop()

# Server communication
def server_receive(connection):
    global new_player_pos, enemy_list, new_bullet_pos, bullet_state, planets, iswin, islose
    while True:
        server_message = connection.recv(2048).decode()
        if server_message == "win":
            islose = True
        elif server_message == "lose":
            iswin = True
        elif server_message.startswith("d"):
            hit = float(server_message[1:])
            hit_index = enemy_list.index([hit, 100])
            enemy_list.pop(hit_index)
            planets.pop(hit_index)
        else:
            parts = server_message.split('$')
            new_player_pos = float(parts[0])
            new_bullet_posx = float(parts[1])
            new_bullet_posy = float(parts[2])
            new_bullet_pos = [new_bullet_posx, new_bullet_posy]
            bullet_state = parts[-1]

client = socket(AF_INET, SOCK_STREAM)
client.connect((HOST, PORT))
client_thread = Thread(target=server_receive, args=(client,))
client_thread.start()

# Pygame initialization
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Planet Selector')

# Colors and settings
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
player_size = 50
player_pos = [width / 2, height - 2 * player_size]
player_speed = 10
enemy_size = 50
enemy_list = [[114, 100], [228, 100], [342, 100], [456, 100], [570, 100], [684, 100]]
bullet_size = 50
bullet_pos = [0, 0]
bullet_speed = 20

# Load images
player_image = pygame.image.load('images/plane/p.png')
player_image = pygame.transform.scale(player_image, (player_size, player_size)).convert_alpha()
planets = [
    pygame.transform.scale(pygame.image.load(f'images/planets/{i+1}.png'), (enemy_size, enemy_size)).convert_alpha()
    for i in range(6)
]
laser_bullet = pygame.image.load('images/bullet.png')
laser_bullet = pygame.transform.scale(laser_bullet, (bullet_size, bullet_size)).convert_alpha()
triangle = pygame.image.load('images/triangle.png')
triangle = pygame.transform.scale(triangle, (bullet_size - 30, bullet_size - 35)).convert_alpha()

# Helper functions
def detect_click_on_enemy(mouse_pos, enemy_pos):
    mx, my = mouse_pos
    ex, ey = enemy_pos
    return ex <= mx <= ex + enemy_size and ey <= my <= ey + enemy_size

def send_selected_place(pos):
    global selected
    selected = True
    pos_str = str(pos[0])
    client.send(pos_str.encode())

def display_alert(screen, message, color):
    alert_box_pos = (100, 100)
    alert_box_size = (600, 100)
    text_color = (255, 255, 255)
    pygame.draw.rect(screen, color, (*alert_box_pos, *alert_box_size))
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, text_color)
    text_size = text.get_size()
    text_pos = (alert_box_pos[0] + (alert_box_size[0] - text_size[0]) / 2,
                alert_box_pos[1] + (alert_box_size[1] - text_size[1]) / 2)
    screen.blit(text, text_pos)
    pygame.display.flip()
    pygame.time.delay(4000)

def win(screen):
    display_alert(screen, "You win!", (10, 255, 10))

def lose(screen):
    display_alert(screen, "You Lose!", (250, 10, 10))

# Game loop
running = True
while running:
    screen.fill(BLACK)

    for i in range(len(planets)):
        screen.blit(planets[i], enemy_list[i])
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not selected:
            mouse_pos = pygame.mouse.get_pos()
            for enemy_pos in enemy_list:
                if detect_click_on_enemy(mouse_pos, enemy_pos):
                    send_selected_place(enemy_pos)
                    selected_planet = enemy_pos

    screen.blit(player_image, [new_player_pos, player_pos[1]])
    
    if selected_planet:
        screen.blit(triangle, [selected_planet[0] + 18, 70])
    
    if bullet_state == "fire":
        screen.blit(laser_bullet, [bullet_pos[0], bullet_pos[1]])
        bullet_pos = new_bullet_pos

    if iswin:
        win(screen)
        pygame.quit()
        sys.exit()
    
    if islose:
        lose(screen)
        pygame.quit()
        sys.exit()
    
    pygame.display.update()

pygame.quit()
