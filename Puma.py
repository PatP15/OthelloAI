#!/usr/bin/env python3
# -*- coding: utf-8 -*

"""
An AI player for Othello. This is the template file that you need to  
complete and submit for the competition. 

@author: YOUR NAME
"""

import random
import sys
import time
import math
# You can use the functions in othello_shared to write your AI 
from othello_shared import find_lines, get_possible_moves, get_score, play_move

def compute_utility(board, color):
    return 0

def check_space(board, player, i, j):
    new_board = play_move(board, player, i, j)
    if new_board == board: #the piece is already there
        return True
    else:
        return False#the piece is not there

############ MINIMAX ###############################

def minimax_min_node(board, color, depth, alpha, beta, start_time):
    new_board = board
    cur_min = math.inf
    moves = get_possible_moves(board, color)
    end = time.time()
    if len(moves) == 0 or depth == 0 or end - start_time> 4.9:
        return (-1,-1), evaluate_board(board, color)
    else: 
        for i in moves:
            new_board = play_move(board, color, i[0], i[1])
            if color == 1:
                next_player = 2
            else:
                next_player = 1
            new_move, new_score = minimax_max_node(new_board, next_player, depth - 1, alpha, beta, start_time)
            if new_score < cur_min:
                cur_min = new_score
                best_move = i
            beta = min(new_score, beta) 
            if beta <= alpha:
                break
        return best_move, cur_min 

def evaluate_board(board, color):

    cur_score=get_score(board)
    if color == 1:
        score = cur_score[0] - cur_score[1] #switch depending on who goes first 1,0 is when AI goes second 
    
        #if the AI goes first
        #corners
        if check_space(board, 1, 7, 0):
            score +=1000
        if check_space(board, 1, 7, 7):
            score +=1000
        if check_space(board, 1, 0, 0):
            score +=1000
        if check_space(board, 1, 0, 7):
            score +=1000
        #the corners 2taken by teh opponent 
        if check_space(board, 2, 7, 0):
            score -=1225
        if check_space(board, 2, 7, 7):
            score -=1225
        if check_space(board, 2, 0, 0):
            score -=1225
        if check_space(board, 2, 0, 7):
            score -=1225
        
        #the area around the corner 
        if check_space(board, 1, 1,0):
            score -=25
        if check_space(board, 1, 1,1):
            score -=25
        if check_space(board, 1, 0, 1):
            score -=25
        if check_space(board, 1, 0,6):
            score -=25
        if check_space(board, 1, 1,6):
            score-=25
        if check_space(board, 1, 1, 7):
            score -=25
        if check_space(board, 1, 6,6): 
            score -=25
        if check_space(board, 1, 7,6):
            score-=25
        if check_space(board, 1, 6, 7):
            score -=25
        if check_space(board, 1, 6,0): 
            score -=25
        if check_space(board, 1, 6,1):
            score-=25
        if check_space(board, 1, 7, 1):
            score-=25
            
        #the edges
        
        if check_space(board, 1, 3, 0):
            score +=25
        if check_space(board, 1, 4, 0):
            score +=25
        
        
        if check_space(board, 1, 0, 3):
            score +=25
        if check_space(board, 1, 0, 4):
            score +=25
    
        if check_space(board, 1, 3, 7):
            score +=25
        if check_space(board, 1, 4, 7):
            score +=25
        
        
        if check_space(board, 1, 7, 3):
            score +=25
        if check_space(board, 1, 7, 4):
            score +=25
        
        #more good moves
        if check_space(board, 1, 2, 0):
            score +=25
        if check_space(board, 1, 2, 1):
            score +=25
        if check_space(board, 1, 2, 2):
            score +=25
        if check_space(board, 1, 1, 2):
            score +=25
        if check_space(board, 1, 0, 2):
            score +=25
        if check_space(board, 1, 0, 5):
            score +=25
        if check_space(board, 1, 1, 5):
            score +=25
        if check_space(board, 1, 2, 5):
            score +=25
        if check_space(board, 1, 2, 6):
            score +=25
        if check_space(board, 1, 2, 7):
            score +=25
        if check_space(board, 1, 5, 7):
            score +=25
        if check_space(board, 1, 5, 6):
            score +=25
        if check_space(board, 1, 5, 5):
            score +=25
        if check_space(board, 1, 6, 5):
            score +=25
        if check_space(board, 1, 7, 5):
            score +=25
        if check_space(board, 1, 7, 2):
            score +=25
        if check_space(board, 1, 6, 2):
            score +=25
        if check_space(board, 1, 5, 2):
            score +=25
        if check_space(board, 1, 5, 1):
            score +=25
        if check_space(board, 1, 5, 0):
            score +=25
    if color == 2:
        score = cur_score[1] - cur_score[0] #switch depending on who goes first 1,0 is when AI goes second 
        #if the AI goes first
        #corners
        if check_space(board, 2, 7, 0):
            score +=1000
        if check_space(board, 2, 7, 7):
            score +=1000
        if check_space(board, 2, 0, 0):
            score +=1000
        if check_space(board, 2, 0, 7):
            score +=1000
        #the corners 2taken by teh opponent 
        if check_space(board, 1, 7, 0):
            score -=1225
        if check_space(board, 1, 7, 7):
            score -=1225
        if check_space(board, 1, 0, 0):
            score -=1225
        if check_space(board, 1, 0, 7):
            score -=1225
        
        #the area around the corner 
        if check_space(board, 2, 1,0):
            score -=25
        if check_space(board, 2, 1,1):
            score -=25
        if check_space(board, 2, 0, 1):
            score -=25
        if check_space(board, 2, 0,6):
            score -=25
        if check_space(board, 2, 1,6):
            score-=25
        if check_space(board, 2, 1, 7):
            score -=25
        if check_space(board, 2, 6,6): 
            score -=25
        if check_space(board, 2, 7,6):
            score-=25
        if check_space(board, 2, 6, 7):
            score -=25
        if check_space(board, 2, 6,0): 
            score -=25
        if check_space(board, 2, 6,1):
            score-=25
        if check_space(board, 2, 7, 1):
            score-=25
            
        #the edges
        
        if check_space(board, 2, 3, 0):
            score +=25
        if check_space(board, 2, 4, 0):
            score +=25
    
        
        if check_space(board, 2, 0, 3):
            score +=25
        if check_space(board, 2, 0, 4):
            score +=25
        if check_space(board, 2, 3, 7):
            score +=25
        if check_space(board, 2, 4, 7):
            score +=25
        
        if check_space(board, 2, 7, 3):
            score +=25
        if check_space(board, 2, 7, 4):
            score +=25
        

        #more good moves
        if check_space(board, 2, 2, 0):
            score +=25
        if check_space(board, 2, 2, 1):
            score +=25
        if check_space(board, 2, 2, 2):
            score +=25
        if check_space(board, 2, 1, 2):
            score +=25
        if check_space(board, 2, 0, 2):
            score +=25
        if check_space(board, 2, 0, 5):
            score +=25
        if check_space(board, 2, 1, 5):
            score +=25
        if check_space(board, 2, 2, 5):
            score +=25
        if check_space(board, 2, 2, 6):
            score +=25
        if check_space(board, 2, 2, 7):
            score +=25
        if check_space(board, 2, 5, 7):
            score +=25
        if check_space(board, 2, 5, 6):
            score +=25
        if check_space(board, 2, 5, 5):
            score +=25
        if check_space(board, 2, 6, 5):
            score +=25
        if check_space(board, 2, 7, 5):
            score +=25
        if check_space(board, 2, 7, 2):
            score +=25
        if check_space(board, 2, 6, 2):
            score +=25
        if check_space(board, 2, 5, 2):
            score +=25
        if check_space(board, 2, 5, 1):
            score +=25
        if check_space(board, 2, 5, 0):
            score +=25

    return score

def minimax_max_node(board, color, depth, alpha, beta, start_time):
    end = time.time()
    cur_max = -math.inf
    new_board = board
    moves = get_possible_moves(board, color)
    if len(moves) == 0 or depth == 0 or end - start_time> 4.9:
        return (-1,-1), evaluate_board(board, color)
    else: 
        for i in moves:
            new_board = play_move(board, color, i[0], i[1])
            if color == 1:
                next_player = 2
            else:
                next_player = 1
            new_move, new_score = minimax_min_node(new_board, next_player, depth - 1, alpha, beta, start_time)
            if new_score > cur_max:
                cur_max = new_score
                best_move = i
            alpha = max(new_score, alpha) 
            if beta <= alpha:
                break
        return best_move, cur_max

    
def select_move_minimax(board, color):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  
    """
    start = time.time()
    best_move, score = minimax_max_node(board, color, 4, -math.inf, math.inf, start )
    i, j = best_move[0], best_move[1]

    return i,j, score

"""
############ ALPHA-BETA PRUNING #####################

#alphabeta_min_node(board, color, alpha, beta, level, limit)
def alphabeta_min_node(board, color, alpha, beta): 
    return None


#alphabeta_max_node(board, color, alpha, beta, level, limit)
def alphabeta_max_node(board, color, alpha, beta):
    return None


def select_move_alphabeta(board, color): 
    return 0,0 


####################################################
"""
def run_ai():
    """
    This function establishes communication with the game manager. 
    It first introduces itself and receives its color. 
    Then it repeatedly receives the current score and current board state
    until the game is over. 
    """

    print("Artificial Stupidity") # First line is the name of this AI  
    color = int(input()) # Then we read the color: 1 for dark (goes first), 
                         # 2 for light. 

    while True: # This is the main loop 
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input() 
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over. 
            print 
        else: 
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The 
                                  # squares in each row are represented by 
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)
                    
            # Select the move and send it to the manager 
            movei, movej, score = select_move_minimax(board, color)
            #movei, movej = select_move_alphabeta(board, color)
            print("{} {}".format(movei, movej))


if __name__ == "__main__":
    run_ai()