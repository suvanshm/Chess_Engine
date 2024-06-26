"""
Driver file. Handles user input and displays game state.
"""

import pygame as p
import ChessEngine

OFFSET = 30
WIDTH = HEIGHT = 512
DIM = 8
SQ_SIZE = HEIGHT // DIM
MAX_FPS = 15
IMAGES = {}


def load_images():
    """ initialize dictionary of images, called only once in main """
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bP", "wR", "wN", "wB", "wQ", "wK", "wP"]
    for piece in pieces:
        # print current path 
        path = "C:\\Users\\suvan\\ChessEngine\\Chess_Engine\\Chess\\chess_images\\"
        # import images grom path using names of pieces
        #IMAGES[piece] = p.transform.scale(p.image.load(path + piece + ".png"), (SQ_SIZE, SQ_SIZE))
        IMAGES[piece] = p.transform.scale(p.image.load("Chess\\chess_images\\" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    valid_moves = gs.get_valid_moves()
    print([x.get_notation() for x in valid_moves])
    move_made = False
    load_images()
    running = True
    sq_selected = ()
    sq_clicks = []
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # mouse handlers
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sq_selected == (row, col):
                    sq_selected = ()
                    sq_clicks = []
                else:
                    sq_selected = (row, col)
                    sq_clicks.append(sq_selected)
                if len(sq_clicks) == 2:
                    move = ChessEngine.Move(sq_clicks[0], sq_clicks[1], gs)
                    if move in valid_moves:
                        gs.make_move(move)
                        move_made = True
                        sq_clicks = []
                        sq_selected = ()
                    else:
                        sq_clicks = [sq_selected]
            # key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undo_move()
                    move_made = True # we need to update the valid moves

        if move_made:
            valid_moves = gs.get_valid_moves()
            print([x.get_notation() for x in valid_moves])
            move_made = False

        draw_gamestate(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


def draw_gamestate(screen, gs):
    draw_board(screen)
    draw_pieces(screen, gs.board)


def draw_board(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIM):
        for c in range(DIM):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_pieces(screen, board):
    for r in range(DIM):
        for c in range(DIM):
            piece = board[r][c]
            if piece != "--":  # not empty
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == '__main__':
    main()
