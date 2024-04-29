"""
Stores game state, valid moves, and move log.
"""

import numpy as np
import string
import hashlib

class GameState:
    def __init__(self):
        # board is 8x8 array with piece names and empty squares represented by --
        self.board = np.array([
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP" for _ in range(8)],
            ["--" for _ in range(8)],
            ["--" for _ in range(8)],
            ["--" for _ in range(8)],
            ["--" for _ in range(8)],
            ["wP" for _ in range(8)],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]])
        
        self.board_history = {} # store board states for threefold repetition check

        self.white_move = True  # white's turn to move at first
        self.move_log = []

        self.move_functions = {"P": self.get_pawn_moves, "R": self.get_rook_moves, "N": self.get_knight_moves,
                               "B": self.get_bishop_moves, "Q": self.get_queen_moves, "K": self.get_king_moves}

        self.white_king_loc = (7, 4)
        self.black_king_loc = (0, 4)

        self.checkmate = False
        self.stalemate = False
        self.insufficient_material = False
        self.threefold_repetition = False



    def make_move(self, move, print_move=True):
        if self.board[move.start_row][move.start_col] != "--":  # checks if start_sq is empty
            # edge case: castling
            if move.castle:
                if move.castle_type == "short": 
                    if self.white_move: 
                        self.board[7][5] = "wR"
                        self.board[7][7] = "--"

                    if not self.white_move: 
                        self.board[0][5] = "bR"
                        self.board[0][7] = "--"

                if move.castle_type == "long": 
                    if self.white_move: 
                        self.board[7][3] = "wR"
                        self.board[7][0] = "--"

                    if not self.white_move: 
                        self.board[0][3] = "bR"
                        self.board[0][0] = "--"

                self.board[move.end_row][move.end_col] = move.piece_moved
            # edge case: promotion
            elif move.promotion:
                if self.board[move.start_row][move.start_col][0] == "w":
                    self.board[move.end_row][move.end_col] = "wQ"
                else:
                    self.board[move.end_row][move.end_col] = "bQ"

            # edge case: en passant
            elif move.enpassant:
                self.board[move.start_row][move.end_col] = "--"
                self.board[move.end_row][move.end_col] = move.piece_moved
                
            else:
                self.board[move.end_row][move.end_col] = move.piece_moved

            self.board[move.start_row][move.start_col] = "--"

            self.move_log.append(move)
            #self.update_board_history()
            #self.threefold_repetition = self.is_threefold_repetition()

            self.white_move = not self.white_move  # turn changes

            if print_move:
                print(move.get_notation())

            # updating king location
            if move.piece_moved == "wK":
                self.white_king_loc = (move.end_row, move.end_col)
            elif move.piece_moved == "bK":
                self.black_king_loc = (move.end_row, move.end_col)

    def undo_move(self):
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.white_move = not self.white_move  # turn changes

            # en passant
            if move.enpassant:
                self.board[move.end_row][move.end_col] = "--"
                self.board[move.start_row][move.end_col] = move.piece_captured
            else:
                self.board[move.end_row][move.end_col] = move.piece_captured
            
            # castling
            if move.castle:
                if move.castle_type == "short": 
                    if self.white_move: 
                        self.board[7][7] = "wR"
                        self.board[7][5] = "--"

                    if not self.white_move: 
                        self.board[0][7] = "bR"
                        self.board[0][5] = "--"

                if move.castle_type == "long": 
                    if self.white_move: 
                        self.board[7][0] = "wR"
                        self.board[7][3] = "--"

                    if not self.white_move: 
                        self.board[0][0] = "bR"
                        self.board[0][3] = "--"

            # updating king location
            if move.piece_moved == "wK":
                self.white_king_loc = (move.start_row, move.start_col)
            elif move.piece_moved == "bK":
                self.black_king_loc = (move.start_row, move.start_col)
            
            self.threefold_repetition = False
            self.checkmate = False
            self.stalemate = False
            self.insufficient_material = False

    def get_valid_moves(self):
        turn = "w" if self.white_move else "b"
        moves = self.get_all_moves()
        for i in range(len(moves) - 1, -1, -1):
            self.make_move(moves[i], print_move=False)
            if self.in_check(check_color=turn):
                moves.remove(moves[i])
            self.undo_move()
            
        if len(moves) == 0:
            if self.in_check(check_color=turn):
                self.checkmate = True
                print("CHECKMATE")
            else:
                self.stalemate = True
                print("STALEMATE")
        return moves

    def in_check(self, check_color, r=None, c=None):
        if check_color == "w":
            enemy_r = self.black_king_loc[0]
            enemy_c = self.black_king_loc[1]
        else:
            enemy_r = self.white_king_loc[0]
            enemy_c = self.white_king_loc[1]

        if r is None and c is None:
            if check_color == "w":
                r = self.white_king_loc[0]
                c = self.white_king_loc[1]
            else:
                r = self.black_king_loc[0]
                c = self.black_king_loc[1]
        else: 
            r = r
            c = c
        
        # adjacent kings (not technically a check but important to filter from legal moves)
        if abs(r - enemy_r) <= 1 and abs(c - enemy_c) <= 1:
            return True

        # orthogonal checks
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        for d in directions:
            for i in range(1, len(self.board)):
                row = r + (d[0] * i)
                col = c + (d[1] * i)
                if (row in range(len(self.board))) and (col in range(len(self.board[0]))):
                    if self.board[row][col] == "--":
                        continue
                    elif check_color == self.board[row][col][0]:
                        break
                    elif self.board[row][col][1] in ["P", "B", "N"]:
                        break
                    elif self.board[row][col][1] in ["R", "Q"]:
                        return True
                else:
                    break

        # diagonal checks
        directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        for d in directions:
            for i in range(1, len(self.board)):
                row = r + (d[0] * i)
                col = c + (d[1] * i)
                if (row in range(len(self.board))) and (col in range(len(self.board[0]))):
                    if self.board[row][col] == "--":
                        continue
                    elif check_color == self.board[row][col][0]:
                        break
                    elif self.board[row][col][1] in ["R", "N"] or (self.board[row][col][1] == "P" and i > 1):
                        break
                    elif (self.board[row][col][1] in ["Q", "B"]) or (self.board[row][col][1] == "P" and i == 1):
                        return True
                else:
                    break

        # knight checks
        rows = [r - 2, r - 2, r + 2, r + 2, r - 1, r + 1, r - 1, r + 1]
        cols = [c + 1, c - 1, c + 1, c - 1, c + 2, c + 2, c - 2, c - 2]
        for row, col in zip(rows, cols):
            if (row in range(len(self.board))) and (col in range(len(self.board[0]))):
                if self.board[row][col][0] != check_color and (self.board[row][col][1] == "N"):
                    return True

        return False

    def get_all_moves(self):
        moves = []
        for r, c in np.ndindex(np.shape(self.board)):
            turn = self.board[r][c][0]
            if (turn == 'w' and self.white_move) or (turn == 'b' and not self.white_move):
                piece = self.board[r][c][1]
                self.move_functions[piece](r, c, moves)
        return moves

    def get_pawn_moves(self, r, c, moves):
        if self.white_move:
            if self.board[r - 1][c] == "--":  # 1 square forward
                moves.append(Move((r, c), (r - 1, c), self))
                if r == 6 and self.board[r - 2][c] == "--":  # 2 squares forward
                    moves.append(Move((r, c), (r - 2, c), self))
            if c > 0 and self.board[r - 1][c - 1][0] == "b":  # left capture
                moves.append(Move((r, c), (r - 1, c - 1), self))
            if c < 7 and self.board[r - 1][c + 1][0] == "b":  # right capture
                moves.append(Move((r, c), (r - 1, c + 1), self))

        else:  # black pawns
            if self.board[r + 1][c] == "--":  # 1 square forward
                moves.append(Move((r, c), (r + 1, c), self))
                if r == 1 and self.board[r + 2][c] == "--":  # 2 squares forward
                    moves.append(Move((r, c), (r + 2, c), self))
            if c > 0 and self.board[r + 1][c - 1][0] == "w":  # left capture
                moves.append(Move((r, c), (r + 1, c - 1), self))
            if c < 7 and self.board[r + 1][c + 1][0] == "w":  # right capture
                moves.append(Move((r, c), (r + 1, c + 1), self))
        
        # check if enpassant is possible or not 
        if len(self.move_log) > 0: 
            prev_move = self.move_log[-1] 
            if prev_move.piece_moved[1] == "P" and abs(prev_move.start_row - prev_move.end_row) == 2: 
                if r == prev_move.end_row and abs(c - prev_move.end_col) == 1: 
                    # moves.append(Move((r, c), (r - 1  if self.white_move else r + 1, prev_move.end_col), self))
                    en_passant_row = r - 1 if self.white_move else r + 1
                    moves.append(Move((r, c), (en_passant_row, prev_move.end_col), self))

    def get_rook_moves(self, r, c, moves):
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        for d in directions:
            for i in range(1, len(self.board)):
                row = r + (d[0] * i)
                col = c + (d[1] * i)
                if (row in range(len(self.board))) and (col in range(len(self.board[0]))):
                    if self.board[row][col] == "--":
                        moves.append(Move((r, c), (row, col), self))
                        continue
                    if (self.white_move and self.board[row][col][0] == "b") or (not self.white_move and self.board[row][col][0] == "w"):
                        moves.append(Move((r, c), (row, col), self))
                        break
                    if (self.white_move and self.board[row][col][0] == "w") or (not self.white_move and self.board[row][col][0] == "b"):
                        break
                else:
                    break

    def get_bishop_moves(self, r, c, moves):
        directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        for d in directions:
            for i in range(1, len(self.board)):
                row = r + (d[0] * i)
                col = c + (d[1] * i)
                if (row in range(len(self.board))) and (col in range(len(self.board[0]))):
                    if self.board[row][col] == "--":
                        moves.append(Move((r, c), (row, col), self))
                        continue
                    if (self.white_move and self.board[row][col][0] == "b") or (not self.white_move and self.board[row][col][0] == "w"):
                        moves.append(Move((r, c), (row, col), self))
                        break
                    if (self.white_move and self.board[row][col][0] == "w") or (not self.white_move and self.board[row][col][0] == "b"):
                        break
                else:
                    break

    def get_knight_moves(self, r, c, moves):
        rows = [r - 2, r - 2, r + 2, r + 2, r - 1, r + 1, r - 1, r + 1]
        cols = [c + 1, c - 1, c + 1, c - 1, c + 2, c + 2, c - 2, c - 2]
        for row, col in zip(rows, cols):
            if (row in range(len(self.board))) and (col in range(len(self.board[0]))):
                if self.board[row][col] == "--":
                    moves.append(Move((r, c), (row, col), self))
                if (self.white_move and self.board[row][col][0] == "b") or (not self.white_move and self.board[row][col][0] == "w"):
                    moves.append(Move((r, c), (row, col), self))

    def get_king_moves(self, r, c, moves):
        rows = [r - 1, r + 1, r, r, r - 1, r - 1, r + 1, r + 1]
        cols = [c, c, c - 1, c + 1, c - 1, c + 1, c - 1, c + 1]
        for row, col in zip(rows, cols):
            if (row in range(len(self.board))) and (col in range(len(self.board[0]))):
                if self.board[row][col] == "--":
                    moves.append(Move((r, c), (row, col), self))
                if (self.white_move and self.board[row][col][0] == "b") or (not self.white_move and self.board[row][col][0] == "w"):
                    moves.append(Move((r, c), (row, col), self))
        
        # check for castling
        turn = "w" if self.white_move else "b"
        possible_castles = self.can_castle(turn)
        if possible_castles['short']: 
            #print("SHORT CASTLE")
            if turn == "w": 
                #print("WHITE SHORT CASTLE")
                moves.append(Move(self.white_king_loc, (7, 6), self))
            if turn == "b": moves.append(Move(self.black_king_loc, (0, 6), self))
        if possible_castles['long']:
            if turn == "w": moves.append(Move(self.white_king_loc, (7, 2), self))
            if turn == "b": moves.append(Move(self.black_king_loc, (0, 2), self))

    def get_queen_moves(self, r, c, moves):
        self.get_rook_moves(r, c, moves)
        self.get_bishop_moves(r, c, moves)
    
    # Castling methods 
    def can_castle(self, color):
        result = {'short': False, 'long': False}
        # if king has moved, return false
        king = self.white_king_loc if color == "w" else self.black_king_loc
        if self.has_moved(king): return result
        # if in check, return false
        if self.in_check(color): return result 
        rooks = self.get_rook_locations(color)
        for rook in rooks:
            if self.has_moved(rook): continue # if rook moved, that side remains false
            if self.is_path_clear(king, rook, color): 
                if rook[1] == 0: 
                    result['long'] = True
                if rook[1] == 7: 
                    result['short'] = True
        return result
    
    def has_moved(self, loc):
        for move in self.move_log:
            if move.start_row == loc[0] and move.start_col == loc[1]: return True
        return False
    
    def get_rook_locations(self, color):
        rooks = []
        for r, c in np.ndindex(np.shape(self.board)):
            if self.board[r][c][0] == color and self.board[r][c][1] == "R":
                rooks.append((r, c))
        return rooks
    
    def is_path_clear(self, start, end, color):
        direction = 1 if end[1] > start[1] else -1
        for i in range(start[1] + direction, end[1], direction):
            if self.board[start[0]][i] != "--": return False
            if self.in_check(color, start[0], i): return False
        return True
    
    # checking for forced draw conditions
    def is_insufficient_material(self):
        w_pieces = []
        b_pieces = []

        for r,c in np.ndindex(np.shape(self.board)):
            if self.board[r][c] != "--" and self.board[r][c][1] != "K":
                if self.board[r][c][1] in ["Q", "R", "P"]: return False 
                if self.board[r][c][0] == "w":
                    w_pieces.append((self.board[r][c], (r,c)))
                else:
                    b_pieces.append((self.board[r][c], (r,c)))

        # at the minimum having any 2 pieces on the board means it's not insufficient material
        if len(w_pieces) > 1 or len(b_pieces) > 1: return False

        if len(w_pieces) == 0: 
            if len(b_pieces) == 0: return True # lone kings 
            if b_pieces[0][0][1] in ["N", "B"]: return True # king and knight or king and bishop
            return False

        if len(b_pieces) == 0:
            if w_pieces[0][0][1] in ["N", "B"]: return True
            return False

        # king and knight vs king and knight 
        if len(w_pieces) == 1 and w_pieces[0][0][1] == "N" and len(b_pieces) == 1 and b_pieces[0][0][1] == "N": return True

        # same color bishops
        if len(w_pieces) == 1 and w_pieces[0][0][1] == "B" and len(b_pieces) == 1 and b_pieces[0][0][1] == "B": 
            # check for square color of both bishops 
            w_sq = (w_pieces[0][1][0] + w_pieces[0][1][1]) % 2
            b_sq = (b_pieces[0][1][0] + b_pieces[0][1][1]) % 2
            return w_sq == b_sq

        return False
    
    def is_threefold_repetition(self):
        # check if the current board state has been repeated 3 times
        return any(value >= 3 for value in self.board_history.values())
    
    def update_board_history(self):
        raw_board_string = self.board.tostring().decode('utf-8')
        board_string = hashlib.md5(raw_board_string.encode()).hexdigest()
        #print(board_string)
        if board_string in self.board_history:
            self.board_history[board_string] += 1
            print(self.board_history[board_string], ":", board_string)
        else:
            #print("NEW: ", board_string)
            self.board_history[board_string] = 1
    
    def undo_board_history(self): 
        raw_board_string = self.board.tostring().decode('utf-8')
        board_string = hashlib.md5(raw_board_string.encode()).hexdigest()
        #print("undoing move: ", board_string)
        if board_string in self.board_history:
            #print("inside loop")
            self.board_history[board_string] -= 1
            print(self.board_history[board_string], ":", board_string)
            if self.board_history[board_string] == 0:
                #print("DELETING: ", board_string)
                del self.board_history[board_string]


        
    



class Move:
    def __init__(self, start_sq, end_sq, gs):
        self.gs = gs
        self.board = self.gs.board
        self.start_row = start_sq[0]
        self.end_row = end_sq[0]
        self.start_col = start_sq[1]
        self.end_col = end_sq[1]
        self.piece_moved = self.gs.board[self.start_row][self.start_col]
        self.piece_captured = self.gs.board[self.end_row][self.end_col]
        self.move_ID = int(str(self.start_row) + str(self.start_col) + str(self.end_row) + str(self.end_col))
        self.promotion = self.piece_moved[1] == "P" and (self.end_row == 0 or self.end_row == 7)
        self.enpassant = self.is_enpassant()
        self.castle = self.is_castle() 
        self.check = self.is_check()
        if self.castle: 
            self.castle_type = "short" if self.end_col == 6 else "long"

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_ID == other.move_ID
        return False
    

    def get_notation(self):
        """
        outputs out notation for each move. ADD CASTLING, DISAMBIGUATION, CHECK, CHECKMATE, STALEMATE.
        """
        # castling 
        if self.castle: 
            return "O-O" if self.castle_type == "short" else "O-O-O" 
        
        board_row = board_col = np.arange(8)
        letters = string.ascii_lowercase[:8]
        numbers = reversed([str(x) for x in np.arange(9)[1:]])

        # mapping square
        rank_map = {x: y for x, y in zip(board_row, numbers)}
        file_map = {x: y for x, y in zip(board_col, letters)}
        square = file_map[self.end_col] + rank_map[self.end_row]

        # mapping piece
        piece_map = {x: x for x in ["K", "Q", "R", "B", "N"]}
        piece_map["P"] = ""

        # check color
        rev_color_map = {"w": "b", "b": "w"}
        check_color = rev_color_map[self.piece_moved[0]]

        # empty output
        output = ""

        # en passant
        if self.is_enpassant():
            output = file_map[self.start_col] + "x" + square
            # if self.gs.in_check(check_color=check_color): output += "+"
            if self.check: output += "+"
            return output

        if self.piece_moved != "--":
            piece = piece_map[self.piece_moved[1]]
            if self.piece_captured == "--":
                output = piece + square
            else:
                if self.piece_moved[1] == "P":
                    piece = file_map[self.start_col]
                output = piece + "x" + square
            if self.promotion:
                output += "=Q"
            #if self.gs.in_check(check_color=check_color): output += "+"
            if self.check: output += "+"
            return output
        else:
            return None
        
    def is_enpassant(self): 
        # classify move as ep if pawn moves diagonally without capturing anything 
        # conditions for ep already checked in get_pawn_moves, only way we get a diagonal move without capturing is if it's an ep
        if self.piece_moved[1] == "P" and abs(self.end_col-self.start_col)==1 and self.piece_captured == "--": 
            self.piece_captured = "bP" if self.piece_moved[0] == "w" else "wP"
            return True
    
    def is_castle(self): 
        # classify move as castling if king moves 2 squares to the left or right
        # conditions for castling already checked in get_king_moves, only way we get a move of 2 squares is if it's a castle
        if self.piece_moved[1] == "K" and abs(self.end_col - self.start_col) == 2: 
            return True
        return False

    def is_check(self): 
        # classify move as check if it results in the opponent being in check
        if self.piece_moved == '--': 
            return False
        
        rev_color_map = {"w": "b", "b": "w"}
        check_color = rev_color_map[self.piece_moved[0]] # color of the opponent
        self.gs.make_move(self, print_move=False) 
        in_check =  self.gs.in_check(check_color=check_color)
        self.gs.undo_move() 
        return in_check