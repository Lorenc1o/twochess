import tkinter as tk
from PIL import Image, ImageTk
from .board import Board

class Game:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=1300, height=800, bg='white')
        self.canvas.pack()
        self.board = Board()
        self.selected_piece_position = None
        self.canvas.bind("<Button-1>", self.on_square_clicked)
        
        # Press 'r' to reset the board
        self.root.bind('r', self.reset_game)

        # Press 'q' to quit
        self.root.bind('q', self.quit)

        # Press 'm' to go back to the menu
        self.root.bind('m', self.go_to_menu)

        # Keep track of turns. 0: White Left, 1: Black Right, 2: White Right, 3: Black Left
        self.current_turn = 0
        
        # Load all piece images
        self.piece_images = {}
        colors = ['white', 'black']
        pieces = ['r', 'n', 'b', 'q', 'k', 'p']
        for color in colors:
            for piece in pieces:
                image = Image.open(f'twochess/images/{color}-{piece}.png')
                image = image.resize((90, 90))  # Assuming square size is 100x100, adjust if needed
                self.piece_images[f'{color}-{piece}'] = ImageTk.PhotoImage(image)

                image = Image.open(f'twochess/images/{color}-{piece}_active.png')
                image = image.resize((90, 90))  # Assuming square size is 100x100, adjust if needed
                self.piece_images[f'{color}-{piece}_active'] = ImageTk.PhotoImage(image)

                if piece == 'k':
                    image = Image.open(f'twochess/images/{color}-{piece}_check.png')
                    image = image.resize((90, 90))
                    self.piece_images[f'{color}-{piece}_check'] = ImageTk.PhotoImage(image)

        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        for i in range(8):
            for j in range(13):
                x1 = j * 100
                y1 = i * 100
                x2 = x1 + 100
                y2 = y1 + 100

                if (i + j) % 2 == 0:
                    color = 'white'
                else:
                    color = 'grey'

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

                piece = self.board.board[i][j]
                if piece:
                    # Draw the active pieces (those that can be moved)
                    # Check the kings first for checks
                    if piece.piece_type == 'k' and piece.check_for_check(self.board.board, piece.team, (i, j)):
                            image = self.piece_images[f'{piece.team}-{piece.piece_type}_check']
                            self.canvas.create_image(x1+5, y1+5, anchor='nw', image=image)
                    else:
                        if self.current_turn == 0:
                            if piece.team == 'white' and j <= 6:
                                image = self.piece_images[f'{piece.team}-{piece.piece_type}_active']
                                self.canvas.create_image(x1+5, y1+5, anchor='nw', image=image)
                            else:
                                image = self.piece_images[f'{piece.team}-{piece.piece_type}']
                                self.canvas.create_image(x1+5, y1+5, anchor='nw', image=image)
                        elif self.current_turn == 1:
                            if piece.team == 'black' and j <= 6:
                                image = self.piece_images[f'{piece.team}-{piece.piece_type}_active']
                                self.canvas.create_image(x1+5, y1+5, anchor='nw', image=image)
                            else:
                                image = self.piece_images[f'{piece.team}-{piece.piece_type}']
                                self.canvas.create_image(x1+5, y1+5, anchor='nw', image=image)
                        elif self.current_turn == 2:
                            if piece.team == 'white' and j >= 6:
                                image = self.piece_images[f'{piece.team}-{piece.piece_type}_active']
                                self.canvas.create_image(x1+5, y1+5, anchor='nw', image=image)
                            else:
                                image = self.piece_images[f'{piece.team}-{piece.piece_type}']
                                self.canvas.create_image(x1+5, y1+5, anchor='nw', image=image)
                        elif self.current_turn == 3:
                            if piece.team == 'black' and j >= 6:
                                image = self.piece_images[f'{piece.team}-{piece.piece_type}_active']
                                self.canvas.create_image(x1+5, y1+5, anchor='nw', image=image)
                            else:
                                image = self.piece_images[f'{piece.team}-{piece.piece_type}']
                                self.canvas.create_image(x1+5, y1+5, anchor='nw', image=image)

    def on_square_clicked(self, event):
        x = event.y // 100
        y = event.x // 100

        # Only allow moving a piece if the right player is moving
        if self.selected_piece_position:
            print(self.selected_piece_position)
            piece = self.board.board[self.selected_piece_position[0]][self.selected_piece_position[1]]
            if piece:
                if ((self.current_turn == 0 and piece.team == 'white' and self.selected_piece_position[1] <= 6)
                    or (self.current_turn == 1 and piece.team == 'black' and self.selected_piece_position[1] <= 6)
                    or (self.current_turn == 2 and piece.team == 'white' and self.selected_piece_position[1] >= 6)
                    or (self.current_turn == 3 and piece.team == 'black' and self.selected_piece_position[1] >= 6)):
                        if self.board.move_piece(self.selected_piece_position, (x, y)):
                            self.current_turn = (self.current_turn + 1) % 4
                self.selected_piece_position = None
            else:
                print(f"Clicked on square ({x}, {y}), turn of the {'white' if self.current_turn in [0, 2] else 'black'} player")
                self.selected_piece_position = (x, y)
        else:
            print(f"Clicked on square ({x}, {y}), turn of the {'white' if self.current_turn in [0, 2] else 'black'} player")
            self.selected_piece_position = (x, y)

        self.draw_board()

    def reset_game(self, event):
        self.board = Board()
        self.current_turn = 0
        self.draw_board()

    def quit(self):
        # Quit the application
        self.root.destroy()

    def go_to_menu(self, event):
        # Go back to the menu
        menu = Menu(self.root)
        self.canvas.destroy()

