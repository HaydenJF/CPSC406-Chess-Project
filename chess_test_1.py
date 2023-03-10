import chess
import chess.engine
import chess.svg
import webbrowser


engine = chess.engine.SimpleEngine.popen_uci('/usr/games/stockfish')

board = chess.Board()

while not board.is_game_over():
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

    with open("board.svg", "w") as f:
        f.write(board_svg)

    webbrowser.open("board.svg")

print("Game over: ", board.result())

engine.quit()