import tkinter as tk
from tkinter import simpledialog

class StarWarsApp:
    def __init__(self):
        self.is_server = False
        self.init_main_window()

    def init_main_window(self):
        self.root = tk.Tk()
        self.root.geometry("300x200")
        self.root.title("Star Wars")
        self.create_widgets()
        self.root.mainloop()

    def create_widgets(self):
        server_button = tk.Button(self.root, text="Be The server (aircraft)", command=self.start_server)
        server_button.pack(pady=20)
        
        client_button = tk.Button(self.root, text="Be The client (planet)", command=self.start_client)
        client_button.pack(pady=20)
        
        close_button = tk.Button(self.root, text="Close", command=self.close_app)
        close_button.pack(pady=20)

    def start_server(self):
        self.is_server = True
        self.root.destroy()

    def start_client(self):
        self.is_server = False
        self.root.destroy()

    def close_app(self):
        self.root.destroy()

    def run(self):
        while True:
            self.init_main_window()
            if self.is_server:
                import server  # Assuming server.py exists in the same directory
                server.main()  # Assuming server.py has a main function
            else:
                import client  # Assuming client.py exists in the same directory
                client.main()  # Assuming client.py has a main function

if __name__ == "__main__":
    app = StarWarsApp()
    app.run()
