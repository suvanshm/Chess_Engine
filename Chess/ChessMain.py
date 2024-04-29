"""
Driver file. Handles user input and displays game state.
"""

import pygame as p
import ChessEngine
import MoveFinder
from multiprocessing import Process, Queue

WIDTH = HEIGHT = 512
RIGHT_OFFSET = 250
DOWN_OFFSET = 100
DIM = 8
SQ_SIZE = HEIGHT // DIM
MAX_FPS = 60
IMAGES = {}


def load_images():
    """ initialize dictionary of images, called only once in main """
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bP", "wR", "wN", "wB", "wQ", "wK", "wP"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("Chess\\chess_images\\" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
        # alternative path for other OS 
        # IMAGES[piece] = p.transform.scale(p.image.load("chess_images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


def main():
    p.init()
    screen = p.display.set_mode((WIDTH + RIGHT_OFFSET, HEIGHT + DOWN_OFFSET))
    clock = p.time.Clock()
    screen.fill(p.Color("black"))
    move_log_font = p.font.SysFont('Dejavu Sans Mono', 14, False, False)
    gs = ChessEngine.GameState()
    valid_moves = gs.get_valid_moves()
    print([x.get_notation() for x in valid_moves])
    move_made = False
    animate = False 
    load_images()
    running = True
    sq_selected = ()
    sq_clicks = []
    game_over = False
    undo = False
    human_white = True # if a human is playing as white
    human_black = True # if a human is playing as black
    movefinder_process = None
    AIThinking = False

    while running:
        human_turn = (gs.white_move and human_white) or (not gs.white_move and human_black)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # mouse handlers
            elif e.type == p.MOUSEBUTTONDOWN:
                if not game_over and human_turn: 
                    location = p.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if sq_selected == (row, col) or col >= 8 or row >= 8:
                        sq_selected = ()
                        sq_clicks = []
                    else:
                        sq_selected = (row, col)
                        sq_clicks.append(sq_selected)
                    if len(sq_clicks) == 2:
                        move = ChessEngine.Move(sq_clicks[0], sq_clicks[1], gs)
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                gs.make_move(valid_moves[i])
                                move_made = True
                                animate = True
                                sq_clicks = []
                                sq_selected = ()
                        if not move_made:
                            sq_clicks = [sq_selected]
            # key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    undo = True
                    gs.undo_board_history()
                    gs.undo_move()
                    move_made = True # we need to update the valid moves
                    animate = False
                    game_over = False
                    gs.checkmate = False
                    gs.stalemate = False
                    gs.insufficient_material = False
                    gs.threefold_repetition = False
                    if AIThinking: 
                        movefinder_process.terminate()
                        AIThinking = False
                        human_turn = True


                if e.key == p.K_r:
                    gs = ChessEngine.GameState()
                    valid_moves = gs.get_valid_moves()
                    sq_selected = ()
                    sq_clicks = []
                    move_made = False
                    animate = False
                    game_over = False
                    if AIThinking: 
                        movefinder_process.terminate()
                        AIThinking = False

        
        # AI Move Finder Logic 
        if not game_over and not human_turn:
            if not AIThinking:
                AIThinking = True
                AIMove = None
                return_queue = Queue()
                movefinder_process = Process(target=MoveFinder.negamax_helper, args=(gs, valid_moves, return_queue))
                movefinder_process.start()
                #AIMove = MoveFinder.negamax_helper(gs, valid_moves)
                #AIMove = MoveFinder.minmax_helper(gs, valid_moves)
            
            if not movefinder_process.is_alive():
                AIMove = return_queue.get()
                if AIMove is None:
                    print('no move found by engine')
                    AIMove = MoveFinder.find_random_move(valid_moves)
                gs.make_move(AIMove)
                move_made = True
                animate = True
                AIThinking = False

        
        if move_made:
            if animate:
                animate_move(gs.move_log[-1], screen, gs.board, clock)
            valid_moves = gs.get_valid_moves()
            print([x.get_notation() for x in valid_moves])
            if undo == False: 
                gs.update_board_history()
                gs.threefold_repetition = gs.is_threefold_repetition()
            undo = False
            gs.insufficient_material = gs.is_insufficient_material()
            move_made = False

        draw_gamestate(screen, gs, sq_selected, valid_moves, move_log_font)

        if gs.checkmate: 
            game_over = True
            if gs.white_move:
                draw_endgame_text(screen, 'checkmate! black wins')
            else:
                draw_endgame_text(screen, 'checkmate! white wins')
        elif gs.stalemate:
            game_over = True
            draw_endgame_text(screen, 'draw: stalemate')
        elif gs.insufficient_material:
            game_over = True
            draw_endgame_text(screen, 'draw: insufficient material')
        elif gs.threefold_repetition:
            game_over = True
            draw_endgame_text(screen, 'draw: threefold repetition')
        
        clock.tick(MAX_FPS)
        p.display.flip()


def draw_gamestate(screen, gs, sq_selected, valid_moves, move_log_font):
    draw_board(screen)
    highlight_last_move(screen, gs)
    highlight_avl_moves(screen, gs, sq_selected, valid_moves)
    draw_pieces(screen, gs.board)
    draw_move_log(screen, gs, move_log_font)
    #draw_buttons(screen)


def draw_board(screen):
    #colors = [p.Color("white"), p.Color("gray")]
    colors = [(241, 217, 192), (169, 121, 101)] # light and dark brown
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


def highlight_avl_moves(screen, gs, sq_selected, valid_moves):
    if sq_selected != ():
        r, c = sq_selected
        if gs.board[r][c][0] == ("w" if gs.white_move else "b"):
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(50)  # transparency value
            s.fill(p.Color("red"))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            s.fill(p.Color("green"))
            for move in valid_moves:
                if move.start_row == r and move.start_col == c:
                    screen.blit(s, (move.end_col * SQ_SIZE, move.end_row * SQ_SIZE))


def highlight_last_move(screen, gs):
    if len(gs.move_log) != 0:
        move = gs.move_log[-1]
        s = p.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(50)
        s.fill(p.Color("blue"))
        screen.blit(s, (move.start_col * SQ_SIZE, move.start_row * SQ_SIZE))
        screen.blit(s, (move.end_col * SQ_SIZE, move.end_row * SQ_SIZE))


def draw_move_log(screen, gs, font):
    move_log_rect = p.Rect(WIDTH, 0, RIGHT_OFFSET, HEIGHT)
    p.draw.rect(screen, p.Color("black"), move_log_rect)
    move_log = gs.move_log
    move_texts = []
    for i in range(0, len(move_log), 2):
        move_string = str(i // 2 + 1) + "." + move_log[i].get_notation() + ","
        if i + 1 < len(move_log):
            move_string += move_log[i + 1].get_notation() + ""
        move_texts.append(move_string)
    padding = 5
    text_y = padding
    line_spacing = 2 
    # add title 'move log' underlined 
    text_object = font.render("Move Log", True, p.Color('white'))
    text_location = move_log_rect.move(padding, padding)
    screen.blit(text_object, text_location)
    text_y += text_object.get_height() + line_spacing
    line_width = move_log_rect.width - padding # maximum width of text in pixels
    current_width = 0
    for i in range(len(move_texts)):
        text = move_texts[i]
        text_width = font.size(text + " ")[0]
        if current_width + text_width <= line_width:
            text_location = move_log_rect.move(padding/2 + current_width, text_y)
            screen.blit(font.render(text, True, p.Color('white')), text_location)
            current_width += text_width
        else:
            text_y += font.size("Ag")[1] + line_spacing
            current_width = 0
            text_location = move_log_rect.move(padding/2 + current_width, text_y)
            screen.blit(font.render(text, True, p.Color('white')), text_location)
            current_width += text_width



def animate_move(move, screen, board, clock):
    delta_x = move.end_col - move.start_col
    delta_y = move.end_row - move.start_row
    frames_per_square = 5  # frames to move one square
    frame_count = max(abs(delta_x), abs(delta_y)) * frames_per_square

    for frame in range(frame_count + 1):
        r, c = (move.start_row + delta_y * frame / frame_count, 
                move.start_col + delta_x * frame / frame_count)
        draw_board(screen)
        draw_pieces(screen, board)
        # erase the piece moved from its ending square
        # color = 'white' if (move.end_row + move.end_col) % 2 == 0 else 'gray'
        color = (241, 217, 192) if (move.end_row + move.end_col) % 2 == 0 else (169, 121, 101) # light and dark brown 
        end_square = p.Rect(move.end_col * SQ_SIZE, move.end_row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, end_square)
        # draw captured piece onto rectangle
        if move.piece_captured != '--':
            screen.blit(IMAGES[move.piece_captured], end_square)
        # draw moving piece
        screen.blit(IMAGES[move.piece_moved], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(MAX_FPS)


def draw_endgame_text(screen, text):
    font = p.font.SysFont('Courier', 32, True, False)
    text_object = font.render(text, 0, p.Color('Black'))
    # center the text
    text_location = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - text_object.get_width() / 2, HEIGHT / 2 - text_object.get_height() / 2)
    screen.blit(text_object, text_location)


if __name__ == '__main__':
    main()
