import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from bs4 import BeautifulSoup

from helpers import apology, login_required, lookup, bmi, bmr, define_user, calculate

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

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    # get current time
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d")

    if request.method == "GET":

    # calculate daily intake
        bmi_res = bmi(session["user_id"])
        bmr_res = bmr(session["user_id"])
        body_type = define_user(session["user_id"], bmi_res)
        intake = calculate(session["user_id"], body_type, bmr_res)

        daily_diet = db.execute("SELECT * FROM daily_diet WHERE user_id = ? AND date = ?", session["user_id"], formatted_datetime)

        daily_progress = db.execute("SELECT SUM(protein) AS pro_sum, SUM(calories) AS cal_sum FROM daily_diet WHERE date = ? AND user_id = ?", formatted_datetime, session["user_id"])

        status = db.execute("SELECT * FROM build WHERE user_id = ?", session["user_id"])
        
        return render_template("index.html", protein_min=intake["pro_min"], protein_max=intake["pro_max"], calorie=round(intake["calorie"]), daily_diet=daily_diet, pro_progress=daily_progress[0]["pro_sum"], cal_progress=daily_progress[0]["cal_sum"], bmi=bmi_res, status=status)
    
    else:
    
        # add food to daily consumption via the search page
        food = request.form.get("name")
        if food:
            protein = request.form.get("protein")
            calories = request.form.get("calories")

            if not protein or not calories:
                return apology("Please input all fields!", 403)

            db.execute("INSERT INTO daily_diet (user_id, food, protein, calories, date) VALUES (?, ?, ?, ?, ?)", session["user_id"], food, protein, calories, formatted_datetime)
            return redirect("/")
        
        # add food to daily consumption via modal page
        food_name = request.form.get("food_name")
        if food_name:
            protein_amount = request.form.get("protein_amount")
            calories_amount = request.form.get("calories_amount")

            if not protein_amount or not calories_amount:
                return apology("PLease input all fields!", 403)

            db.execute("INSERT INTO daily_diet (user_id, food, protein, calories, date) VALUES (?, ?, ?, ?, ?)", session["user_id"], food_name, protein_amount, calories_amount, formatted_datetime)
            return redirect("/")
        
        
        # modify physical status
        weight = float(request.form.get("weight_mod"))
        if weight:
            age = request.form.get("age_mod")
            height = float(request.form.get("height_mod"))
            goal = request.form.get("goal_mod")
            freq = request.form.get("freq_mod")

            if not height or not goal or not freq:
                return apology("Please fill all the input fields!", 403)
            elif height <= 0 or height > 300 or weight <= 0 or weight > 200:
                return apology("Please input appropriate number within the fields")

            db.execute("UPDATE build SET age = ?, height = ?, weight = ?, goal = ?, freq = ? WHERE user_id = ?", age, height, weight, goal, freq, session["user_id"])
            return redirect("/")

        # a catchall apology
        else:
            return apology("Please fill all the input fields!", 403)
       
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

        # Redirect user to introduction page to submit physical information
        return redirect("/introduction")

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

        
@app.route("/introduction", methods=["GET", "POST"])
@login_required
def intro():
    if request.method == "POST":
        age = float(request.form.get("age"))
        weight = float(request.form.get("weight"))
        height = float(request.form.get("height"))
        freq = request.form.get("freq")
        goal = request.form.get("goal")
        sex = request.form.get("sex")

        # ensure user inputs all fields
        if not weight or not height or not age:
            return apology("Please fill all fields", 403)
        elif weight <= 0 or height <= 0 or weight > 200 or height > 300:
            return apology("Please input the appropriate height or weight!", 403)
        elif age <= 0 or age > 100:
            return apology("Please fill in appropriate age!", 403)

        # update the database
        db.execute("INSERT INTO build (user_id, age, height, weight, freq, goal, sex) VALUES (?, ?, ?, ?, ?, ?, ?)", session["user_id"], age, height, weight, freq, goal, sex)

        return redirect("/")
    
    else:
        # check if user's physical information is already in the database
        user_info = db.execute("SELECT * FROM build WHERE user_id = ?", session["user_id"])

        # redirect user to the index page if user data exists
        if user_info:
            return redirect("/")
        else:   
            return render_template("introduction.html")


@app.route("/todolist", methods=["GET", "POST"])
@login_required
def todolist():
    if request.method == "POST":
        todo = request.form.get("todo")

        if todo:
            db.execute("INSERT INTO todolist (user_id, todo, deadline) VALUES (?, ?, ?)", session["user_id"], todo, 1)
        
        # javascript will automatically submit the form if a checkbox is checked
        # how do you handle multiple check requests?
        # you don't because the page will be reloaded everytime a checkbox is checked
        # but every todos will have the same name
        # unless they don't
    
        return redirect("/todolist")
    else:
        todolist = db.execute("SELECT * FROM todolist WHERE user_id = ?", session["user_id"])

        return render_template("todolist.html", todolist=todolist)
    
@app.route("/todo_completed", methods=["POST", "GET"])
@login_required
def todo_completed ():
    if request.method == "POST":
        for i in range(1, 50):
            # making sure that the checkbox with a specific id exists
            checkbox = request.form.get(f"check{i}")
    
            if checkbox is not None:
                # print("sheesh")
                db.execute("UPDATE todolist SET done = ? WHERE todo = ? AND user_id = ?", "true", checkbox, session["user_id"])
            else:
                # how do you get the checkbox value if it is unchecked?
                # how to identify which todo is in question?
                # answer: use another input under the checkbox input in html
                # grab the value of the hidden input if request.form.get returns None
                # checkVal{i} is the identifier of a specific checkbox
                checkVal = request.form.get(f"checkVal{i}")
                db.execute("UPDATE todolist SET done = ? WHERE todo = ? AND user_id = ?", "false", checkVal, session["user_id"])

        return redirect('/todolist')
    
    return render_template('todo_completed.html')

