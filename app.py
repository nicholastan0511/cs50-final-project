import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///final.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    # get the query
    q = request.args.get("food")

    if not q:
        foods = []
    else:
    # query the food from the csv file
        foods = lookup(q)

    return render_template("index.html", foods=foods)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    # clear session from any user id
    session.clear()

    # redirect user to the login page
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        
        # get the usernames of all registered users
        active_users = db.execute("SELECT username FROM users")

        # ensure user inputs all input fields
        if not username:
            return apology("Please input username!", 403)
        elif not password or not confirmation:
            return apology("Please input password!", 403)
        elif not password == confirmation:
            return apology("Password confirmation invalid!", 403)

        # ensure user inputs unique username
        for user in active_users:
            if username == user["username"]:
                return apology("Username taken! Please input another username!", 403)

        # add successful cases to the database and redirect user to the login page
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, generate_password_hash(password, method='pbkdf2', salt_length=16))
        return redirect("/login");
    
    # render the register page when user access the register page
    return render_template("register.html")

@app.route("/search")
def search():
    # get the query
    q = request.args.get("food")

    if not q:
        foods = []
    else:
    # query the food from the csv file
        foods = lookup(q)

    return render_template("search.html", foods=foods)

        
@app.route("/introduction")
def intro():
    weight = request.form.get("weight")
    height = request.form.get("height")
    freq = request.form.get("freq")
    goal = request.form.get("goal")

    db.execute("INSERT INTO build (user_id, height, weight, freq, goal) VALUES (?, ?, ?, ?, ?)", session["user_id"], height, weight, freq, goal)

    return redirect("/")


