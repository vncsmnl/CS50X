# Import necessary modules and functions
import os
from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL

# Import helper functions from helpers.py
from helpers import apology, login_required, lookup, usd

# Configure the Flask application
app = Flask(__name__)

# Custom filter for currency formatting in templates
app.jinja_env.filters["usd"] = usd

# Configure session to use the filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Route to display user's portfolio of stocks
@app.route("/")
@login_required
def index():
    # Retrieve user's cash and stock transactions from the database
    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    transactions = db.execute(
        "SELECT symbol, name, SUM(shares) AS shares, price FROM transactions WHERE user_id = ? GROUP BY symbol",
        session["user_id"],
    )
    account = cash[0]["cash"]

    # Calculate total value of each stock and update the account balance
    for transaction in transactions:
        name = transaction["name"]
        total = transaction["shares"] * transaction["price"]
        transaction["name"] = name
        transaction["total"] = total
        transaction["price"] = transaction["price"]
        account += total

    # Render the portfolio template with the data
    return render_template(
        "index.html", transactions=transactions, cash=cash[0]["cash"], account=account
    )


# Route for buying shares of stock
@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    # Handle the form submission when buying stocks
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("missing symbol")

        # Retrieve stock information using the provided symbol
        quote = lookup(symbol)
        if not quote:
            return apology("invalid symbol")

        # Validate and retrieve the number of shares to be bought
        shares = request.form.get("shares")
        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("invalid shares")

        shares = int(shares)
        # Check if the user has sufficient funds to make the purchase
        row = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        cash = row[0]["cash"]
        balance = cash - (shares * quote["price"])

        if balance < 0:
            return apology("insufficient funds")

        # Update user's cash balance and add a new transaction record
        db.execute(
            "UPDATE users SET cash = ? WHERE id = ?", balance, session["user_id"]
        )
        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, name, price, transacted) VALUES (?, ?, ?, ?, ?, ?)",
            session["user_id"],
            symbol.upper(),
            shares,
            quote["name"],
            quote["price"],
            datetime.now(),
        )

        # Display a success message and redirect to the portfolio page
        flash("Bought!")
        return redirect(url_for("index"))
    else:
        # Render the buy template for GET requests
        return render_template("buy.html")


# Route to display user's transaction history
@app.route("/history")
@login_required
def history():
    # Retrieve user's transaction history from the database
    transactions = db.execute(
        "SELECT symbol, shares, name, price, transacted FROM transactions WHERE user_id = ?",
        session["user_id"],
    )
    # Check if there are no transactions and return an apology if true
    if not transactions:
        return apology("no history", 403)
    else:
        # Render the history template with the transaction data
        return render_template("history.html", transactions=transactions)


# Route for user login
@app.route("/login", methods=["GET", "POST"])
def login():
    # Clear existing session data
    session.clear()

    # Handle form submission when logging in
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Validate username and password
        if not username or not password:
            return apology("must provide username and password", 400)

        # Query the database for the user
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Check if the user exists and the password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("invalid username and/or password", 403)

        # Set the user ID in the session and redirect to the portfolio page
        session["user_id"] = rows[0]["id"]
        return redirect(url_for("index"))
    else:
        # Render the login template for GET requests
        return render_template("login.html")


# Route to log the user out
@app.route("/logout")
def logout():
    # Clear the session and redirect to the home page
    session.clear()
    return redirect("/")


# Route for getting a stock quote
@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    # Handle form submission when getting a stock quote
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("missing symbol")

        # Retrieve and display the stock quote information
        quote_info = lookup(symbol)
        if not quote_info:
            return apology("invalid symbol")

        return render_template("quoted.html", quote=quote_info)
    else:
        # Render the quote template for GET requests
        return render_template("quote.html")


# Route for user registration
@app.route("/register", methods=["GET", "POST"])
def register():
    # Handle form submission when registering a new user
    if request.method == "POST":
        username = request.form.get("username")
        # Check if the username is available
        if not username or db.execute(
            "SELECT * FROM users WHERE username = ?", username
        ):
            return apology("username is not available")

        password = request.form.get("password")
        if not password:
            return apology("missing password")

        confirmation = request.form.get("confirmation")
        if not confirmation:
            return apology("missing confirmation")

        # Check if password and confirmation match
        if password != confirmation:
            return apology("passwords don't match")

        # Add the new user to the database
        db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)",
            username,
            generate_password_hash(password),
        )
        return redirect("/")
    else:
        # Render the registration template for GET requests
        return render_template("register.html")


# Route for selling shares of stock
@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    # Handle form submission when selling shares
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Validate symbol and shares
        if not symbol or not shares:
            return apology("missing symbol or shares")

        shares = int(shares)
        if shares <= 0:
            return apology("shares must be positive")

        # Retrieve stock information and the total number of shares owned
        sumshares = db.execute(
            "SELECT symbol, price, name, SUM(shares) AS shares FROM transactions WHERE user_id = ? AND symbol = ?",
            session["user_id"],
            symbol,
        )

        # Check if the user has enough shares to sell
        if shares > sumshares[0]["shares"]:
            return apology("too many shares")

        # Add a new transaction record for the sale
        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, name, price, transacted) VALUES (?, ?, ?, ?, ?, ?)",
            session["user_id"],
            symbol.upper(),
            -shares,
            sumshares[0]["name"],
            sumshares[0]["price"],
            datetime.now(),
        )

        # Update user's cash balance after the sale
        sold = shares * sumshares[0]["price"]
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0][
            "cash"
        ]
        db.execute(
            "UPDATE users SET cash = ? WHERE id = ?", cash + sold, session["user_id"]
        )

        # Display a success message and redirect to the home page
        flash("Sold!")
        return redirect("/")
    else:
        # Retrieve the symbols of stocks owned by the user for the sell form
        symbols = db.execute(
            "SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol",
            session["user_id"],
        )
        return render_template("sell.html", symbol=symbols)


# Route for adding additional cash to the user's account
@app.route("/addcash", methods=["GET", "POST"])
@login_required
def addcash():
    # Handle form submission when adding cash to the account
    if request.method == "POST":
        add_cash = request.form.get("add_cash")

        # Validate and add the provided amount of cash to the user's balance
        if not add_cash:
            return apology("missing add cash")

        add_cash = int(add_cash)
        if add_cash <= 0:
            return apology("add cash must be positive")

        row = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        cash = row[0]["cash"]
        balance = cash + add_cash
        db.execute(
            "UPDATE users SET cash = ? WHERE id = ?", balance, session["user_id"]
        )

        # Display a success message and redirect to the home page
        flash("Added!")
        return redirect("/")
    else:
        # Render the addcash template for GET requests
        return render_template("addcash.html")
