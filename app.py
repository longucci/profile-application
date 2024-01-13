"""
Description: Profile application with Python + MySQL
"""
import os
from flask import Flask, request, session, render_template, redirect, url_for
from flaskext.mysql import MySQL
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)
mysql_server = MySQL()

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
            #Set the username to session if login is successful
            session["loggedin"] = True
            session["id"] = account["id"]
            session["username"] = account["username"]
            msg = "Logged in successfully !"
            return render_template("index.html", msg=msg) #If the login was successful, announce for user and use index.html template
        else:
            msg = "Incorrect username/password !"
    return render_template("login.html", msg=msg) #If not, stay at the login.html template


@app.route("/index")
def index():
    if 'loggedin' in session:
        return render_template("index.html")
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(host="localhost", port=7000)