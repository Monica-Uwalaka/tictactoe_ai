"""
Tic Tac Toe Player
"""

from copy import deepcopy
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = 0
    o_count = 0
    
    for row in board:
        for col in row:
            if col == X:
                x_count += 1
            elif col == O:
                o_count += 1

    # return player with the lower count
    if x_count > o_count:
        return O
    elif x_count < o_count:
        return X
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()

    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == EMPTY:
                possible_actions.add((i,j))
    if possible_actions:
        return possible_actions
    
    # return any action is the board is full
    possible_actions.add((0,0))
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = deepcopy(board)
    i = action[0]
    j = action[1]
    valid = {0, 1, 2}

    if not ((i in valid) and (j in valid)):
        raise IndexError
    
    if board[i][j] == EMPTY:
        next_player = player(board)
        new_board[i][j] = next_player
    
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    wins = (
        [(0, 0), (0, 1), (0, 2)], # Horizontal
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
        [(0, 0), (1, 0), (2, 0)], # Vertical
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
        [(0, 0), (1, 1), (2, 2)], # Diagonal
        [(0, 2), (1, 1), (2, 0)],
    )

    for moves in wins:
        row = [board[i][j] for i,j in moves]
        if len(set(row)) == 1:
            return row[0]
    return None



def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    game_is_over = True
    empty_cells = 0
    
    #the game end if there is a winner
    if winner(board):
        return game_is_over

    for _, row in enumerate(board):
        for _, cell in enumerate(row):
            if cell == EMPTY:
                empty_cells += 1

    #the game ends if the board is full      
    if 0 < empty_cells <= 9:
        return not game_is_over
    else:
        return game_is_over

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    player = winner(board)
    
    if player:
        if player == X:
            return 1
        if player == O:
            return -1
    return 0

def min_value(board):
    """ 
    Find the minimum value for all possible actions
    """
    if terminal(board):
        return utility(board)
    
    value = math.inf
    possible_actions = actions(board)
    for action in possible_actions:
            value = min(value, max_value(result(board, action))) 
    return value

def max_value(board):
    """
    Find tha maximum value from all possible actions 
    """
    if terminal(board):
        return utility(board)
    
    value = -math.inf
    possible_actions = actions(board)
    for action in possible_actions:
            value = max(value, min_value(result(board, action))) 
    return value


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # find whose turn it is and get all the possible ations 
    next_player = player(board)
    possible_actions = actions(board)

    # X player aims to maximize the score
    if next_player == X:
        action_value = [None, -math.inf]
        for action in possible_actions:
            # O player tries to minimize the value after X takes this action
            value = min_value(result(board, action))
            if value > action_value[1]:
                action_value[0], action_value[1] = action, value

        return action_value[0]

    # O player aims to minimize the score
    if next_player == O:
        action_value = [None, math.inf]
        for action in possible_actions:
            # X player tries to maximize the value after O takes this action
            value = max_value(result(board, action))
            if value < action_value[1]:
                action_value[0], action_value[1] = action, value
        
        return action_value[0]


        

    