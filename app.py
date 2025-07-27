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
        searchData = get_search_data()
        searchResults = get_search_results(searchData)

        # return render_template("results.html", searchData=searchData, searchResults=searchResults)
        return render_template("index.html", type=searchData['type'], searchResults=searchResults)
    else:
        # Handle GET request (e.g., display a form)
        return render_template('index.html')

@app.route("/results", methods=["GET", "POST"])
def results():

    # User reached route via POST that means new search
    if request.method == "POST":
        type = None
        return render_template("index.html", type=type)

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


def get_search_results(searchData):

    # establish database connection
    db = sqlite3.connect(DATABASE)

    # use row factory for dictionary like access (instead of tuple)
    db.row_factory = sqlite3.Row

    # create query as string
    #query = f"Select * FROM ? WHERE name LIKE ? AND population >= ? AND population <= ?"


    # query database for search results
    with db:
        cursor = db.cursor()
        cursor.execute("Select * FROM county WHERE name LIKE ? AND population >= ? AND population <= ?", (searchData['name'], searchData['lowerValue'], searchData['upperValue']))
        searchResults = cursor.fetchall()
        return searchResults


def get_search_data():
        
        searchData = {}
        searchData['name'] = request.form.get('name')
        searchData['lowerValue'] = request.form.get('lowerValue')
        searchData['upperValue']= request.form.get('upperValue')
        searchData['type'] = request.form.get('type')
        searchData['class'] = request.form.get('class')

        return clean_data(searchData)


def clean_data(searchData):
    
    for key in searchData:
        if key == "name" and (searchData[key] == "" or searchData[key] == None):
            searchData[key] = "%"
        elif key == 'name':
             searchData[key] = f"%{searchData[key]}%"
        elif key == "upperValue" and (searchData[key] == "" or searchData[key] == None):
            searchData[key] = 9999999
        elif key == "lowerValue" and (searchData[key] == "" or searchData[key] == None):
            searchData[key] = 0    
        elif key == "class" and (searchData['class'] == '' or searchData[key] == None):
            searchData["class"] = "%"

    return searchData


if __name__ == '__main__':
    app.run(debug=True) # Runs the development server