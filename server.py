from socket import *
from threading import *

state = []
messages = []
specific_enemy_pos = [100]
# Connection Data
host = '127.0.0.1'
port = 8888


def client_session(connection):
    global messages
    client_rcv = Thread(target=client_recieve,args=(connection,))
    client_rcv.start()
    while True:
        if messages:
            connection.send(messages.pop(0).encode())

def client_recieve(connection):
    while True:
        global specific_enemy_pos
        client_message=connection.recv(2048).decode()
        print(client_message)
        specific_enemy_pos.insert(0,int(client_message))

        

import pygame
import random
import sys
colours = [(24, 208, 17),(255, 239, 0),(242, 0, 234),(5, 20, 240)]

# Initialize Pygame
pygame.init()
print("try")
# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Pygame Shooter')

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
enemy_list = [[100, 100],[300, 100],[500, 100],[700, 100]]
  # Specific enemy for game over condition

# Bullet settings
bullet_size = 10
bullet_pos = [0, 0]
bullet_speed = 20
bullet_state = "ready"
bullet_count = 3  # Player starts with three bullets

# Font settings
font = pygame.font.SysFont("monospace", 35)

# Function to display the bullet count
def display_bullet_count(bullet_count):
    bullet_count_text = font.render("Bullets: " + str(bullet_count), True, BLACK)
    screen.blit(bullet_count_text, (10, 10))

# Function to detect collision
def detect_collision(bullet_pos, enemy_pos):
    bx, by = bullet_pos
    ex, ey = enemy_pos
    if (bx >= ex and bx < (ex + enemy_size)) or (bx + bullet_size >= ex and bx + bullet_size < (ex + enemy_size)):
        if (by >= ey and by < (ey + enemy_size)) or (by + bullet_size >= ey and by + bullet_size < (ey + enemy_size)):
            return True
    return False

def win():
    # Send a win message to the client
    connection.send('win'.encode())
    # Display a win message on the server
    print("You win!")

# Starting Server
server = socket(AF_INET, SOCK_STREAM)
server.bind((host, port))
server.listen(5)

connection, addr = server.accept()
client_thread = Thread(target=client_session,args=(connection,))
client_thread.start()
print("try")


# Game loop



running = True
while running:
    pygame.time.delay(20)
    screen.fill(WHITE)

    # Draw enemies
    i = 0
    for enemy_pos in enemy_list:
        pygame.draw.rect(screen, colours[i], (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))
        i+=1

    # Display bullet count
    display_bullet_count(bullet_count)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] < width - player_size:
        player_pos[0] += player_speed

    # Shooting bullets
    if keys[pygame.K_SPACE] and bullet_count > 0:
        if bullet_state == "ready":
            bullet_state = "fire"
            bullet_pos[0] = player_pos[0] + player_size / 2 - bullet_size / 2
            bullet_pos[1] = player_pos[1]
            bullet_count -= 1  # Decrease bullet count

    # Bullet movement
    if bullet_state == "fire":
        pygame.draw.rect(screen, RED, (bullet_pos[0], bullet_pos[1], bullet_size, bullet_size))
        bullet_pos[1] -= bullet_speed
        if bullet_pos[1] < 0:
            bullet_state = "ready"

    # Collision detection
    for enemy_pos in enemy_list[:]:
        if detect_collision(bullet_pos, enemy_pos):
            if enemy_pos == specific_enemy_pos:
                win()
                pygame.quit()
                sys.exit()  # End the game if the specific enemy is hit
            enemy_list.remove(enemy_pos)
            messages.append("d"+str(enemy_pos[0]))
            bullet_state = "ready"

    curr_state = str(player_pos[0]) + "$" + str(bullet_pos[0])+"$"+str(bullet_pos[1])+"$"+bullet_state
    messages.append(curr_state)
    # Draw player
    pygame.draw.rect(screen, RED, (player_pos[0], player_pos[1], player_size, player_size))

    # Update display
    pygame.display.update()

# Quit Pygame
pygame.quit()

    
    
