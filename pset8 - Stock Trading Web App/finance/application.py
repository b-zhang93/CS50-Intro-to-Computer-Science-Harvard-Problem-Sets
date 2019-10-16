import os

import cs50
from cs50 import SQL, get_string
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash


from helpers import apology, login_required, lookup, usd

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
    """Show portfolio of stocks"""

    user_id = session["user_id"]

    # get remaining cash and total portfolio value
    cash = db.execute("SELECT cash FROM users WHERE id = :userid", userid=user_id)
    cashv = db.execute("SELECT sum(amount) as amount FROM Transactions WHERE userid = :userid", userid=user_id)
    # cash on hand
    cash_total = cash[0]["cash"]
    # portfolio value
    stock_total = cashv[0]["amount"]

    # checks for None and convert to integer
    if cash_total is None:
        cash_total = int(0)

    # checks for None
    if stock_total is None:
        stock_total = int(0)

    # get the required information for index table from SQL table transactions
    index = db.execute("SELECT symbol, sum(shares) as shares, curr_value, curr_price FROM Transactions WHERE userid = :userid GROUP BY symbol HAVING sum(shares) > 0 ORDER BY date_purch desc", userid=user_id)

    # calculate current price of stock and the current value based on how many stocks are owned
    for i in range(len(index)):
        symbol = index[i]["symbol"]
        shares = index[i]["shares"]
        curr_price = lookup(symbol)["price"]
        curr_value = (curr_price * shares)
        db.execute("UPDATE Transactions SET curr_price=:curr_price, curr_value=:curr_value WHERE userid=:userid AND symbol=:symbol", curr_price=curr_price,
                   curr_value=curr_value, userid=user_id, symbol=symbol)

    # render index again for refresh
    index = db.execute("SELECT symbol, sum(shares) as shares, curr_value, curr_price FROM Transactions WHERE userid = :userid GROUP BY symbol HAVING sum(shares) > 0 ORDER BY date_purch desc", userid=user_id)
    # calculates portfolio worth with remaining cash + all assets
    grand_total = (stock_total * -1) + cash_total

    return render_template("index.html", index=index, total=cash_total, pvalue=grand_total, stocktotal=(stock_total*-1))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":

        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        quote = lookup(symbol)
        userid = session["user_id"]

        # checks integers only
        try:
            shares = int(shares)
        except ValueError:
            return apology("Invalid Entry")

        # Ensure something was submitted
        if not symbol:
            return apology("Symbol not valid")

        # Ensures the symbol exists in API
        elif not quote:
            return apology("Symbol not Found")

        elif not shares:
            return apology("input shares please")

        # Cannot buy negative stock
        elif int(shares) < 0:
            return apology("Shares Must be Positive")

        else:
            # get the price from quote dict
            price = quote["price"]
            # calculate total transaction cost
            cost = (float(price) * int(shares))

            # checks user's current cash amount from SQL
            cash = db.execute("SELECT cash FROM users WHERE id = :id", id=userid)
            funds = float(cash[0]["cash"])

            if cost > funds:
                return apology("Not Enough Funds")

            # insert transaction into database [note: buy = 0, sell = 1]
            db.execute("INSERT INTO Transactions(userid, symbol, price, shares, buyorsell, amount) values(:userid, :symbol, :price, :shares, :buy, :amount)",
                       userid=userid, symbol=symbol.upper(), price=price, shares=shares, buy="B", amount=(cost * -1))

            # updates cost and user's cash
            db.execute("UPDATE users SET cash = cash - :cost WHERE id = :id", cost=cost, id=userid)

            flash("Purchase Successful")
            return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    userid = session["user_id"]
    # queue data from SQL listing transaction history for user
    history = db.execute("SELECT symbol, price, buyorsell, shares, amount, date_purch FROM Transactions WHERE userid= :userid ORDER BY date_purch DESC",
                         userid=userid)

    return render_template("history.html", history=history)


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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

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
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":

        symbol = request.form.get("symbol")
        quote = lookup(symbol)

        # Ensure something was submitted
        if not symbol:
            return apology("Symbol not valid")

        # Ensures the symbol exists in API
        elif not quote:
            return apology("Symbol not Found")

        else:
            return render_template("quoted.html", symbol=quote["symbol"], name=quote["name"],
                                   price=quote["price"])
    else:
        return render_template("quote.html")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""

    user = request.args.get("username")
    # query the database with IDs and usernames
    rows = db.execute("SELECT * FROM users WHERE username = :username", username=user)

    # ensures validation for username
    if not user:
        return jsonify(False)

    # checks if username already exists or not
    if len(rows) >= 1:
        return jsonify(False)

    else:
        return jsonify(True)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        new_user = request.form.get("username")
        pword = request.form.get("password")
        confirm = request.form.get("confirmation")
        # query the database with IDs and usernames
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=new_user)

        # ensures validation for username, password, and confirmation
        if not new_user:
            return apology("missing username", 400)

        elif not pword:
            return apology("missing password", 400)

        elif not confirm:
            return apology("must confirm password", 400)

        # checks if username already exists or not
        elif len(rows) >= 1:
            return apology("Username Taken", 400)

        elif pword != confirm:
            return apology("Passwords do not match", 400)

        # if passes all checks, insert new user into database
        else:
            hash_p = generate_password_hash(pword)
            db.execute("INSERT INTO users(username,hash) values(:username, :hash)",
                       username=new_user, hash=hash_p)

            rows = db.execute("SELECT * FROM users WHERE username = :username", username=new_user)

            # saves the session for this user
            session["user_id"] = rows[0]["id"]

            return redirect("/")
    else:
        return render_template("register.html")


@app.route("/addcash", methods=["GET", "POST"])
@login_required
def addcash():
    """ allows user to add more cash """

    userid = session["user_id"]

    # brings up cash amount
    cash = db.execute("SELECT cash FROM users WHERE id = :id", id=userid)
    funds = float(cash[0]["cash"])

    if request.method == "POST":

        # gets cash inputted by user and adds to user's bank
        add = int(request.form.get("add"))

        if add < 0:
            return apology("invalid amount")
        else:
            db.execute("UPDATE users SET cash = cash + :add WHERE id = :id", add=add, id=userid)

        return redirect("/")

    else:
        return render_template("addcash.html", funds=funds)


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # getting the list of stocks that are currently owned by logged in user
    userid = session["user_id"]
    stocks = db.execute("SELECT symbol, sum(shares) as shares FROM Transactions WHERE userid = :userid GROUP BY symbol HAVING sum(shares) > 0 ",
                        userid=userid)

    # creating a list with all symbols without extra syntax
    s_list = set()
    for stocks in stocks:
        s_list.add(stocks["symbol"])

    if request.method == "POST":

        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        quote = lookup(symbol)
        price = quote["price"]

        # calculate total transaction gain from selling stock
        rev = (float(price) * int(shares))

        # count total shares owned for stock being sold and record it as a variable
        count = db.execute("SELECT sum(shares) as shares FROM Transactions WHERE symbol= :symbol GROUP BY symbol",
                           symbol=symbol)
        inventory = count[0]["shares"]

        # Ensure something was submitted
        if not symbol:
            return apology("Symbol not valid")

        # Cannot buy negative stock
        elif int(shares) < 0:
            return apology("Shares cannot be negative")

        # makes sure you don't sell more stock than you have
        elif int(shares) > int(inventory):
            return apology("You do not have that many shares")

        else:
            # queue information from SQL database
            stocks = db.execute("SELECT symbol FROM Transactions WHERE userid = :userid GROUP BY symbol HAVING sum(shares) > 0",
                                userid=userid)
            # checks user's current cash amount from SQL
            cash = db.execute("SELECT cash FROM users WHERE id = :id", id=userid)
            funds = float(cash[0]["cash"])

            # insert transaction into database [note: buy = B, sell = S]
            db.execute("INSERT INTO Transactions(userid, symbol, price, shares, buyorsell, amount) values(:userid, :symbol, :price, :shares, :sell, :amount)",
                       userid=userid, symbol=symbol, price=price, shares=(int(shares) * -1), sell="S", amount=rev)

            # updates cost and user's cash
            db.execute("UPDATE users SET cash = cash + :rev WHERE id = :id", rev=rev, id=userid)

            flash("Stocks Sold")
            return redirect("/")

    else:
        return render_template("sell.html", stocks=stocks, list=s_list)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
