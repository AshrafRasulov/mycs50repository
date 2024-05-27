import asyncio
import datetime, time
import threading
from cs50 import SQL
from flask import Flask, flash, request, session, render_template, redirect, session
from flask_session import Session
from util import login_required, apology, checkpassword, usd, checkphone
from werkzeug.security import generate_password_hash

import json

# for demonstration will used secound like a minute
minuteTemp = 1 *  5  * 12

app = Flask(__name__)
app.jinja_env.filters["usd"] = usd

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
try:
    db = SQL("sqlite:///cofeedb.db")
    print("connection successfully!!!")
except:
    print("it can't connected")

globOrders = 0

try:
    globOrders = db.execute("SELECT * FROM orderTable")
except:
    print("nothing changed")



@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/server")
def server():
    return render_template("server.html")


# @app.route("/employlog")
# def employ_login():
#         return render_template("employ-loging.html")

orderExecutes = threading

@app.route("/employlog")
@app.route("/barista-login", methods=["GET", "POST"])
# @login_required
def baristaprofile():
    if request.method == "POST":
        dtb = db.execute("SELECT orderTable.id, email,name, img, count, tblCoffee.preparationTime FROM orderTable JOIN tblCoffee ON tblCoffee.id = orderTable.coffeType JOIN tblClient ON tblClient.id = orderTable.client_id")

        return render_template("barista.html", baristadb=dtb)
    else:
        dtb = db.execute("SELECT orderTable.id, email,name, img, count, tblCoffee.preparationTime FROM orderTable JOIN tblCoffee ON tblCoffee.id = orderTable.coffeType JOIN tblClient ON tblClient.id = orderTable.client_id")

        print("GET Barista")
        return render_template("barista.html", baristadb=dtb)

@app.route("/barista-login")
# @login_required
def baristarefresh():
    dtb = db.execute("SELECT orderTable.id, email,name, img, count, tblCoffee.preparationTime FROM orderTable JOIN tblCoffee ON tblCoffee.id = orderTable.coffeType JOIN tblClient ON tblClient.id = orderTable.client_id")
    print("Refresh Barista")
    # withoutlogend(dtb[0])
    return render_template("barista.html", baristadb=dtb)



@app.route("/index")
@app.route("/")
def index():
    session.clear()
    try:
        coffe = db.execute("SELECT * FROM tblCoffee")
    except:
        print("selection not work")

    print(coffe)
        
    return render_template("index.html", cofeedb=coffe)


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    print(session["user_id"])

    """Show portfolio of stocks"""
    user_id = session["user_id"]

    try:
        coffe = db.execute("SELECT * FROM tblCoffee")
    except:
        print("selection not work")
        
    return render_template("profile.html", cofeedb=coffe)



@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()
    """Register user"""
    if request.method == "POST":

        if not request.form.get("phone"):
            return apology("Please, Enter the phone:")
        
        if not checkphone(request.form.get("phone")):
            return apology("Number is did not conform to the input requirement")
        
        if not request.form.get("email"):
            return apology("Please, Enter the email:")
        
        if not request.form.get("password"):
            return apology("Please, Enter the password:")
        
        if not request.form.get("confirmation"):
            return apology("Confirm the password, please.")
        
        phone = request.form.get("phone")   
        email = request.form.get("email")        
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if password != confirmation:
            return apology("Confirm the password, please.")

        rows = db.execute("SELECT email FROM tblClient WHERE email= ?;", email)
        if len(rows) != 0:
            return apology(f"The username '{email}' already exists. Please choose another name.")

        if password != confirmation:
            return apology("Password not Confirmed or not they match")

        hash = generate_password_hash(password)
        try:
            new_user = db.execute("INSERT INTO tblClient (phone, email, password) VALUES(?, ?, ?)", phone, email, hash)
        except:
            return apology("Username is exists", 400)

        session["user_id"] = new_user
        flash("Registered!")

        return redirect("/")

    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()
    if request.method == "GET":
        return render_template("login.html")
    else:
        # Ensure username was submitted
        if not request.form.get("email"):
            return apology("must provide email", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        
        email = request.form.get("email")
        password = request.form.get("email")

        # Query database for username
        rows = db.execute(
            "SELECT * FROM tblClient WHERE email = ?", email)
        print(checkpassword(rows, password))
        
        # print(check_password_hash(password))
        # Ensure username exists and password is correct
        if len(rows) != 1 or not checkpassword(rows, password):
            print("False")
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in and i can't solve this problem with user id coz i leave this problem.
        session["user_id"] = rows[0]["id"]
        # session["user_id"] = session["user_id"]
        return redirect("/profile")

@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")


@app.route("/coffee/<CoffeeType>", methods=["GET", "POST"])
def cofeeOrder(CoffeeType):
    if request.method == "POST":
        coffeedata = db.execute("SELECT * FROM tblCoffee WHERE id = ?", int(CoffeeType))
        return render_template("order.html", coffee = coffeedata[0])
    else:
        coffeedata = db.execute("SELECT * FROM tblCoffee WHERE id = ?", int(CoffeeType))
        return redirect("order.html", coffee = coffeedata[0])


@app.route("/buy/<data>", methods=["GET", "POST"])
def buy(data):
    if request.method == "POST":
        type = int(data)
        todayTime = str(datetime.datetime.now().hour) + ":" + str(datetime.datetime.now().minute) +":" + str(datetime.datetime.now().second)
        user_id = session["user_id"]
        # check if has not data
        if not request.form.get("count"):
            return apology("must provide count", 400)        
        # try to get data from form
        try:
            count = int(request.form.get("count"))
        except:
            return apology("Username is exists", 400)
        
        coffee = db.execute("SELECT * FROM tblCoffee WHERE id = ?", type)[0]
        preparationTime = int(coffee["preparationTime"])

        # print("This is complate selecting data to insert:")
        db.execute("INSERT INTO orderTable (client_id, coffeType, count, orderDate, preparationTime) VALUES(?, ?, ?, ?, ?)",
                                                                                    user_id, type, count, todayTime, preparationTime)
        
        tr = threading.Thread(target = dataCcleanFromTable, args=str(user_id))
        tr.start()

        return redirect("/profile")
    else:
        return redirect("/profile")


@app.route("/myhome")
def myhome():
    user_id = session["user_id"]
    dbclient = db.execute("SELECT client_id, name, price, img, count, orderDate, orderTable.preparationTime AS 'PrTime' FROM orderTable JOIN tblCoffee ON tblCoffee.id = orderTable.coffeType WHERE orderTable.client_id = ?",
                           user_id)
    
    


    
    return render_template("myhome.html", dbs = dbclient)

def dataCcleanFromTable(user_id):
    print(f"dataCcleanFromTable activated")
    GlobN = int(1)
    if not db.execute("SELECT COUNT(id) AS 'COUNT' FROM orderTable")[0]["COUNT"]:
        GlobN = 0
    else:
        GlobN = int(db.execute("SELECT COUNT(id) AS 'COUNT' FROM orderTable")[0]["COUNT"])
    print(GlobN)
    if GlobN == 0:
        db.execute("UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME = 'orderTable'")
        
    userid = int(user_id)

    N = 0
    for evN in globOrders:
        if int(evN["client_id"]) == userid:
            N = N + 1

    print(f"user[{userid}]: {N}")

    selfOrd = int(db.execute("SELECT COUNT(id) AS 'COUNT' FROM orderTable  WHERE client_id = ?", userid)[0]["COUNT"])
    if selfOrd != selfOrd:
        return print('Baristart')

    Baristart = db.execute("SELECT id, preparationTime AS 'prtime' FROM orderTable WHERE client_id = ?", userid)
    print(Baristart)
    for prT in Baristart:
        time.sleep(int(prT["prtime"]) * minuteTemp)
        
        # print(f"for coffeetype[{prT["id"]}]: need {prT["prtime"]}")
        db.execute("DELETE FROM orderTable WHERE id = ?", int(prT["id"]))
    return print("All Done")





if __name__=='__main__':
    t1 = threading.Thread(target=app.run(debug=True, threaded=True, processes=2))
    t1.start()


