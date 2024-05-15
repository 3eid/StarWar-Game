import pygame
import sys
import re
from socket import *
from threading import *
host = '127.0.0.1'
port = 8888
selected_planet =0


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
root.title("Client")

# Add a button to trigger the input dialog
input_button = tk.Button(root, text="Connect a server", command=set_host_port)
input_button.pack(pady=20)

# # Start the Tkinter event loop
root.mainloop()


def win(screen):
    print("won")
    # Define the size and position of the alert box
    alert_box_pos = (100, 100)
    alert_box_size = (600, 100)
    alert_box_color = (10, 255, 10)   # green color
    text_color = (255, 255, 255)  # White color

    # Draw the alert box
    pygame.draw.rect(screen, alert_box_color, (*alert_box_pos, *alert_box_size))

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

    # Define the size and position of the alert box
    alert_box_pos = (100, 100)
    alert_box_size = (600, 100)
    alert_box_color = (250, 10, 10)  # Red color
    text_color = (255, 255, 255)  # White color

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



iswin = islose = False
new_bullet_pos =[]
selected = False
new_player_pos = 0.0
bullet_state = "ready"
def server_recieve(connection):
    global new_player_pos,enemy_list,new_bullet_pos,bullet_state,planets,iswin,islose
    while True:
        server_message=connection.recv(2048).decode()
        if server_message == "win":
            islose =True
        elif server_message == "lose":
            iswin=True
        elif server_message[0] == "d":
            hit = float(server_message[1:])
            hit_index = enemy_list.index([hit,100])
            enemy_list.pop(hit_index)
            planets.pop(hit_index)
        else:
            parts = server_message.split('$')
            new_player_pos = float(parts[0])
            new_bullet_posx = float(parts[1])
            new_bullet_posy = float(parts[2])
            new_bullet_pos  = [new_bullet_posx,new_bullet_posy]
            bullet_state = parts[-1]
            


client = socket(AF_INET, SOCK_STREAM)
client.connect((host, port))
client_thread = Thread(target=server_recieve,args=(client,))
client_thread.start()

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Planet Selector')

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

# Bullet settings
bullet_size = 50
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

triangle = pygame.image.load('images/triangle.png')
triangle = pygame.transform.scale(triangle, (bullet_size-30, bullet_size-35)).convert_alpha()
# Game loop


running = True
while running:
    screen.fill(BLACK)

    # Draw enemies
    for i in range(len(planets)):
        screen.blit(planets[i], enemy_list[i])
        
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
                    selected_planet = enemy_pos
    # Draw player
    screen.blit(player_image, [new_player_pos,player_pos[1]])
    #draw Bullets
    if selected_planet:
        screen.blit(triangle, [selected_planet[0]+18,70])
    if bullet_state =="fire":
        screen.blit(laser_bullet, [bullet_pos[0],bullet_pos[1]])
        bullet_pos[1] = new_bullet_pos[1]
        bullet_pos[0] = new_bullet_pos[0]
    if iswin:
        win(screen)
        pygame.quit()
        sys.exit()
    if islose:
        lose(screen)
        pygame.quit()
        sys.exit()
    # Update display
    pygame.display.update()

# Quit Pygame
pygame.quit()
