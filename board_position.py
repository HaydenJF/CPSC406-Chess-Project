import chess
import chess.engine
import chess.svg
import webbrowser

class Position:
    """
    engine: this is the chess engine, never needs to be dynamically adjusted, basically just connects to stockfish.
    board: think of board as the current position at play.  It also keeps track of whos move it is.
    d: this is the depth.  Currently set to 10.  Currently can't be changed.
    p: this is the position.  Is the stringlike object passed around for non-current boards.
    v: this is stockfish score with extra stuff too.
    children: this is the possible moves a current position
    min_b: this is the minimum b score necessary to be considered a good child move.
    b: this is the special function we are trying to solve for.  Dr. Kurz had a really good description of it https://hackmd.io/@alexhkurz/Hk5sjmHkh  (he called it w).
    score: this just gives the score.
    top_v: the top v scores (set to 4)
    top_b: the top b scores (set to 4)
    """
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
        """finds the children.  Returns the children and their v scores.
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

    
    def set_v(self):
        """
        Caluclates the v (think stockfish) and adds aditional important details to the v.  Returns v and details of v.
        """
        v = self.engine.play(self.board, chess.engine.Limit(depth=self.d))
        return v
    
    def set_b(self, position=None):
        """
        Calculates the current b value (Average of children v score).  Returns sum of values greater than minimum b score.
        """
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
        """
        Returns a list with the children, v score, and b score.
        """
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
        """
        Returns the top 4 v scores and their moves.
        """
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
        """
        Returns the top 4 b scores and their moves.
        """
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
        """
        Updates the svg to the current board position (or to what the player selects on the side.)
        """
        if position is None:
            board = self.board
        else:
            board = chess.Board(position)
        board_svg = chess.svg.board(board=board)
        with open("static/images/board.svg", "w") as f:
            f.write(board_svg)
    
    
    
    def update_board(self, move):
        """
        Updates the board one move.
        """
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
        """
        Updates the board as stockfish would.
        """
        self.update_board(self.v.move.uci())
        
    def set_score(self, position=None):
        """
        Returns the score of the board or current position
        """
        if position is None:
            board = self.board
        else:
            board = chess.Board(position)
        
        result = self.engine.analyse(board, chess.engine.Limit(nodes=self.d))
        

        return (result["score"].relative.score()/100)*self.get_whos_turn(position)
        
        
    def get_everything(self):
        """
        Returns all the variables to Flask
        """
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
        """
        Gets if its black or white pieces move
        """
        if position is None:
            board = self.board
        else:
            board = chess.Board(position)
            
        if board.turn:
            return 1
        return -1
    
    def possible_move(self, position=None):
        """
        Returns the possible moves the position can have next.
        """
        if position is None:
            board = self.board
        else:
            board = chess.Board(position)
            
        moves = list(board.legal_moves)
        string_moves = []
        for i in moves:

            string_moves.append(i.uci())
        return string_moves
    
    
            
        
        
    
    

