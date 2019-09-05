#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 13:49:07 2019

@author: PattyP


This module contains a simple graphical user interface for Othello. 
To run othello:

Try (in a terminal):
        python othello_gui.py

or in spyder: "run othello_gui.py"

This should open a window that generates a board.

To change the dimension of the board, look for the line near the bottom:
   game = OthelloGameManager(dimension=8)

You can change the dimension of the board (e..g, to a smaller board of 4)


Without parameters, the game has 2 human players.  The parameters can be used to indicate opponents.  There is an existing opponent code, randy_ai.py that plays a random player so:

python othello_gui.py randy_ai.py  <- you play against random 
python othello_gui.py randy_ai.py  randy_ai.py <- 2 randoms play against each other

@author: Daniel Bauer 
"""
from tkinter import *
from tkinter import scrolledtext

from othello_game import OthelloGameManager, AiPlayerInterface, Player, InvalidMoveError, AiTimeoutError
from othello_shared import get_possible_moves, get_score

class OthelloGui(object):

    def __init__(self, game_manager, player1, player2):

        self.game = game_manager
        self.players = [None, player1, player2]
        self.height = self.game.dimension
        self.width = self.game.dimension 
        
        self.offset = 3
        self.cell_size = 50

        root = Tk()
        root.wm_title("Othello")
        root.lift()
        root.attributes("-topmost", True)
        self.root = root
        self.canvas = Canvas(root,height = self.cell_size * self.height + self.offset,width = self.cell_size * self.width + self.offset)
        self.move_label = Label(root)
        self.score_label = Label(root)
        self.text = scrolledtext.ScrolledText(root, width=70, height=10)
        self.move_label.pack(side="top")
        self.score_label.pack(side="top")
        self.canvas.pack()
        self.text.pack()
        self.draw_board()

    def get_position(self,x,y):
        i = (x -self.offset) // self.cell_size
        j = (y -self.offset) // self.cell_size
        return i,j

    def mouse_pressed(self,event):
        i,j = self.get_position(event.x, event.y)

        try:
            player = "Dark" if self.game.current_player == 1 else "Light"
            self.log("{}: {},{}".format(player, i,j))
            self.game.play(i, j)
            self.draw_board()
            if not get_possible_moves(self.game.board, self.game.current_player):
                self.shutdown("Game Over")
            elif isinstance(self.players[self.game.current_player], AiPlayerInterface):
                self.root.unbind("<Button-1>")
                self.root.after(100,lambda: self.ai_move())
        except InvalidMoveError:
            self.log("Invalid move. {},{}".format(i,j))

    def shutdown(self, text):
        self.move_label["text"] = text 
        self.root.unbind("<Button-1>")
        if isinstance(self.players[1], AiPlayerInterface): 
            self.players[1].kill(self.game)
        if isinstance(self.players[2], AiPlayerInterface): 
            self.players[2].kill(self.game)
 
    def ai_move(self):
        player_obj = self.players[self.game.current_player]
        try:
            i,j = player_obj.get_move(self.game)
            player = "Dark" if self.game.current_player == 1 else "Light"
            player = "{} {}".format(player_obj.name, player)
            self.log("{}: {},{}".format(player, i,j))
            self.game.play(i,j)
            self.draw_board()
            if not get_possible_moves(self.game.board, self.game.current_player):
                self.shutdown("Game Over")
            elif isinstance(self.players[self.game.current_player], AiPlayerInterface):
                self.root.after(1, lambda: self.ai_move())
            else: 
                self.root.bind("<Button-1>",lambda e: self.mouse_pressed(e))        
        except AiTimeoutError:
            self.shutdown("Game Over, {} lost (timeout)".format(player_obj.name))

    def run(self):
        if isinstance(self.players[1], AiPlayerInterface):
            self.root.after(10, lambda: self.ai_move())
        else: 
            self.root.bind("<Button-1>",lambda e: self.mouse_pressed(e))        
        self.draw_board()
        self.canvas.mainloop()

    def draw_board(self):
        self.draw_grid()
        self.draw_disks()
        player = "Dark" if self.game.current_player == 1 else "Light"
        self.move_label["text"]= player
        self.score_label["text"]= "Dark {} : {} Light".format(*get_score(self.game.board)) 
   
    def log(self, msg, newline = True): 
        self.text.insert("end","{}{}".format(msg, "\n" if newline else ""))
        self.text.see("end")
 
    def draw_grid(self):
        for i in range(self.height):
            for j in range(self.width):
                self.canvas.create_rectangle(i*self.cell_size + self.offset, j*self.cell_size + self.offset, (i+1)*self.cell_size + self.offset, (j+1)*self.cell_size + self.offset, fill="dark green")
       
    def draw_disk(self, i,j, color):
        x = i * self.cell_size + self.offset
        y = j * self.cell_size + self.offset
        padding =2 
        self.canvas.create_oval(x+padding, y+padding, x+self.cell_size-padding, y+self.cell_size-padding, fill=color)
        
    def draw_disks(self):
        for i in range(self.height): 
            for j  in range(self.width): 
                if self.game.board[i][j] == 1:
                    self.draw_disk(j, i, "black")
                elif self.game.board[i][j] == 2:
                    self.draw_disk(j, i, "white")

def main():
    
    if len(sys.argv) == 3:
        p1 = AiPlayerInterface(sys.argv[1],1)
        p2 = AiPlayerInterface(sys.argv[2],2)
    elif len(sys.argv) == 2:
        p1 = Player(1)
        p2 = AiPlayerInterface(sys.argv[1],2)
    else: 
        p1 = Player(1)
        p2 = Player(2)
    game = OthelloGameManager(dimension=8)
    gui = OthelloGui(game, p1, p2) 
    gui.run()

if __name__ == "__main__":
    main()