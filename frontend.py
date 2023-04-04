from flask import Flask, render_template, request, redirect, url_for
from flask.views import MethodView
from board_position import Position


p = Position()



class HomePage(MethodView):
    def get(self):
        list = p.get_everything()
        print(list["top_v"])
        return render_template("index.html", list=list)
    
    def post(self):
        data = request.form
        if "player-button" in data:
            if data['input-field'] != '':
                if data["input-field"] in p.possible_move():
                    p.update_board(data['input-field'])
        elif "stockfish-button" in data:
            p.stockfish_update_board()
        elif "board_position_button" in data:
            p.update_svg(data["board_position_button"])
        list = p.get_everything()


        #print(list["list_moves"])

        return render_template("index.html", list=list)


