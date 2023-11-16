import csv
import re

from flask import redirect, render_template, session
from functools import wraps
from cs50 import SQL

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///final.db")

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def lookup(food):
    file_name = open("./database/nutrition.csv")
    data = csv.DictReader(file_name)

    food_list = []

    for row in data:
        # if row["name"].lower().__contains__(food.lower()):
        #     food_list.append(row)
        # if food.lower() in row["name"]:
        #     food_list.append(row)

        if re.search(r'\b' + re.escape(food.lower()) + r'\b', row["name"].lower()):
            food_list.append(row)
            
    return food_list

def calculate(user_id, body_type, bmr):
    data = db.execute("SELECT * FROM build WHERE user_id = ?", user_id)

    intake = {}

    # source: examine.com
    # if user is active and has healthy weight targets muscle gain and fat loss
    if not data[0]["goal"] == 0 and body_type["exercise_level"] == "active" and body_type["bmi"] < 2:
        intake["pro_min"] = round(data[0]["weight"] * 1.6, 2)
        intake["pro_max"] = round(data[0]["weight"] * 2.4, 2)

    # if user is sedentary and has healthy weight
    elif body_type["exercise_level"] == "sedentary" and body_type["bmi"] < 2:
        intake["pro_min"] = round(data[0]["weight"] * 1.2, 2)
        intake["pro_max"] = round(data[0]["weight"] * 1.8, 2)

    # if user is active and targets maintenence
    elif data[0]["goal"] == 0 and body_type["exercise_level"] == "active" and body_type["bmi"] < 2:
        intake["pro_min"] = round(data[0]["weight"] * 1.4, 2)
        intake["pro_max"] = round(data[0]["weight"] * 2.0, 2)

    elif body_type["bmi"] >= 2:
        intake["pro_min"] = round(data[0]["weight"] * 1.2, 2)
        intake["pro_max"] = round(data[0]["weight"] * 1.5, 2)

    # source: ministry of health of UAE
    # calculate calorie intake based on activity level
    if body_type["exercise_level"] == "active":
        intake["calorie"] =  bmr * 1.55
    else: 
        intake["calorie"] = bmr * 1.2

    return intake

def define_user(user_id, bmi):
    data = db.execute("SELECT * FROM build WHERE user_id = ?", user_id)

    # store all information about the user physical type in the dictionary
    body_type = {}

    # 0 as underweight, 1 as normalweight, 2 as overweight, 3 as obesity
    if bmi <= 18.5:
        body_type["bmi"] = 0
    elif bmi > 18.5 and bmi <= 24.9:
        body_type["bmi"] = 1
    elif bmi >= 25 and bmi <= 29.9:
        body_type["bmi"] = 2
    else:
        body_type["bmi"] = 3

    if data[0]["freq"] == 0:
        body_type["exercise_level"] = "sedentary"
    else:
        body_type["exercise_level"] = "active"

    return body_type
      

def bmi(user_id):
    data = db.execute("SELECT height, weight FROM build WHERE user_id = ?", user_id)

    # formula for bmi
    # return only two decimal points
    return float("{:.2f}".format(float(data[0]["weight"] / (float(data[0]["height"])/100) ** 2)))

def bmr(user_id):
    data = db.execute("SELECT sex, age, height, weight FROM build WHERE user_id = ?", user_id)

    if data[0]["sex"] == 0:
        return 10 * data[0]["weight"] + 6.25 * data[0]["height"] - 5 * data[0]["age"] + 5

    else:
        return 10 * data[0]["weight"] + 6.25 * data[0]["height"] - 5 * data[0]["age"] - 161