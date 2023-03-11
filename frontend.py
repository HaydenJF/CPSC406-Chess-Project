from flask import Flask, render_template, request, redirect, url_for
from flask.views import MethodView




class HomePage(MethodView):
    def get(self):
        return render_template("index.html")

