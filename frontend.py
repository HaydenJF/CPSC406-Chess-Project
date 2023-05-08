from flask import Flask, render_template, request, redirect, url_for
from flask.views import MethodView
from board_position import Position
from board import Board


p = Position()
b = Board()


class HomePage(MethodView):
    def get(self):
        list = p.get_everything()
        print(list["top_v"])
        print(list["top_b"])
        print(list['list_moves'])
        b.add_position(list)
        return render_template("index.html", list=b.give_list())
    
    def post(self):
        data = request.form
        if "player-button" in data:
            if data['input-field'] != '':
                if data["input-field"] in p.possible_move():
                    p.update_board(data['input-field'])
                    list = p.get_everything()
                    b.add_position(list)
                    return render_template("index.html", list=b.give_list())
        elif "stockfish-button" in data:
            p.stockfish_update_board()
            list = p.get_everything()
            b.add_position(list)
            return render_template("index.html", list=b.give_list())
        elif "board_position_button" in data:
            print(data["board_position_button"])
            svg_list = b.give_list(data["board_position_button"])
            p.update_svg(svg_list["list_moves"][int(data["board_position_button"])][1])
            p.update_other_svg(svg_list["top_v"], svg_list["top_b"])
            return render_template("index.html", list=svg_list)


        return render_template("index.html", list=b.give_list())


