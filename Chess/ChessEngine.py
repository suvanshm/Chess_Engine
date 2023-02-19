"""
Stores game state, valid moves, and move log.
"""

import numpy as np
import string


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
        # white's turn to move at first
        self.white_move = True
        self.move_log = []

    def make_move(self, move):
        if self.board[move.start_row][move.start_col] != "--":  # checks if start_sq is empty
            if move.promotion():
                if self.board[move.start_row][move.start_col][0] == "w":
                    self.board[move.end_row][move.end_col] = "wQ"
                else:
                    print("true")
                    self.board[move.end_row][move.end_col] = "bQ"
            else:
                self.board[move.end_row][move.end_col] = move.piece_moved
            self.board[move.start_row][move.start_col] = "--"
            self.move_log.append(move)
            self.white_move = not self.white_move  # turn changes

    def undo_move(self):
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_move = not self.white_move

    def get_valid_moves(self):
        return self.get_all_moves()

    def get_all_moves(self):
        moves = []
        for r, c in np.ndindex(np.shape(self.board)):
            turn = self.board[r][c][1]
            if (turn == 'w' and self.white_move) or (turn == 'b' and not self.white_move):
                pass


class Move:
    def __init__(self, start_sq, end_sq, board, move_log):
        self.start_row = start_sq[0]
        self.end_row = end_sq[0]
        self.start_col = start_sq[1]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]

    def get_notation(self):
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

        # empty output
        output = ""

        if self.piece_moved != "--":
            piece = piece_map[self.piece_moved[1]]
            if self.piece_captured == "--":
                output = piece + square
            else:
                if self.piece_moved[1] == "P":
                    piece = file_map[self.start_col]
                output = piece + "x" + square
            if self.promotion():
                output += "=Q"
            return output
        else:
            return None

    def promotion(self):
        if self.piece_moved[1] == "P":
            if (self.piece_moved[0] == "w" and self.end_row == 0) or (self.piece_moved[0] == "b" and self.end_row == 7):
                return True
        return False
