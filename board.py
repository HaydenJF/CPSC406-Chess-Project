import chess
import chess.engine
import chess.svg
import webbrowser

from board_position import Position

class Board:
    def __init__(self):
        self.board = []
    
    def add_position(self, info):
        self.board.append((info, len(self.board)))
        
    def give_list(self, position_number=None):
        if position_number == None:
            return self.board[-1][0]
        print("here")
        return self.board[int(position_number)][0]
        