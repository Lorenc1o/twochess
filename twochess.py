import tkinter as tk
from PIL import Image, ImageTk

class Piece:
    def __init__(self, piece_type, team):
        self.piece_type = piece_type
        self.team = team
        self.first_move = True  # To check if it's the pawn's first move

    def is_valid_move(self, start, end, board, last_double_step_move=None):
        if self.piece_type == 'p':
            return self.is_valid_pawn_move(start, end, board, last_double_step_move)
        if self.piece_type == 'k':
            return self.is_valid_king_move(start, end, board)
        if self.piece_type == 'q':
            return self.is_valid_queen_move(start, end, board)
        if self.piece_type == 'r':
            return self.is_valid_rook_move(start, end, board)
        if self.piece_type == 'b':
            return self.is_valid_bishop_move(start, end, board)
        if self.piece_type == 'n':
            return self.is_valid_knight_move(start, end, board)
        return False

    def is_valid_pawn_move(self, start, end, board, last_double_step_move=None):
        direction = 1 if self.team == 'white' else -1
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        # Check for normal move or capture
        if dx == direction and (dy == 0 or abs(dy) == 1):
            if dy == 0 and board[end[0]][end[1]] is None: 
                return True
            elif abs(dy) == 1 and ((board[end[0]][end[1]] is not None and board[end[0]][end[1]].team != self.team) or last_double_step_move == (end[0] - direction, end[1])):
                return True
        # Check for double step move from start position
        elif dx == 2*direction and dy == 0 and start[0] == (6 if direction == -1 else 1) and board[end[0]][end[1]] is None:
            return True
        return False

    def is_valid_king_move(self, start, end, board):
        dx = abs(end[0] - start[0])
        dy = abs(end[1] - start[1])
        # Check if king is moving to a square within one step
        if dx <= 1 and dy <= 1:
            # If king is in columns 1-6, it cannot move to column 7 or greater
            if start[1] <= 6 and end[1] >= 7:
                return False
            # If king is in columns 8-13, it cannot move to column 7 or less
            elif start[1] >= 8 and end[1] <= 7:
                return False
            # Otherwise, the king is moving within its allowed columns
            else:
                return (board[end[0]][end[1]] is None or board[end[0]][end[1]].team != self.team)
        else:
            return False

    def is_valid_queen_move(self, start, end, board):
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        if dx == 0 or dy == 0 or abs(dx) == abs(dy):  # moving in a straight line
            step_x = dx // max(1, abs(dx))
            step_y = dy // max(1, abs(dy))
            for i in range(1, max(abs(dx), abs(dy))):
                # Checking all intermediate squares for pieces
                if board[start[0]+i*step_x][start[1]+i*step_y] is not None:
                    return False
            return board[end[0]][end[1]] is None or board[end[0]][end[1]].team != self.team
        return False
    
    def is_valid_rook_move(self, start, end, board):
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        if dx == 0 or dy == 0:  # moving in a straight line
            step_x = dx // max(1, abs(dx)) if dx != 0 else 0
            step_y = dy // max(1, abs(dy)) if dy != 0 else 0
            for i in range(1, max(abs(dx), abs(dy))):
                # Checking all intermediate squares for pieces
                if board[start[0]+i*step_x][start[1]+i*step_y] is not None:
                    return False
            return board[end[0]][end[1]] is None or board[end[0]][end[1]].team != self.team
        return False

    def is_valid_bishop_move(self, start, end, board):
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        if abs(dx) == abs(dy):  # moving diagonally
            step_x = dx // abs(dx)
            step_y = dy // abs(dy)
            for i in range(1, abs(dx)):  # dx and dy are same in magnitude
                # Checking all intermediate squares for pieces
                if board[start[0]+i*step_x][start[1]+i*step_y] is not None:
                    return False
            return board[end[0]][end[1]] is None or board[end[0]][end[1]].team != self.team
        return False

    def is_valid_knight_move(self, start, end, board):
        dx = abs(end[0] - start[0])
        dy = abs(end[1] - start[1])
        # Knight moves two squares in one direction and one in the other
        return (dx, dy) == (2, 1) or (dx, dy) == (1, 2)


class Board:
    def __init__(self):
        self.board = self.create_board()
        self.last_double_step_move = None

    def create_board(self):
        board = [[None for _ in range(13)] for _ in range(8)]
        setup = 'rnbknbqbnkbnr'
        teams = ['white', 'black']
        
        for team in teams:
            for i in range(13):
                board[0 if team == 'white' else 7][i] = Piece(setup[i], team)
                board[1 if team == 'white' else 6][i] = Piece('p', team)
        return board

    def move_piece(self, start, end):
        piece = self.board[start[0]][start[1]]

        if piece is not None and piece.is_valid_move(start, end, self.board, self.last_double_step_move):
                # Capture the piece in the destination square, if any
                # Check for en passant
                if self.board[end[0]][end[1]] is None and piece.piece_type == 'p' and start[1] != end[1]:
                    print('En passant!')
                    captured_piece = self.board[start[0]][end[1]]
                    self.board[start[0]][end[1]] = None
                else:
                    captured_piece = self.board[end[0]][end[1]]
                if captured_piece is not None:
                    print(f'{piece.team} {piece.piece_type} captured {captured_piece.team} {captured_piece.piece_type}!')

                # Move the piece
                self.board[end[0]][end[1]] = piece
                self.board[start[0]][start[1]] = None

                # Check for pawn promotion
                if self.board[end[0]][end[1]].piece_type == 'p' and ((self.board[end[0]][end[1]].team == 'white' and end[0] == 0) or (self.board[end[0]][end[1]].team == 'black' and end[0] == 7)):
                    self.board[end[0]][end[1]].piece_type = 'q'

                # Check for double step move
                if self.board[end[0]][end[1]].piece_type == 'p' and abs(start[0] - end[0]) == 2:
                    print('Double step move!')
                    print(end)
                    self.last_double_step_move = end
                else:
                    self.last_double_step_move = None

                # Check for en passant
                if self.board[end[0]][end[1]].piece_type == 'p' and abs(start[1] - end[1]) == 1 and self.board[end[0]][end[1]] is None:
                    self.board[start[0]][end[1]] = None
                    print('En passant!')

                return True
        return False


class Game:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=1300, height=800, bg='white')
        self.canvas.pack()
        self.board = Board()
        self.selected_piece_position = None
        self.canvas.bind("<Button-1>", self.on_square_clicked)

        # Keep track of turns. 0: White Left, 1: Black Right, 2: White Right, 3: Black Left
        self.current_turn = 0
        
        # Load all piece images
        self.piece_images = {}
        colors = ['white', 'black']
        pieces = ['r', 'n', 'b', 'q', 'k', 'p']
        for color in colors:
            for piece in pieces:
                image = Image.open(f'images/{color}-{piece}.png')
                image = image.resize((90, 90))  # Assuming square size is 100x100, adjust if needed
                self.piece_images[f'{color}-{piece}'] = ImageTk.PhotoImage(image)

                image = Image.open(f'images/{color}-{piece}_active.png')
                image = image.resize((90, 90))  # Assuming square size is 100x100, adjust if needed
                self.piece_images[f'{color}-{piece}_active'] = ImageTk.PhotoImage(image)

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

root = tk.Tk()
game = Game(root)
root.mainloop()
