from .piece import Piece

class Board:
    def __init__(self):
        self.board = self.create_board()
        self.last_double_step_move = None
        self.n_kings = {'white': 2, 'black': 2}

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

        if piece is not None and piece.can_move(start, end, self.board, self.n_kings[piece.team],  self.last_double_step_move):
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
                    if captured_piece.piece_type == 'k' and captured_piece.team == 'white':
                        self.n_kings['white'] -= 1
                    elif captured_piece.piece_type == 'k' and captured_piece.team == 'black':
                        self.n_kings['black'] -= 1

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

