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

        self.white_move = True  # white's turn to move at first
        self.move_log = []

        self.move_functions = {"P": self.get_pawn_moves, "R": self.get_rook_moves, "N": self.get_knight_moves,
                               "B": self.get_bishop_moves, "Q": self.get_queen_moves, "K": self.get_king_moves}

    def make_move(self, move):
        if self.board[move.start_row][move.start_col] != "--":  # checks if start_sq is empty
            if move.promotion():
                if self.board[move.start_row][move.start_col][0] == "w":
                    self.board[move.end_row][move.end_col] = "wQ"
                else:
                    self.board[move.end_row][move.end_col] = "bQ"
            else:
                self.board[move.end_row][move.end_col] = move.piece_moved
            self.board[move.start_row][move.start_col] = "--"
            self.move_log.append(move)
            print(move.get_notation())
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
            turn = self.board[r][c][0]
            if (turn == 'w' and self.white_move) or (turn == 'b' and not self.white_move):
                piece = self.board[r][c][1]
                self.move_functions[piece](r, c, moves)
        return moves

    def get_pawn_moves(self, r, c, moves):
        if self.white_move:
            if self.board[r - 1][c] == "--":  # 1 square forward
                moves.append(Move((r, c), (r - 1, c), self.board, self.move_log))
                if r == 6 and self.board[r - 2][c] == "--":  # 2 squares forward
                    moves.append(Move((r, c), (r - 2, c), self.board, self.move_log))
            if c > 0 and self.board[r - 1][c - 1][0] == "b":  # left capture
                moves.append(Move((r, c), (r - 1, c - 1), self.board, self.move_log))
            if c < 7 and self.board[r - 1][c + 1][0] == "b":  # right capture
                moves.append(Move((r, c), (r - 1, c + 1), self.board, self.move_log))

        else:  # black pawns
            if self.board[r + 1][c] == "--":  # 1 square forward
                moves.append(Move((r, c), (r + 1, c), self.board, self.move_log))
                if r == 1 and self.board[r + 2][c] == "--":  # 2 squares forward
                    moves.append(Move((r, c), (r + 2, c), self.board, self.move_log))
            if c > 0 and self.board[r + 1][c - 1][0] == "w":  # left capture
                moves.append(Move((r, c), (r + 1, c - 1), self.board, self.move_log))
            if c < 7 and self.board[r + 1][c + 1][0] == "w":  # right capture
                moves.append(Move((r, c), (r + 1, c + 1), self.board, self.move_log))

    def get_rook_moves(self, r, c, moves):
        for i in range(r + 1, len(self.board)):  # vertical down
            if self.board[i][c] == "--":
                moves.append(Move((r, c), (i, c), self.board, self.move_log))
                continue
            if (self.white_move and self.board[i][c][0] == "b") or (not self.white_move and self.board[i][c][0] == "w"):
                moves.append(Move((r, c), (i, c), self.board, self.move_log))
                break
            if (self.white_move and self.board[i][c][0] == "w") or (not self.white_move and self.board[i][c][0] == "b"):
                break

        for i in range(r - 1, -1, -1):  # vertical up
            if self.board[i][c] == "--":
                moves.append(Move((r, c), (i, c), self.board, self.move_log))
                continue
            if (self.white_move and self.board[i][c][0] == "b") or (not self.white_move and self.board[i][c][0] == "w"):
                moves.append(Move((r, c), (i, c), self.board, self.move_log))
                break
            if (self.white_move and self.board[i][c][0] == "w") or (not self.white_move and self.board[i][c][0] == "b"):
                break

        for i in range(c + 1, len(self.board)):  # horizontal right
            if self.board[r][i] == "--":
                moves.append(Move((r, c), (r, i), self.board, self.move_log))
                continue
            if (self.white_move and self.board[r][i][0] == "b") or (not self.white_move and self.board[r][i][0] == "w"):
                moves.append(Move((r, c), (r, i), self.board, self.move_log))
                break
            if (self.white_move and self.board[r][i][0] == "w") or (not self.white_move and self.board[r][i][0] == "b"):
                break

        for i in range(c - 1, -1, -1):  # horizontal left
            if self.board[r][i] == "--":
                moves.append(Move((r, c), (r, i), self.board, self.move_log))
                continue
            if (self.white_move and self.board[r][i][0] == "b") or (not self.white_move and self.board[r][i][0] == "w"):
                moves.append(Move((r, c), (r, i), self.board, self.move_log))
                break
            if (self.white_move and self.board[r][i][0] == "w") or (not self.white_move and self.board[r][i][0] == "b"):
                break

    def get_bishop_moves(self, r, c, moves):
        # top right
        row = r - 1
        col = c + 1
        while (row >= 0) and (col < len(self.board)):
            if self.board[row][col] == "--":
                moves.append(Move((r, c), (row, col), self.board, self.move_log))
                row -= 1
                col += 1
                continue
            if (self.white_move and self.board[row][col][0] == "b") or (not self.white_move and self.board[row][col][0] == "w"):
                moves.append(Move((r, c), (row, col), self.board, self.move_log))
                break
            if (self.white_move and self.board[row][col][0] == "w") or (not self.white_move and self.board[row][col][0] == "b"):
                break

        # top left
        row = r - 1
        col = c - 1
        while (row >= 0) and (col >= 0):
            if self.board[row][col] == "--":
                moves.append(Move((r, c), (row, col), self.board, self.move_log))
                row -= 1
                col -= 1
                continue
            if (self.white_move and self.board[row][col][0] == "b") or (not self.white_move and self.board[row][col][0] == "w"):
                moves.append(Move((r, c), (row, col), self.board, self.move_log))
                break
            if (self.white_move and self.board[row][col][0] == "w") or (not self.white_move and self.board[row][col][0] == "b"):
                break

        # bottom left
        row = r + 1
        col = c - 1
        while (row < len(self.board)) and (col >= 0):
            if self.board[row][col] == "--":
                moves.append(Move((r, c), (row, col), self.board, self.move_log))
                row += 1
                col -= 1
                continue
            if (self.white_move and self.board[row][col][0] == "b") or (not self.white_move and self.board[row][col][0] == "w"):
                moves.append(Move((r, c), (row, col), self.board, self.move_log))
                break
            if (self.white_move and self.board[row][col][0] == "w") or (not self.white_move and self.board[row][col][0] == "b"):
                break

        # bottom right
        row = r + 1
        col = c + 1
        while (row < len(self.board)) and (col < len(self.board[0])):
            if self.board[row][col] == "--":
                moves.append(Move((r, c), (row, col), self.board, self.move_log))
                row += 1
                col += 1
                continue
            if (self.white_move and self.board[row][col][0] == "b") or (not self.white_move and self.board[row][col][0] == "w"):
                moves.append(Move((r, c), (row, col), self.board, self.move_log))
                break
            if (self.white_move and self.board[row][col][0] == "w") or (not self.white_move and self.board[row][col][0] == "b"):
                break

    def get_knight_moves(self, r, c, moves):
        rows = [r - 2, r - 2, r + 2, r + 2, r - 1, r + 1, r - 1, r + 1]
        cols = [c + 1, c - 1, c + 1, c - 1, c + 2, c + 2, c - 2, c - 2]
        for row, col in zip(rows, cols):
            if (row in range(len(self.board))) and (col in range(len(self.board[0]))):
                if self.board[row][col] == "--":
                    moves.append(Move((r, c), (row, col), self.board, self.move_log))
                if (self.white_move and self.board[row][col][0] == "b") or (not self.white_move and self.board[row][col][0] == "w"):
                    moves.append(Move((r, c), (row, col), self.board, self.move_log))

    def get_king_moves(self, r, c, moves):
        rows = [r - 1, r + 1, r, r, r - 1, r - 1, r + 1, r + 1]
        cols = [c, c, c - 1, c + 1, c - 1, c + 1, c - 1, c + 1]
        for row, col in zip(rows, cols):
            if (row in range(len(self.board))) and (col in range(len(self.board[0]))):
                if self.board[row][col] == "--":
                    moves.append(Move((r, c), (row, col), self.board, self.move_log))
                if (self.white_move and self.board[row][col][0] == "b") or (not self.white_move and self.board[row][col][0] == "w"):
                    moves.append(Move((r, c), (row, col), self.board, self.move_log))

    def get_queen_moves(self, r, c, moves):
        self.get_rook_moves(r, c, moves)
        self.get_bishop_moves(r, c, moves)


class Move:
    def __init__(self, start_sq, end_sq, board, move_log):
        self.start_row = start_sq[0]
        self.end_row = end_sq[0]
        self.start_col = start_sq[1]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.move_ID = int(str(self.start_row) + str(self.start_col) + str(self.end_row) + str(self.end_col))

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_ID == other.move_ID
        return False

    def get_notation(self):
        """
        outputs out notation for each move. ADD CASTLING, DISAMBIGUATION.
        """
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
