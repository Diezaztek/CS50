"""
Tic Tac Toe Player
"""

import math
import copy

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
    number_of_x = len([cell for row in board for cell in row if cell == X])
    number_of_o = len([cell for row in board for cell in row if cell == O])
    
    if number_of_x == number_of_o:
        return X # As in an initial game the X's starts
    else:
        return O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i,j))
    
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    possible_actions = actions(board)
    
    if action in possible_actions:
        resulting_board = copy.deepcopy(board)
        row = action[0]
        column = action[1]
        resulting_board[row][column] = player(board)
        return resulting_board
    else:
        raise Exception("Invalid move")


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if board[0][0] == board[0][1] == board[0][2]:
        return board[0][0]
    elif board[1][0] == board[1][1] == board[1][2]:
        return board[1][0]
    elif board[2][0] == board[2][1] == board[2][2]:
        return board[2][0]
    elif board[0][0] == board[1][0] == board[2][0]:
        return board[0][0]
    elif board[0][1] == board[1][1] == board[2][1]:
        return board[0][1]
    elif board[0][2] == board[1][2] == board[2][2]:
        return board[0][2]
    elif board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    elif board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]
    else:
        return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if not winner(board) is None:
        return True
    
    cells_with_values = [cell for row in board for cell in row if cell != EMPTY]
    
    if(len(cells_with_values) < 9):
        return False
    else:
        return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner_player = winner(board)
    
    if winner_player == "X":
        return 1
    elif winner_player == "O":
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    return calculate_best_move(board)[1]
                

            

def calculate_best_move(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return (utility(board), ())
    
    current_turn = player(board)
    if current_turn == X:
        max_score = -1
        best_move = ()
        for possible_move in actions(board):
            current_move = possible_move
            next_turn = calculate_best_move(result(board, possible_move))
            
            #Debugging
            '''final_board = result(board, possible_move)
            print(utility(final_board))
            print(final_board)'''
            
            if next_turn[0] > max_score:
                max_score = next_turn[0]
                best_move = current_move
        return (max_score, best_move)
    
    elif current_turn == O:
        min_score = 1
        best_move = ()
        for possible_move in actions(board):
            current_move = possible_move
            next_turn = calculate_best_move(result(board, possible_move))
            
            #Debugging
            '''final_board = result(board, possible_move)
            print(utility(final_board))
            print(final_board)'''
            
            if next_turn[0] < min_score:
                min_score = next_turn[0]
                best_move = current_move
        return (min_score, best_move) 