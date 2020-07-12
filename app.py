from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp
import math
import copy

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app = Flask(__name__)
app.secret_key = "dev"

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
    if session["board"][row][col] == None:
        session["board"][row][col] = session["turn"]
        if session["turn"] == "X":
            session["turn"] = "O"
        else:
            session["turn"] = "X"   
        return redirect(url_for("index"))
    else:
        return redirect(url_for("index"))    

@app.route("/computer")
def computer():
    if sum(j.count(None) for j in session["board"]) == 9:
        move = 0, 0
    else:       
        move = minimax(session["board"])
    return redirect(url_for('play', row=move[0], col=move[1]))

@app.route("/not")
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

def actions(board):
    possible = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == None:
                possible.append([i, j])
    return possible

def result(board, action):
    newboard = copy.deepcopy(board)
    i = action[0]
    j = action[1]

    if newboard[i][j] != None:
        raise Exception

    newboard[i][j] = player(board)
    return newboard

def terminal(board):
    if winner(board) is not None:
        return True
    if sum(j.count(None) for j in board) == 0:
        return True

    return False


def utility(board):
    if winner(board) == "X":
        return 1
    if winner(board) == "O":
        return -1
    else:
        return 0

def player(board):
    if sum(j.count(None) for j in board) % 2 == 1:
        return "X"
    else:
        return "O"        

def minimax(board):

    if player(board) == "X":
        v = -math.inf
        for action in actions(board):
            q = min_value(result(board, action))
            if q > v:
                v = q
                best = action

    if player(board) == "O":
        v = math.inf
        for action in actions(board):
            q = max_value(result(board, action))
            if q < v:
                v = q
                best = action
    return best


def max_value(board):
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


def min_value(board):
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v           

   