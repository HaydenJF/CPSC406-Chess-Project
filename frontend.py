from flask import Flask, render_template, request, redirect, url_for
from flask.views import MethodView
from board_position import Position


p = Position()



class HomePage(MethodView):
    def get(self):
        
        return render_template("index.html")
    
    def post(self):
        data = request.form
        print(data)
        if "player-button" in data:
            if data['input-field'] != '':
                p.update_board(data['input-field'])
        elif "stockfish-button" in data:
            p.stockfish_update_board()
        print(data)
        
        return render_template("index.html")


