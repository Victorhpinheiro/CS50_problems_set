import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd
from datetime import datetime

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    #dict of all stocks, price  I will pass in template
    stocks={}
    #stock list
    stock_list = db.execute("SELECT symbol FROM (SELECT * FROM transactions GROUP BY symbol) WHERE user_id=?", session["user_id"])
    #cash
    cash = db.execute("SELECT cash FROM users where id=?", session["user_id"])[0]["cash"]
    #total agragate
    total = 0

    #lookup current price for everi item in stock list

    for stock in stock_list:
        if db.execute("SELECT SUM(shares) FROM transactions WHERE symbol=?", stock["symbol"])[0]["SUM(shares)"]>0:
            info = lookup(stock["symbol"])
            info["shares"] = db.execute("SELECT SUM(shares) FROM transactions WHERE symbol=?", info["symbol"])[0]["SUM(shares)"]
            info["total"] = info["shares"] * info["price"]
            total += info["total"]
            stocks[stock["symbol"]] = info

    total += cash

    return render_template("index.html", stocks=stocks, cash=cash, total=total)

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":

        #store the logic variables for testing
        stock = lookup(request.form.get("symbol"))
        if not stock:
            return apology("must provide valid symbol", 400)
        cash = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])[0]["cash"]
        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("must provide integer amount", 400)
        #error handling

        if shares < 1:
            return apology("must provide valid quantity", 400)
        if (shares*stock["price"]) > cash:
            return apology("Not enough money for the buy", 400)

        #passed error testing and user will buy stock
        #add stock information to the database
        db.execute("INSERT INTO transactions (user_id, symbol, price, shares, time, type) VALUES (?, ?, ?, ?, ?, ?)", session["user_id"], stock["symbol"], stock["price"], shares, datetime.now(), "Bought")

        #update the current cash value
        db.execute("UPDATE users SET cash=? WHERE id=?", cash-(shares*stock["price"]), session["user_id"])

        #redirect to index
        return redirect("/")

    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
     #dict of all stocks, price  I will pass in template
    stocks={}
    #stock list
    transactions = db.execute("SELECT * FROM transactions WHERE user_id=? ORDER BY time", session["user_id"])


    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))


        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":
        stock = lookup(request.form.get("symbol"))
        if not stock:
            return apology("must provide valid symbol", 400)
        return render_template("quoted.html", stock=stock)
    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        number=[0,1,2,3,4,5,6,7,8,9]
        valid_symbols = "!@#$%^&*()_-+={}[]"
        count_number = 0

        # for s in password:
        #     if not s in valid_symbols:
        #         return apology("must password with at least 1 symbol", 400)
        #     if s in number:
        #         count_number += count_number
        # if count_number < 2:
        #         return apology("must password with at least 2 numbers", 400)





        hashed = generate_password_hash(password)
        rows = db.execute("SELECT username FROM users WHERE username=?", username)


        #Error handling

        if not username:
            return apology("must provide username", 400)

        if password != request.form.get("confirmation") or not password:
            return apology("must provide valid password", 400)

        if len(rows) > 0:
            return apology("Username already used", 400)

        #add information to database
        db.execute("INSERT INTO users (username, hash) VALUES (?,?)", username, hashed)

        return redirect("/")

    """Register user"""
    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():

    symbols = db.execute("SELECT symbol FROM transactions GROUP BY symbol HAVING user_id=?", session["user_id"])
    stock_list = []

    for item in symbols:
            stock_list.append(item["symbol"])
    #check holdings

    for item in stock_list:
        if db.execute("SELECT SUM(shares) FROM transactions WHERE symbol=? GROUP BY symbol HAVING user_id=?", item, session["user_id"])[0]["SUM(shares)"] < 1:
            print(stock_list)
            print(item)
            stock_list.remove(item)
            print(stock_list)

    if request.method == "POST":
        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("must provide integer amount", 400)

        stock = lookup(request.form.get("symbol"))

        if not stock:
            return apology("must provide valid symbol", 400)

        for item in symbols:
            stock_list.append(item["symbol"])

        if stock["symbol"] not in stock_list:
            return apology("must provide valid symbol", 400)
        #store the logic variables for testing

        cash = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])[0]["cash"]
        hold = db.execute("SELECT SUM(shares) FROM transactions WHERE symbol=? GROUP BY symbol HAVING user_id=?", stock["symbol"], session["user_id"])[0]["SUM(shares)"]

        ##check if shares are an integer

        #error handling

        if shares < 1:
            return apology("must provide valid quantity", 400)
        if hold < shares:
            return apology("Not enough stocks for the sell", 400)

        #passed error testing and user will buy stock
        #add stock information to the database
        db.execute("INSERT INTO transactions (user_id, symbol, price, shares, time, type) VALUES (?, ?, ?, ?, ?, ?)", session["user_id"], stock["symbol"], stock["price"], -shares, datetime.now(), "Sold")

        #update the current cash value
        db.execute("UPDATE users SET cash=? WHERE id=?", cash+(shares*stock["price"]), session["user_id"])

        #redirect to index
        return redirect("/")



    return render_template("sell.html", symbols=stock_list)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
