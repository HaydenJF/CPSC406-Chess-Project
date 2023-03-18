import chess
import chess.engine
import chess.svg
import webbrowser


engine = chess.engine.SimpleEngine.popen_uci('/usr/games/stockfish')

board = chess.Board()
if __name__ == "__main__":
    while not board.is_game_over():
        #moves that can be played per turn
        moves = list(board.legal_moves)
        print(board.fen())
        if board.turn == chess.WHITE:
            print("players move")
            print(moves)
            print(len(moves))
            move = input("Enter your move: ")
            board.push_san(move)
        else:
            print("stockfish move")
            print(moves)
            print(len(moves))
            
            result = engine.play(board, chess.engine.Limit(depth=25))
            print(result)
            board.push(result.move)
        board_svg = chess.svg.board(board=board)

        with open("/static/images/board.svg", "w") as f:
            f.write(board_svg)


    print("Game over: ", board.result())

    engine.quit()