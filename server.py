from socket import *
from threading import *
import pygame
import sys

import tkinter as tk
from tkinter import simpledialog
host ="127.0.0.1"
port = 8000
# Function to set the host and port variables
def set_host_port():
    global host, port
    host = simpledialog.askstring("Input", "Enter host:", parent=root)
    port = simpledialog.askinteger("Input", "Enter port:", parent=root)
    # You can add validation or use the variables as needed here
    root.destroy()

# Create the main window
root = tk.Tk()
root.geometry("300x150")
root.title("server")

# Add a button to trigger the input dialog
input_button = tk.Button(root, text="initiate server", command=set_host_port)
input_button.pack(pady=20)

# # Start the Tkinter event loop
root.mainloop()

state = []
messages = []
specific_enemy_pos = [100]



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

        

pygame.mixer.init()
win_sound  = pygame.mixer.Sound('sound/win.mp3')
lose_sound = pygame.mixer.Sound('sound/lose.mp3')
ping_sound = pygame.mixer.Sound('sound/ping.mp3')
shot_sound = pygame.mixer.Sound('sound/shot.mp3')
boom_sound = pygame.mixer.Sound('sound/boom.mp3')

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Star War')

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
enemy_list = [[114, 100],[228, 100],[342, 100],[456, 100],[570, 100],[684, 100]]
  # Specific enemy for game over condition

# Bullet settings
bullet_size = 50
bullet_pos = [0, 0]
bullet_speed = 20
bullet_state = "ready"
bullet_count = 3  # Player starts with three bullets

# Font settings
font = pygame.font.SysFont("monospace", 35)

# Function to display the bullet count
def display_bullet_count(bullet_count):
    bullet_count_text = font.render("Bullets: " + str(bullet_count), True, WHITE)
    screen.blit(bullet_count_text, (10, 10))

# Function to detect collision
def detect_collision(bullet_pos, enemy_pos):
    bx, by = bullet_pos
    ex, ey = enemy_pos
    if (bx >= ex and bx < (ex + enemy_size)) or (bx + bullet_size >= ex and bx + bullet_size < (ex + enemy_size)):
        if (by >= ey and by < (ey + enemy_size)) or (by + bullet_size >= ey and by + bullet_size < (ey + enemy_size)):
            return True
    return False

def win(screen):
    messages.append("win")

    # Define the size and position of the alert box
    alert_box_pos = (100, 100)
    alert_box_size = (600, 100)
    alert_box_color = (10, 255, 10)   # Red color
    text_color = (255, 255, 255)  # White color

    # Draw the alert box
    pygame.draw.rect(screen, alert_box_color, (*alert_box_pos, *alert_box_size))
    win_sound.play()
    # Create a font object
    font = pygame.font.Font(None, 36)

    # Render the text
    text = font.render("You win!", True, text_color)

    # Get the text size
    text_size = text.get_size()

    # Calculate the position of the text
    text_pos = (alert_box_pos[0] + (alert_box_size[0] - text_size[0]) / 2,
                alert_box_pos[1] + (alert_box_size[1] - text_size[1]) / 2)

    # Blit the text onto the screen
    screen.blit(text, text_pos)

    # Update the display
    pygame.display.flip()

    # Pause the game for a few seconds to show the alert
    pygame.time.delay(4000)

def lose(screen):
    messages.append("lose")
    # Define the size and position of the alert box
    alert_box_pos = (100, 100)
    alert_box_size = (600, 100)
    alert_box_color = (250, 10, 10)  # Red color
    text_color = (255, 255, 255)  # White color
    lose_sound.play()
    # Draw the alert box
    pygame.draw.rect(screen, alert_box_color, (*alert_box_pos, *alert_box_size))

    # Create a font object
    font = pygame.font.Font(None, 36)

    # Render the text
    text = font.render("You Lose!", True, text_color)

    # Get the text size
    text_size = text.get_size()

    # Calculate the position of the text
    text_pos = (alert_box_pos[0] + (alert_box_size[0] - text_size[0]) / 2,
                alert_box_pos[1] + (alert_box_size[1] - text_size[1]) / 2)

    # Blit the text onto the screen
    screen.blit(text, text_pos)

    # Update the display
    pygame.display.flip()

    # Pause the game for a few seconds to show the alert
    pygame.time.delay(4000)



# Starting Server
server = socket(AF_INET, SOCK_STREAM)
server.bind((host, port))
server.listen(5)

connection, addr = server.accept()
client_thread = Thread(target=client_session,args=(connection,))
client_thread.start()
print("try")




# Load the image and scale it to the size of the player rectangle
player_image = pygame.image.load('images/plane/p.png')
player_image = pygame.transform.scale(player_image, (player_size, player_size)).convert_alpha()

# Load the image and scale it to the size of the player rectangle

planets = [ 
        pygame.transform.scale(pygame.image.load('images/planets/1.png'), (enemy_size, enemy_size)).convert_alpha(),
        pygame.transform.scale(pygame.image.load('images/planets/2.png'), (enemy_size, enemy_size)).convert_alpha(),
        pygame.transform.scale(pygame.image.load('images/planets/3.png'), (enemy_size, enemy_size)).convert_alpha(),
        pygame.transform.scale(pygame.image.load('images/planets/4.png'), (enemy_size, enemy_size)).convert_alpha(),
        pygame.transform.scale(pygame.image.load('images/planets/1.png'), (enemy_size, enemy_size)).convert_alpha(),
        pygame.transform.scale(pygame.image.load('images/planets/2.png'), (enemy_size, enemy_size)).convert_alpha(),
]

laser_bullet = pygame.image.load('images/bullet.png')
laser_bullet = pygame.transform.scale(laser_bullet, (bullet_size, bullet_size)).convert_alpha()

# Game loop


running = True
while running:
    pygame.time.delay(20)
    screen.fill(BLACK)

    # Draw enemies
    for i in range(len(planets)):
        screen.blit(planets[i], enemy_list[i])
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
            shot_sound.play()
            bullet_state = "fire"
            bullet_pos[0] = player_pos[0] + player_size / 2 - bullet_size / 2
            bullet_pos[1] = player_pos[1]
            bullet_count -= 1  # Decrease bullet count

    # Bullet movement
    if bullet_state == "fire":
        screen.blit(laser_bullet, [bullet_pos[0],bullet_pos[1]])
        bullet_pos[1] -= bullet_speed
        if bullet_pos[1] < 0:
            bullet_state = "ready"
        print(bullet_pos[1])
    # Collision detection
    for enemy_pos in enemy_list[:]:
        if detect_collision(bullet_pos, enemy_pos):
            if enemy_pos == specific_enemy_pos:
                win(screen)
                pygame.quit()
                sys.exit()  # End the game if the specific enemy is hit
            boom_sound.play()
            hit_index = enemy_list.index(enemy_pos)
            enemy_list.pop(hit_index)
            planets.pop(hit_index)
            messages.append("d"+str(enemy_pos[0]))
            if bullet_count <= 0 :
                win(screen)
                pygame.quit()
                sys.exit()
            bullet_state = "ready"

    curr_state = str(player_pos[0]) + "$" + str(bullet_pos[0])+"$"+str(bullet_pos[1])+"$"+bullet_state
    messages.append(curr_state)
    # Draw player
    screen.blit(player_image, player_pos)
    
    if bullet_count <= 0 and bullet_pos[1]<=0:
        lose(screen)
        pygame.quit()
        sys.exit() 
    # Update display
    pygame.display.update()

# Quit Pygame
pygame.quit()

    
    
