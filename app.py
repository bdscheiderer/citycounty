from flask import Flask, flash, redirect, render_template, request, session, url_for
import sqlite3


''' set name of database: citycounty.db has two tables--
    city table schema: id, Name, Population, Class, County, Seat
    county table schema: id, Name, Population, Class, Township, Seat '''
DATABASE = "citycounty.db"


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle POST request (e.g., process form data)
        searchData = {}
        searchData['name'] = request.form.get('name')
        searchData['lowerValue'] = request.form.get('lowerValue')
        searchData['upperValue']= request.form.get('upperValue')
        searchData['cityorcounty'] = request.form.get('cityorcounty')
        searchData['class'] = request.form.get('class')

        searchResults = query_database(searchData)

        return render_template("results.html", searchData=searchData, searchResults=searchResults)
    else:
        # Handle GET request (e.g., display a form)
        return render_template('index.html')

@app.route("/results", methods=["GET", "POST"])
def results():

    # User reached route via POST that means new search
    if request.method == "POST":
        return render_template("index.html")

    # User reached route via GET
    else:
        return render_template("results.html")


@app.route("/map")
def map():
    return render_template("map.html")


@app.route("/faq")
def faq():
    return render_template("faq.html")


@app.route("/about")
def about():
    return render_template("about.html")


def query_database(searchData):
    searchResults = DATABASE
    return searchResults

if __name__ == '__main__':
    app.run(debug=True) # Runs the development server