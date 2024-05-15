
import tkinter as tk
from tkinter import simpledialog
isserver = False
def start_server():
    global isserver
    isserver = True
    root.destroy()

def start_client():
    global isserver
    isserver = False
    root.destroy()


def close():
    root.destroy()

while True:
    # Create the main window
    root = tk.Tk()
    root.geometry("300x200")
    root.title("Star Wars")

    # Add a button to trigger the input dialog
    input_button = tk.Button(root, text="Be The server (aircraft)", command=start_server)
    input_button.pack(pady=20)
    input_button2 = tk.Button(root, text="Be The client(planet)", command=start_client)
    input_button2.pack(pady=20)
    input_button3 = tk.Button(root, text="close", command=close)
    input_button3.pack(pady=20)

    # # Start the Tkinter event loop
    root.mainloop()
    if isserver:
        from server import *
    else:
        from client import *
