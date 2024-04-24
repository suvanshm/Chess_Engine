import numpy as np
from Chess import ChessEngine

def test_is_insufficient_material():
    # Create a ChessEngine instance
    engine = ChessEngine.GameState()

    # Test case 1: Only kings left on the board
    engine.board = np.array([["--"] * 8] * 8)
    engine.board[0][0] = "wK"
    engine.board[7][7] = "bK"
    assert engine.is_insufficient_material() == True

    # Test case 2: King and knight vs king
    engine.board = np.array([["--"] * 8] * 8)
    engine.board[0][0] = "wK"
    engine.board[0][1] = "wN"
    engine.board[7][7] = "bK"
    assert engine.is_insufficient_material() == True

    # Test case 3: King and bishop vs king and bishop (same color squares)
    engine.board = np.array([["--"] * 8] * 8)
    engine.board[0][0] = "wK"
    engine.board[0][1] = "wB"
    engine.board[7][7] = "bK"
    engine.board[7][6] = "bB"
    assert engine.is_insufficient_material() == True

    # Test case 4: King and bishop vs king and bishop (different color squares)
    engine.board = np.array([["--"] * 8] * 8)
    engine.board[0][0] = "wK"
    engine.board[0][1] = "wB"
    engine.board[7][7] = "bK"
    engine.board[7][5] = "bB"
    assert engine.is_insufficient_material() == False

    # Test case 5: King and queen vs king
    engine.board = np.array([["--"] * 8] * 8)
    engine.board[0][0] = "wK"
    engine.board[0][1] = "wQ"
    engine.board[7][7] = "bK"
    assert engine.is_insufficient_material() == False

    print("All test cases passed")

# Run the test function
test_is_insufficient_material()