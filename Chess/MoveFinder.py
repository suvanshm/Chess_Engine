import random

piece_values = {
    'P': 1,
    'N': 3,
    'B': 3,
    'R': 5,
    'Q': 9,
    'K': 0 # or 1000, not sure
}
checkmate_score = 1000
draw_score = 0
num_evaluations = 0
DEPTH = 3

def find_random_move(valid_moves):
    return valid_moves[random.randint(0, len(valid_moves)-1)]

def negamax_helper(gs, valid_moves):
    global best_move, num_evaluations
    best_move = None
    random.seed(11)
    random.shuffle(valid_moves)
    num_evaluations = 0 # counter is reset
    #negamax(gs, valid_moves, DEPTH, color= 1 if gs.white_move else -1)
    negamax_alphabeta(gs, valid_moves, DEPTH, -checkmate_score, checkmate_score, 1 if gs.white_move else -1)
    if best_move is None:
        print("Negamax helper returning no move")
    else: 
        print("Negamax helper returning move: " + best_move.get_notation())
    print("number of evaluations: " + str(num_evaluations))
    return best_move

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


def negamax_alphabeta(gs, valid_moves, depth, alpha, beta, color):
    global best_move
    if depth <= 0 or gs.checkmate or gs.stalemate or gs.threefold_repetition or gs.insufficient_material:
        return color * evaluate_board(gs)

    # move ordering - implement later
    max_eval = float('-inf')
    for move in valid_moves:
        gs.make_move(move, print_move=False)
        next_moves = gs.get_valid_moves()
        eval = -negamax_alphabeta(gs, next_moves, depth-1, -beta, -alpha, -color)
        if eval > max_eval:
            max_eval = eval
            if depth == DEPTH:
                best_move = move
                print("best move is: " + best_move.get_notation())
        gs.undo_move()
        if max_eval > alpha:
            alpha = max_eval
        if alpha >= beta:
            break
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
    for row in gs.board: 
        for piece in row: 
            if piece != "--":
                if piece[0] == 'w':
                    score += piece_values[piece[1]]
                if piece[0] == 'b':
                    score -= piece_values[piece[1]]
    return score        

            

        



