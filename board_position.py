import chess
import chess.engine
import chess.svg
import webbrowser

class Position:
    
    
    
    def __init__(self, position='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', depth=10, engine = chess.engine.SimpleEngine.popen_uci('/usr/games/stockfish')):
        self.engine = engine
        self.board  = chess.Board(position)
        self.d = depth
        self.children = self.set_children()
        self.update_svg()
        self.p = position
        self.v = self.set_v()
        #self.b = self.set_b()
        
        self.list_moves = []
        
        
    
    def set_children(self):
        """_summary_
        """
        moves = list(self.board.legal_moves)
        scores = []
        for move in moves:
            self.board.push(move)
            result = self.engine.analyse(self.board, chess.engine.Limit(nodes=self.d))
            self.next_board = result
            scores.append([result["score"].relative.score()/100, result["pv"], self.board.fen()])
            self.board.pop()
        return scores

# Sort moves by score and get top 10
#sorted_moves = sorted(zip(moves, scores), key=lambda x: x[1], reverse=True)[:10]

    
    def set_v(self):
        v = self.engine.play(self.board, chess.engine.Limit(depth=self.d))
        return v
    
    def set_b(self):
        """_summary_
        """
        
        return
    
    def update_svg(self):
        board_svg = chess.svg.board(board=self.board)
        with open("static/images/board.svg", "w") as f:
            f.write(board_svg)
    
    
    
    def update_board(self, move):
        self.board.push_san(move)
        self.p = self.board.fen()
        self.v = self.set_v()
        self.children = self.set_children()
        self.update_svg()
        self.list_moves.append((move,self.board.fen()))
        
    def stockfish_update_board(self):
        result = self.engine.play(self.board, chess.engine.Limit(depth=self.d))
        print(result)
        print(result.move)
        print(type(result.move))
        self.update_board(result.move.uci())
        
        
    
    


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