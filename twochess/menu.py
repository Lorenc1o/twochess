import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from twochess.game import Game
import random

class Menu:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(root, bg='#FFFFFF')
        self.frame.pack()

        # Add a background image to the window
        image = Image.open('twochess/images/banner.png')
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(self.frame, image=photo)
        label.image = photo
        label.pack()

        # Create a style for the buttons
        style = ttk.Style()
        style.configure('Menu.TButton', font=('Arial', 14), background='#7BAFD4', foreground='#FFFFFF')

        # Add a "New Game" button
        self.new_game_button = ttk.Button(self.frame, text="New Game", command=self.show_new_game_options, style='Menu.TButton')
        self.new_game_button.pack(pady=10)

        # Add a "Quit" button
        self.quit_button = ttk.Button(self.frame, text="Quit", command=self.quit, style='Menu.TButton')
        self.quit_button.pack(pady=10)

        # Initialize play buttons
        self.play_white_button = None
        self.play_black_button = None
        self.play_random_button = None
        self.return_button = None

    def show_new_game_options(self):
        # Remove the "New Game" and "Quit" buttons
        self.new_game_button.pack_forget()
        self.quit_button.pack_forget()

        # Add three buttons to select the top team
        self.play_white_button = ttk.Button(self.frame, text="Play White", command=lambda: self.start_new_game('white'), style='Menu.TButton', width=20)
        self.play_white_button.pack(pady=10)

        self.play_black_button = ttk.Button(self.frame, text="Play Black", command=lambda: self.start_new_game('black'), style='Menu.TButton', width=20)
        self.play_black_button.pack(pady=10)

        self.play_random_button = ttk.Button(self.frame, text="Play Random", command=lambda: self.start_new_game(random.choice(['white', 'black'])), style='Menu.TButton', width=20)
        self.play_random_button.pack(pady=10)

        # Add a "Return" button
        self.return_button = ttk.Button(self.frame, text="Return", command=self.show_original_buttons, style='Menu.TButton', width=20)
        self.return_button.pack(pady=10)


    def show_original_buttons(self):
        # Remove the three buttons and add the "New Game" and "Quit" buttons
        self.play_white_button.pack_forget()
        self.play_black_button.pack_forget()
        self.play_random_button.pack_forget()
        self.return_button.pack_forget()

        self.new_game_button.pack(pady=10)
        self.quit_button.pack(pady=10)

    def start_new_game(self, top_team):
        # Start a new game with the specified top team
        game = Game(self.root, top_team)
        self.frame.destroy()

    def quit(self):
        # Quit the application
        self.root.destroy()