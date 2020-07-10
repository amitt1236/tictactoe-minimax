from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp
import copy
import math

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():

    if "board" not in session:
        session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
        session["turn"] = "X"
    if draw(session["board"]) == True:
        return render_template("gameover.html", game=session["board"], draw=draw)
    if winner(session["board"]) is not None:
        return render_template("gameover.html", game=session["board"], winner=winner(session["board"]))

    return render_template("game.html", game=session["board"], turn=session["turn"])

@app.route("/reset")
def reset():
    session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
    session["turn"] = "X"
    return redirect(url_for("index"))

@app.route("/play/<int:row>/<int:col>")
def play(row, col):
    session["board"][row][col] = session["turn"]
    if session["turn"] == "X":
        session["turn"] = "O"
    else:
        session["turn"] = "X"   
    return redirect(url_for("index"))

def winner(board):
    # check colums
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != None:
            return board[i][0]
    # check rows
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != None:
            return board[0][i]
    # check diagonal
    if board[0][0] == board[1][1] == board[2][2] or board[2][0] == board[1][1] == board[0][2] and board[1][1] != None:
        return board[1][1]

    return None

def draw(board):
    if sum(j.count(None) for j in board) == 0 and winner(board) is None:
        return True    