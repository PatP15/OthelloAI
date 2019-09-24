#!/usr/bin/env python3
# -*- coding: utf-8 -*

import random
import sys
import time

"""Built by Nathan Smith"""

# You can use the functions in othello_shared to write your AI
from othello_shared import find_lines, get_possible_moves, play_move


# This Part goes in the othello_shared.py document
def isCorner(board, x, y):
    corner_locations = [(0, 0), (len(board) - 1, len(board) - 1), (0, len(board) - 1), (len(board) - 1, 0)]
    if (x, y) in corner_locations:
        return True


def isInvincible(board, color, x, y, direction):
    if isCorner(board, x, y):
        return True

    elif x == len(board) - 1 or x == 0:
        if direction == 0 or direction == -1:
            if board[y - 1][x] == color:
                is_invincible = isInvincible(board, color, x, y - 1, -1)
                if is_invincible == True:
                    return is_invincible

        if direction == 0 or direction == 1:
            if board[y + 1][x] == color:
                return isInvincible(board, color, x, y + 1, 1)

    elif y == len(board) - 1 or y == 0:

        if direction == 0 or direction == -1:
            if board[y][x - 1] == color:
                is_invincible = isInvincible(board, color, x - 1, y, -1)
                if is_invincible == True:
                    return is_invincible

        if direction == 0 or direction == 1:
            if board[y][x + 1] == color:
                return isInvincible(board, color, x + 1, y, 0)

    return False


def get_heuristic_score(board):
    p1_count = 0
    p2_count = 0
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 1:
                if isInvincible(board, 1, j, i, 0):
                    p1_count += 1000
                else:
                    p1_count += 1
            elif board[i][j] == 2:
                if isInvincible(board, 2, j, i, 0):
                    p2_count += 1000
                else:
                    p2_count += 1
    return p1_count, p2_count


def compute_utility(board, color):
    p1_score, p2_score = get_heuristic_score(board)
    score_heuristic = p1_score - p2_score if color == 1 else p2_score - p1_score

    return score_heuristic


move_dictionary = dict()

############ MINIMAX ###############################

def minimax_max_node(board, color, depth):
    possible_moves = get_possible_moves(board, color)
    move_states = {move: play_move(board, color, move[0], move[1]) for move in possible_moves}
    best_move = None
    best_value = None

    if len(possible_moves) > 0:
        if depth == 1:
            for move, state in move_states.items():
                if best_move == None or minimax_min_node(state, color, depth + 1) > best_value:
                    best_move = move
                    best_value = minimax_min_node(state, color, depth + 1)

            return best_move

        else:
            for move, state in move_states.items():

                if best_move == None or minimax_min_node(state, color, depth + 1) > best_value:
                    best_value = minimax_min_node(state, color, depth + 1)

            return best_value
    return compute_utility(board, color)


def minimax_min_node(board, color, depth):
    other_color = 1 if color == 2 else 2
    possible_moves = get_possible_moves(board, other_color)
    move_states = {move: play_move(board, other_color, move[0], move[1]) for move in possible_moves}
    best_move = None
    best_value = None

    if len(possible_moves) > 0:
        if depth <= 3:
            for move, state in move_states.items():

                if best_move == None or minimax_max_node(state, color, depth + 1) < best_value:
                    best_move = move
                    best_value = minimax_max_node(state, color, depth + 1)

            return best_value

        else:
            for move, state in move_states.items():

                if best_value == None or compute_utility(state, color) < best_value:
                    best_value = compute_utility(state, color)

            return best_value
    return compute_utility(board, color)


def select_move_minimax(board, color):
    """
    Given a board and a player color, decide on a move.
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.
    """

    return minimax_max_node(board, color, 1)


############ ALPHA-BETA PRUNING #####################

# alphabeta_min_node(board, color, alpha, beta, level, limit)
def alphabeta_min_node(board, color, alpha, beta, level, limit):
    if board in move_dictionary:
        return move_dictionary[board]       # Retrieval from cached board states
    else:
        min_next_nodes = get_possible_moves(board, 3-color)
        utility_list = []
        if(len(min_next_nodes) == 0 or limit <= level):
            return compute_utility(board, color)            # Leaf node reached

        v = float("inf")
        successor_dict = dict()
        for items in min_next_nodes:
            successor_board = play_move(board, 3-color, items[0], items[1])
            successor_dict.update({successor_board: compute_utility(successor_board,color)})

        #alpha-beta pruning logic - with node ordering heuristic
        for key in sorted(successor_dict, key=successor_dict.get):
            v = min(v, alphabeta_max_node(successor_board, color, alpha, beta, level+1, limit))
            if v <= alpha:
                return v
            beta = min(beta,v)

        move_dictionary.update({board : v})    #Caching of the board states
        return v


#alphabeta_max_node(board, color, alpha, beta, level, limit)
def alphabeta_max_node(board, color, alpha, beta, level, limit):
    if board in move_dictionary:
        return move_dictionary[board]       # Retrieval from cached board states
    else:
        max_next_nodes = get_possible_moves(board, color)

        utility_list = []
        if(len(max_next_nodes) == 0 or limit <= level):
            return compute_utility(board, color)            # Leaf node reached

        v = float("-inf")
        next_dict = dict()
        for items in max_next_nodes:
            successor_board = play_move(board, color, items[0], items[1])
            next_dict.update({successor_board:compute_utility(successor_board,color)})

        #alpha-beta pruning logic - with node ordering heuristic
        for key in sorted(next_dict, key=next_dict.get):
            v = max(v, alphabeta_min_node(key, color, alpha, beta, level+1, limit))
            if v >= beta:
                return v
            alpha = max(alpha,v)

        move_dictionary.update({board : v})     #Caching of the board states
        return v


def select_move_alphabeta(board, color):
    possible_moves = get_possible_moves(board, color)
    action_list = []
    for items in possible_moves:
        successor_board = play_move(board, color, items[0], items[1])
        # The max depth limit reached within 10 seconds - 7
        action =  alphabeta_max_node(successor_board, color, float("-inf"), float("inf"), 0, 7)
        action_list.append(action)

    max_index = action_list.index(max(action_list))
    return possible_moves[max_index][0], possible_moves[max_index][1]


####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("Bad AI")  # First line is the name of this AI
    color = int(input())  # Then we read the color: 1 for dark (goes first),
    # 2 for light.

    while True:  # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL":  # Game is over.
            print()
        else:
            board = eval(input())  # Read in the input and turn it into a Python
            # object. The format is a list of rows. The
            # squares in each row are represented by
            # 0 : empty square
            # 1 : dark disk (player 1)
            # 2 : light disk (player 2)

            # Select the move and send it to the manager
            movei, movej = select_move_minimax(board, color)
            # movei, movej = select_move_alphabeta(board, color)
            print("{} {}".format(movei, movej))


if __name__ == "__main__":
    run_ai()