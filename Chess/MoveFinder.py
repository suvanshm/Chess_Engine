import random
import numpy as np
import time

piece_values = {
    'P': 100,
    'N': 320,
    'B': 330,
    'R': 500,
    'Q': 900,
    'K': 20000 # or 1000, not sure
}

pst_white_pawn = np.array([
    np.array([0,  0,  0,  0,  0,  0,  0,  0]),
    np.array([50, 50, 50, 50, 50, 50, 50, 50]),
    np.array([10, 10, 20, 30, 30, 20, 10, 10]),
    np.array([5,  5, 10, 25, 25, 10,  5,  5]),
    np.array([0,  0,  0, 20, 20,  0,  0,  0]),
    np.array([5, -5,-10,  0,  0,-10, -5,  5]),
    np.array([5, 10, 10,-20,-20, 10, 10,  5]),
    np.array([0,  0,  0,  0,  0,  0,  0,  0])
])

pst_black_pawn = np.flip(pst_white_pawn, axis=0)

pst_white_knight = np.array([
    np.array([-50,-40,-30,-30,-30,-30,-40,-50]),
    np.array([-40,-20,  0,  0,  0,  0,-20,-40]),
    np.array([-30,  0, 10, 15, 15, 10,  0,-30]),
    np.array([-30,  5, 15, 20, 20, 15,  5,-30]),
    np.array([-30,  0, 15, 20, 20, 15,  0,-30]),
    np.array([-30,  5, 10, 15, 15, 10,  5,-30]),
    np.array([-40,-20,  0,  5,  5,  0,-20,-40]),
    np.array([-50,-25,-30,-30,-30,-30,-25,-50])
])

pst_black_knight = np.flip(pst_white_knight, axis=0)


pst_white_bishop = np.array([
    np.array([-20,-10,-10,-10,-10,-10,-10,-20]),
    np.array([-10,  0,  0,  0,  0,  0,  0,-10]),
    np.array([-10,  0,  5, 10, 10,  5,  0,-10]),
    np.array([-10,  5,  5, 10, 10,  5,  5,-10]),
    np.array([-10,  0, 10, 10, 10, 10,  0,-10]),
    np.array([-10, 10, 10, 10, 10, 10, 10,-10]),
    np.array([-10,  5,  0,  0,  0,  0,  5,-10]),
    np.array([-20,-10,-10,-10,-10,-10,-10,-20])
])

pst_black_bishop = np.flip(pst_white_bishop, axis=0)


pst_white_rook = np.array([
    np.array([0,  0,  0,  0,  0,  0,  0,  0]),
    np.array([5, 10, 10, 10, 10, 10, 10,  5]),
    np.array([-5,  0,  0,  0,  0,  0,  0, -5]),
    np.array([-5,  0,  0,  0,  0,  0,  0, -5]),
    np.array([-5,  0,  0,  0,  0,  0,  0, -5]),
    np.array([-5,  0,  0,  0,  0,  0,  0, -5]),
    np.array([-5,  0,  0,  0,  0,  0,  0, -5]),
    np.array([0,  0,  0,  5,  5,  0,  0,  0])
])

pst_black_rook = np.flip(pst_white_rook, axis=0)

pst_white_queen = np.array([
    np.array([-20,-10,-10, -5, -5,-10,-10,-20]),
    np.array([-10,  0,  0,  0,  0,  0,  0,-10]),
    np.array([-10,  0,  5,  5,  5,  5,  0,-10]),
    np.array([ -5,  0,  5,  5,  5,  5,  0, -5]),
    np.array([  0,  0,  5,  5,  5,  5,  0, -5]),
    np.array([-10,  5,  5,  5,  5,  5,  0,-10]),
    np.array([-10,  0,  5,  0,  0,  0,  0,-10]),
    np.array([-20,-10,-10, -5, -5,-10,-10,-20])
])

pst_black_queen = np.flip(pst_white_queen, axis=0)

pst_white_king = np.array([
    np.array([-30,-40,-40,-50,-50,-40,-40,-30]),
    np.array([-30,-40,-40,-50,-50,-40,-40,-30]),
    np.array([-30,-40,-40,-50,-50,-40,-40,-30]),
    np.array([-30,-40,-40,-50,-50,-40,-40,-30]),
    np.array([-20,-30,-30,-40,-40,-30,-30,-20]),
    np.array([-10,-20,-20,-20,-20,-20,-20,-10]),
    np.array([ 20, 20,  0,  0,  0,  0, 20, 20]),
    np.array([ 20, 30, 10,  0,  0, 10, 30, 20])
])

pst_black_king = np.flip(pst_white_king, axis=0)

pst_white_king_endgame = np.array([
    np.array([-50,-40,-30,-20,-20,-30,-40,-50]),
    np.array([-30,-20,-10,  0,  0,-10,-20,-30]),
    np.array([-30,-10, 20, 30, 30, 20,-10,-30]),
    np.array([-30,-10, 30, 40, 40, 30,-10,-30]),
    np.array([-30,-10, 30, 40, 40, 30,-10,-30]),
    np.array([-30,-10, 20, 30, 30, 20,-10,-30]),
    np.array([-30,-30,  0,  0,  0,  0,-30,-30]),
    np.array([-50,-30,-30,-30,-30,-30,-30,-50])
])

pst_black_king_endgame = np.flip(pst_white_king_endgame, axis=0)

position_scores = { 
    'wP': pst_white_pawn,
    'wN': pst_white_knight,
    'wB': pst_white_bishop,
    'wR': pst_white_rook,
    'wQ': pst_white_queen,
    'wK': pst_white_king,
    'bP': pst_black_pawn,
    'bN': pst_black_knight,
    'bB': pst_black_bishop,
    'bR': pst_black_rook,
    'bQ': pst_black_queen,
    'bK': pst_black_king 
    }

checkmate_score = 20000
draw_score = 0
num_evaluations = 0
DEPTH = 3 

def find_random_move(valid_moves):
    return valid_moves[random.randint(0, len(valid_moves)-1)]

def negamax_helper(gs, valid_moves, return_queue):
    global best_move, num_evaluations
    best_move = None
    random.shuffle(valid_moves)
    num_evaluations = 0 # counter is reset
    #negamax(gs, valid_moves, DEPTH, color= 1 if gs.white_move else -1)
    start = time.time()
    negamax_alphabeta(gs, valid_moves, DEPTH, -checkmate_score, checkmate_score, 1 if gs.white_move else -1)
    if best_move is None:
        print("Negamax helper returning no move")
    else: 
        end = time.time()
        print("time taken: " + "{:.2f}".format(end-start))
    print("number of evaluations: " + str(num_evaluations))
    #return best_move
    return_queue.put(best_move)


def negamax_alphabeta(gs, valid_moves, depth, alpha, beta, color):
    global best_move
    if depth <= 0 or gs.checkmate or gs.stalemate or gs.threefold_repetition or gs.insufficient_material:
        return color * evaluate_board(gs)

    # move ordering - implement later
    max_eval = float('-inf')
    for move in valid_moves:
        gs.make_move(move, print_move=False)
        next_moves = gs.get_valid_moves()
        random.shuffle(next_moves)
        eval = -negamax_alphabeta(gs, next_moves, depth-1, -beta, -alpha, -color)
        if eval > max_eval:
            max_eval = eval
            if depth == DEPTH:
                best_move = move
                turn = 1 if gs.white_move else -1
                print("best move is: " + best_move.get_notation() + "  , score = " + str(turn * max_eval/100))
        gs.undo_move()
        if max_eval > alpha:
            alpha = max_eval
        if alpha >= beta:
            break
    return max_eval

def negamax(gs, valid_moves, depth, color):
    global best_move
    if depth == 0 or gs.checkmate or gs.stalemate or gs.threefold_repetition or gs.insufficient_material:
        return color * evaluate_board(gs)

    max_eval = -checkmate_score
    for move in valid_moves:
        gs.make_move(move, print_move=False)
        next_moves = gs.get_valid_moves()
        eval = -negamax(gs, next_moves, depth-1, -color)
        if eval > max_eval:
            max_eval = eval
            if depth == DEPTH:
                best_move = move
                print("best move is: " + best_move.get_notation())
        gs.undo_move()
    return max_eval

def minmax_helper(gs, valid_moves): 
    global best_move, num_evaluations
    best_move = None
    num_evaluations = 0 # counter is reset
    minmax(gs, valid_moves)
    if best_move is None:
        print(" minmax helper returning no move")
    else: 
        print("minmax helper returning move: " + best_move.get_notation())
    print("number of evaluations: " + str(num_evaluations))
    return best_move

def minmax(gs, valid_moves, depth=DEPTH): 
    global best_move
    if depth == 0 or gs.checkmate or gs.stalemate or gs.threefold_repetition or gs.insufficient_material:
        return evaluate_board(gs) 

    if gs.white_move: 
        # maximising player
        max_eval = float('-inf')
        for move in valid_moves: 
            gs.make_move(move, print_move=False) 
            next_moves = gs.get_valid_moves()
            eval = minmax(gs, next_moves, depth-1)
            gs.undo_move()
            if eval > max_eval:
                max_eval = eval
                if depth == DEPTH:
                    best_move = move
                    print("best move is: " + best_move.get_notation())
        return max_eval
    
    else:
        # minimising player
        min_eval = float('inf')
        for move in valid_moves: 
            gs.make_move(move, print_move=False) 
            next_moves = gs.get_valid_moves()
            eval = minmax(gs, next_moves, depth-1)
            gs.undo_move()
            if eval < min_eval:
                min_eval = eval
                if depth == DEPTH:
                    best_move = move
                    print("best move is: " + best_move.get_notation())
        return min_eval


def evaluate_board(gs): 
    global num_evaluations
    num_evaluations += 1
    if gs.checkmate:
        if gs.white_move:
            return -checkmate_score
        else:
            return checkmate_score
    elif gs.stalemate or gs.insufficient_material or gs.threefold_repetition:
        return draw_score
    score = score_material(gs)
    #print("material score: " + str(score))
    return score


def score_material(gs): 
    score = 0
    for row in range(len(gs.board)):  
        for col in range(len(gs.board[row])):
            piece = gs.board[row][col] 
            if piece != "--":
                position_score = position_scores[piece][row][col]
                if piece[0] == 'w':
                    score += piece_values[piece[1]] + position_score
                if piece[0] == 'b':
                    score -= piece_values[piece[1]] + position_score
    return score        

            

        



