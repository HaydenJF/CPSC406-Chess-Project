import frontend as site
from flask import Flask, render_template, request, redirect, url_for
from flask.views import MethodView

app = Flask("ChessProgram")


app.add_url_rule('/', view_func=site.HomePage.as_view('home_page'))

if __name__ == "__main__":
    app.run(debug=True, port=5005)
