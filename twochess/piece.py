class Piece:
    def __init__(self, piece_type, team):
        self.piece_type = piece_type
        self.team = team
        self.first_move = True  # To check if it's the pawn's first move

    def can_move(self, start, end, board, n_kings, last_double_step_move=None):
        return self.is_valid_move(start,end, board, last_double_step_move) and not self.check_for_pin(board, self.team, start, end, n_kings)

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
    
    # def is_valid_move(self, start, end, board, last_double_step_move=None):
    #     valid_movements = {
    #         'p': self.is_valid_pawn_move,
    #         'k': self.is_valid_king_move,
    #         'q': self.is_valid_queen_move,
    #         'r': self.is_valid_rook_move,
    #         'b': self.is_valid_bishop_move,
    #         'n': self.is_valid_knight_move
    #     }
    #     validation_function = valid_movements.get(self.piece_type)
    #     if validation_function:
    #         if self.piece_type == 'p':
    #             return validation_function(start, end, board, last_double_step_move)
    #         else:
    #             return validation_function(start, end, board)
    #     return False

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
            step_x = dx // max(1, abs(dx))
            step_y = dy // max(1, abs(dy))
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
    
    def check_for_check(self, board, team, king_pos):
        for row in range(8):
            for col in range(13):
                piece = board[row][col]
                if piece is not None and piece.team != team and piece.is_valid_move((row, col), king_pos, board):
                    return True
        return False
    
    def check_for_checkmate(self, board, team, king_pos):
        for row in range(8):
            for col in range(13):
                piece = board[row][col]
                if piece is not None and piece.team == team:
                    for i in range(8):
                        for j in range(13):
                            if piece.is_valid_move((row, col), (i, j), board):
                                return False
        return True
    
    def check_for_stalemate(self, board, team, king_pos):
        for row in range(8):
            for col in range(13):
                piece = board[row][col]
                if piece is not None and piece.team == team:
                    for i in range(8):
                        for j in range(13):
                            if piece.is_valid_move((row, col), (i, j), board):
                                return False
        return True
    
    def check_for_pin(self, board, team, begin, end, n_kings):
        if n_kings == 2:
            return False

        # Find the kings
        king_pos = None
        for row in range(8):
            for col in range(13):
                piece = board[row][col]
                if piece is not None and piece.team == team and piece.piece_type == 'k':
                    king_pos = (row, col)
        
        # Check if the piece is pinned
        # Simulate the move
        temp = board[end[0]][end[1]]
        board[end[0]][end[1]] = board[begin[0]][begin[1]]
        board[begin[0]][begin[1]] = None

        # Check if the king is in check
        retval = self.check_for_check(board, team, king_pos)

        # Undo the move
        board[begin[0]][begin[1]] = board[end[0]][end[1]]
        board[end[0]][end[1]] = temp

        return retval

