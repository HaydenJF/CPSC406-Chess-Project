import chess
import chess.engine
import chess.svg
import webbrowser

class position:
    
    
    
    def __init__(self, position='', depth=25, engine = chess.engine.SimpleEngine.popen_uci('/usr/games/stockfish'), board = chess.Board()):
        self.engine = engine
        self.board = board
        self.d = depth
        self.children = None


        self.p = position
        self.v = self.set_v()
        self.b = None
        
        
    
    def set_children(self):
        """_summary_
        """
        moves = list(self.board.legal_moves)
        scores = []
        for move in moves:
            self.board.push(move)
            result = self.engine.analyse(self.board, chess.engine.Limit(nodes=self.d))
            scores.append(result["score"].relative.score())
            self.board.pop()
        return scores

# Sort moves by score and get top 10
sorted_moves = sorted(zip(moves, scores), key=lambda x: x[1], reverse=True)[:10]



    
    def set_v(self):
        v = self.engine.play(self.board, chess.engine.Limit(depth=self.d)
        return v
    
    def set_b(self):
        """_summary_
        """
        return
    
    def get_v(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.v
    
    def get_b(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.b
    
    


'''while not board.is_game_over():
        #moves that can be played per turn
        moves = list(board.legal_moves)
        print(moves)
        print(len(moves))
        if board.turn == chess.WHITE:
            move = input("Enter your move: ")
            board.push_san(move)
        else:
            result = engine.play(board, chess.engine.Limit(time=2.0))
            print(result)
            board.push(result.move)
        board_svg = chess.svg.board(board=board)

        with open("/static/images/board.svg", "w") as f:
            f.write(board_svg)
'''
'''# Calculate evaluation score for each move
scores = []
for move in moves:
    board.push(move)
    result = engine.analyse(board, chess.engine.Limit(time=2.0))
    scores.append(result["score"].relative.score())
    board.pop()

# Sort moves by score and get top 10
sorted_moves = sorted(zip(moves, scores), key=lambda x: x[1], reverse=True)[:10]
'''