from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
import sqlite3


# set name of database
# citycounty.db has two tables: city & county
# city schema: id, Name, Population, Class, County, Seat
# county schema: id, Name, Population, Class, Township, Seat
DATABASE = "citycounty.db"


app = Flask(__name__)

''' TO DO - users need to login??? '''
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    return render_template("index.html")

