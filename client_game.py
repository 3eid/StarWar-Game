import pygame
import sys
import re
from socket import *
from threading import *
new_bullet_pos =[]
selected = False
new_player_pos = 0.0
bullet_state = "ready"
def server_recieve(connection):
    global new_player_pos,enemy_list,new_bullet_pos,bullet_state
    while True:
        server_message=connection.recv(2048).decode()
        if server_message == "win":
            print("You Lose!!")
        elif server_message[0] == "d":
            hit = float(server_message[1:])
            enemy_list.remove([hit,100])
        else:
            parts = server_message.split('$')
            new_player_pos = float(parts[0])
            new_bullet_posx = float(parts[1])
            new_bullet_posy = float(parts[2])
            new_bullet_pos  = [new_bullet_posx,new_bullet_posy]
            bullet_state = parts[-1]
            


client = socket(AF_INET, SOCK_STREAM)
client.connect(('127.0.0.1', 8888))
client_thread = Thread(target=server_recieve,args=(client,))
client_thread.start()

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Enemy Selector')

# Define colors

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Player settings
player_size = 50
player_pos = [width / 2, height - 2 * player_size]
player_speed = 10

# Enemy settings
enemy_size = 50
enemy_list = [[100, 100], [300, 100], [500, 100], [700, 100]]

# Bullet settings
bullet_size = 20
bullet_pos = [0, 0]
bullet_speed = 20
bullet_state = "ready"
# Function to detect if the mouse click is on an enemy
def detect_click_on_enemy(mouse_pos, enemy_pos):
    mx, my = mouse_pos
    ex, ey = enemy_pos
    if ex <= mx <= ex + enemy_size and ey <= my <= ey + enemy_size:
        return True
    return False

def send_selected_place(pos):
    global selected
    selected = True
    pos_str = str(pos[0])
    client.send(pos_str.encode())
# Game loop
running = True
while running:
    screen.fill(WHITE)

    # Draw enemies
    for enemy_pos in enemy_list:
        pygame.draw.rect(screen, RED, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and selected != True:
            mouse_pos = pygame.mouse.get_pos()
            for enemy_pos in enemy_list:
                if detect_click_on_enemy(mouse_pos, enemy_pos):
                    print(f"Enemy at {enemy_pos} was selected.")
                    # Here you can add code to send the selected enemy's position to the server
                    send_selected_place(enemy_pos)
    # Draw player
    pygame.draw.rect(screen, RED, (new_player_pos, player_pos[1], player_size, player_size))
    #draw Bulleti
    if bullet_state =="fire":
        pygame.draw.rect(screen, RED, (bullet_pos[0], bullet_pos[1], bullet_size, bullet_size))
        bullet_pos[1] = new_bullet_pos[1]
        bullet_pos[0] = new_bullet_pos[0]
    print(bullet_state)
    # Update display
    pygame.display.update()

# Quit Pygame
pygame.quit()
