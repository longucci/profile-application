"""
Description: Profile application with Python + MySQL
"""
import os
import re
import secrets
from flask import Flask, request, session, render_template, redirect, url_for
from flaskext.mysql import MySQL
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)
mysql_server = MySQL()

# In order to use session in 
app.secret_key = secrets.token_hex(16)

#Config app to connect to MySQL server
app.config["MYSQL_DATABASE_HOST"] = os.getenv("HOST_NAME")
app.config["MYSQL_DATABASE_DB"] = os.getenv("DB_NAME")
app.config["MYSQL_DATABASE_USER"] = os.getenv("USER_NAME")
app.config["MYSQL_DATABASE_PASSWORD"] = os.getenv("PASSWORD")

mysql_server.init_app(app)


@app.route("/")
def hello():
    return "Hello World"


@app.route("/login", methods = ["GET", "POST"])
def login():
    """
    Description: login() function take `username` and `password` from the user request (when user type in username
    and password to the login page and click login, it will create a POST request). At that time, if username and password
    are already stored in the database, users are able to login into web page. On the other hand, it will announce that
    the login step is failed.
    """
    msg = ""
    if request.method == "POST" and "username" in request.form and "password" in request.form:
        username = request.form["username"]
        password = request.form["password"]

        connector = mysql_server.connect()
        cursor = connector.cursor()

        cursor.execute(
            f"SELECT * FROM accounts WHERE username = '{username}' AND password = '{password}';"
        )
        account = cursor.fetchone() #Fetch one row from the result of query. If account is found from database, it means the login was successful
        
        if account:
            id, username, *other = account
            #Set the username to session if login is successful
            session["loggedin"] = True
            session["id"] = id
            session["username"] = username
            return render_template("index.html") #If the login was successful, announce for user and use index.html template
        else:
            msg = "Incorrect username/password !"
        connector.close()
    return render_template("login.html", msg=msg) #If not, stay at the login.html template


@app.route("/index")
def index():
    if 'loggedin' in session:
        return render_template("index.html")
    return redirect(url_for('login'))


@app.route("/register", methods=["GET", "POST"])
def register():
    msg = ""
    if request.method == "POST" and \
        "username" in request.form and \
        "password" in request.form and \
        "email" in request.form and \
        "address" in request.form and \
        "city" in request.form and \
        "district" in request.form and \
        "country" in request.form:
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        address = request.form["address"]
        city = request.form["city"]
        district = request.form["district"]
        country = request.form["country"]
        
        connector = mysql_server.connect()
        cursor = connector.cursor()

        cursor.execute(
            f"SELECT * FROM accounts WHERE username='{username}';"
        )
        account = cursor.fetchone()
        if account:
            msg = "Account already exists !"
        elif not re.match(r"^[a-z0-9A-Z._@+-]+@[a-zA-Z0-9]+\.[a-zA-Z]+$", string=email):
            msg = "Invalid email address !"
        elif not re.match(r"^[a-zA-Z0-9]+$", username):
            msg = "Username only contains characters and numbers !"
        else:
            cursor.execute(
                f"INSERT INTO accounts VALUES \
                    (NULL, '{username}', '{password}', '{email}', '{address}', '{district}', '{city}', '{country}');"
            )
            connector.commit()
            msg = "Successfully registered !"
        connector.close()
    elif request.method == "POST":
        msg = "Please fill out the form !"
    return render_template("register.html", msg=msg)


@app.route("/display", methods = ["GET"])
def display():
    # While logging in the application, the user profile will be displayed in the display tab
    if "loggedin" in session:
        connector = mysql_server.connect()
        cursor = connector.cursor()
        print(session['id'])
        cursor.execute(
            f"SELECT * FROM accounts WHERE id = '{session['id']}';"
        )
        account = cursor.fetchone()
        return render_template("display.html", account=account)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="localhost", port=7000)