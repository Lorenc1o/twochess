import tkinter as tk
from .game import Game

class Menu:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(root)
        self.frame.pack()

        # Add a "New Game" button
        self.new_game_button = tk.Button(self.frame, text="New Game", command=self.new_game)

        self.new_game_button.pack()

        # Add a "Quit" button
        self.quit_button = tk.Button(self.frame, text="Quit", command=self.quit)
        self.quit_button.pack()

    def new_game(self):
        # Start a new game
        game = Game(self.root)
        self.frame.destroy()

    def quit(self):
        # Quit the application
        self.root.destroy()

