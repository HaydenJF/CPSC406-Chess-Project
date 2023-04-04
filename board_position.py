import chess
import chess.engine
import chess.svg
import webbrowser

class Position:
    
    def __init__(self, position='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', depth=10, engine = chess.engine.SimpleEngine.popen_uci('./stockfish'), minimum_b=0):
        self.engine = engine
        self.board  = chess.Board(position)
        self.d = depth
        self.p = position
        self.v = self.set_v()
        
        self.children = self.set_children()
        self.update_svg()
        
        self.min_b = minimum_b
        self.b = self.set_b()
        self.score = self.set_score()
        
        self.top_v = self.get_top_v()
        self.top_b = self.get_top_b()
  
        self.list_moves = [("Starting Board", self.p)]
        
        
    
    def set_children(self, position=None):
        """_summary_
        """
        if position is None:
            board = self.board
        else:
            board = chess.Board(position)
            
        moves = list(board.legal_moves)
        scores = []
        temp_board = board
        for move in moves:
            temp_board.push(move)
            result = self.engine.analyse(temp_board, chess.engine.Limit(nodes=self.d))
            if result["score"].relative.score() is not None:
                scores.append([(result["score"].relative.score()/100)*self.get_whos_turn(temp_board.fen()), move.uci(), temp_board.fen()])
            temp_board.pop()
        
        return scores

# Sort moves by score and get top 10
#sorted_moves = sorted(zip(moves, scores), key=lambda x: x[1], reverse=True)[:10]

    
    def set_v(self):
        v = self.engine.play(self.board, chess.engine.Limit(depth=self.d))
        return v
    
    def set_b(self, position=None):
        if position is None:
            board = self.board
        else:
            board = chess.Board(position)
            
        temp_children = self.set_children(position=position)
        b_count = 0;
        
        for i in temp_children:
            if i[0]*self.get_whos_turn(position) > self.min_b:
                b_count += 1
        
        return b_count
    
    def get_children_with_b(self, position=None):
        if position is None:
            board = self.board
        else:
            board = chess.Board(position)
        
        p_position = board.fen()
        temp_children = self.set_children(position=p_position)
        children_with_b = []
        for i in temp_children:
            temp_board = chess.Board(i[2])
            temp_b = self.set_b(temp_board.fen())
            children_with_b.append([i[0], i[1], i[2], temp_b])
        
        return children_with_b
            
    def get_top_v(self, position=None, count=4):
        if position is None:
            board = self.board
        else:
            board = chess.Board(position)
        children = self.set_children(position=board.fen())
        if self.get_whos_turn(position=board.fen()) == 1:
            sorted_children = sorted(children, key=lambda x: x[0], reverse=True)
        else:
            sorted_children = sorted(children, key=lambda x: x[0])
        list_send = []
        for i in range(count):
            list_send.append((sorted_children[i][0], sorted_children[i][1]))
            board_svg = chess.svg.board(board=chess.Board(sorted_children[i][2]))
            file_path = "static/images/topV/board{}.svg".format(i+1)
            with open(file_path, "w") as f:
                f.write(board_svg)   
        return list_send
        

    def get_top_b(self, position=None, count=4):
        if position is None:
            board = self.board
        else:
            board = chess.Board(position)
        children = self.get_children_with_b(position=board.fen())
        sorted_children = sorted(children, key=lambda x: x[3], reverse=True)
        list_send = []
        for i in range(count):
            list_send.append((sorted_children[i][3], sorted_children[i][1]))
            board_svg = chess.svg.board(board=chess.Board(sorted_children[i][2]))
            file_path = "static/images/topB/board{}.svg".format(i+1)
            with open(file_path, "w") as f:
                f.write(board_svg)
        return list_send
               
            
        
    def update_svg(self, position=None):
        if position is None:
            board = self.board
        else:
            board = chess.Board(position)
        board_svg = chess.svg.board(board=board)
        with open("static/images/board.svg", "w") as f:
            f.write(board_svg)
    
    
    
    def update_board(self, move):
        #engine
        self.board.push_san(move)
        #d
        self.p = self.board.fen()
        self.v = self.set_v()
        
        self.children = self.set_children()
        self.update_svg()
        
        self.b = self.set_b()
        self.score = self.set_score()
        
        self.top_v = self.get_top_v()
        self.top_b = self.get_top_b()
        
        self.list_moves.append((move,self.board.fen()))
        
    def stockfish_update_board(self):
        self.update_board(self.v.move.uci())
        
    def set_score(self, position=None):
        if position is None:
            board = self.board
        else:
            board = chess.Board(position)
        
        result = self.engine.analyse(board, chess.engine.Limit(nodes=self.d))
        

        return (result["score"].relative.score()/100)*self.get_whos_turn(position)
        
        
    def get_everything(self):
        list = {}
        list["d"] = self.d
        list["v"] = self.v
        list["v_string"] = self.v.move.uci()
        list["b"] = self.b
        list["children"] = self.children
        list["p"] = self.p
        list["score"] = self.score
        list["top_v"] = self.top_v
        list["top_b"] = self.top_b
        list["list_moves"] = self.list_moves
        
        return list
    
    def get_whos_turn(self, position=None):
        if position is None:
            board = self.board
        else:
            board = chess.Board(position)
            
        if board.turn:
            return 1
        return -1
    
    def possible_move(self, position=None):
        if position is None:
            board = self.board
        else:
            board = chess.Board(position)
            
        moves = list(board.legal_moves)
        string_moves = []
        for i in moves:

            string_moves.append(i.uci())
        return string_moves
    
    
            
        
        
    
    


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