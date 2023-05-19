import frontend as site
import backend as back
from flask import Flask, render_template, request, redirect, url_for
from flask.views import MethodView

app = Flask("ChessProgram")


app.add_url_rule('/', view_func=site.HomePage.as_view('home_page'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5005)
