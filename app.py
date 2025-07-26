from flask import Flask, flash, redirect, render_template, request, session, url_for
import sqlite3


''' set name of database: citycounty.db has two tables--
    city table schema: id, Name, Population, Class, County, Seat
    county table schema: id, Name, Population, Class, Township, Seat '''
DATABASE = "citycounty.db"


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

# @app.route("/map")
# def map():
#     return render_template("map.html")

# @app.route("/faq")
# def faq():
#     return render_template("faq.html")

# @app.route("/about")
# def about():
#     return render_template("about.html")



if __name__ == '__main__':
    app.run(debug=True) # Runs the development server