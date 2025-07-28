from flask import Flask, flash, render_template, request
import sqlite3


''' set constants including name of database and table
    citycounty schema: id INTEGER PRIMARY KEY, name TEXT NOT NULL,
    type TEXT, population INTEGER, class TEXT, countyseat TEXT
'''
DATABASE = "citycounty.db"  # sqlite3 database located in same directory
TABLENAME = "citycounty"    # table name in db
MAXPOP = 9999999            # higher than state population (essentially no upper limit)
MINPOP = 0                  # sets lower limit for search terms

# start Flask session
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle POST request (e.g., process form data)
        searchData = get_search_data()
        searchResults = get_search_results(searchData)
        # render results.html with search results in table form
        return render_template("results.html", type=searchData['type'], searchResults=searchResults)
    else:
        # Handle GET request (e.g., display a form)
        return render_template('index.html')


@app.route("/results", methods=["GET", "POST"])
def results():

    # User reached route via POST (that means user clicked new search button)
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


def get_search_results(searchData):

    ''' Takes the search criteria from user input, establishes db 
        connection, performs sql query, and returns search results
    '''

    # establish database connection
    db = sqlite3.connect(DATABASE)

    # use row factory for dictionary-like data access (instead of a tuple)
    db.row_factory = sqlite3.Row

    # create query as string and tuple of ? parameters
    query = f"Select * FROM {TABLENAME} WHERE name LIKE ? AND population >= ? AND population <= ? AND class LIKE ? AND type LIKE ?"
    placeholders = (searchData['name'], searchData['lowerValue'], searchData['upperValue'], searchData['class'], searchData['type'])


    # query database for search results, using ? placeholders
    try:
        with db:
            cursor = db.cursor()
            cursor.execute(query, placeholders)
            return cursor.fetchall()
    
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}") # change this to flash message
        return None
        

def get_search_data():
        
        ''' This function retrieves search terms from user input 
            entered on the index.html search form
        '''
        
        # using dictionary to store the data from the row.factory sqlite3 option
        searchData = {}
        searchData['name'] = request.form.get('name')
        searchData['lowerValue'] = request.form.get('lowerValue')
        searchData['upperValue']= request.form.get('upperValue')
        searchData['type'] = request.form.get('type')
        searchData['class'] = request.form.get('class')

        # run the clean_data function prior to return
        return clean_data(searchData)


def clean_data(searchData):
    
    ''' Modifies search form criteria so that the search terms 
        match sqlite syntax and database schema
    '''

    for key, value in searchData.items():
        # if name is blank, the "%" wildcard will allow sql to return all entries
        if key == "name" and (value == "" or value == None):
            searchData[key] = "%"
        # this strips any whitespace and uses "%pattern%" to match partial names
        # note: sql search is case insensitive for ASCII characters
        elif key == 'name':
             searchData[key] = f"%{value.strip()}%"
        # if max population is blank, set to a high value to return all greater than the min
        elif key == "upperValue" and (value == "" or value == None):
            searchData[key] = MAXPOP
        # if min population is blank, set to zero to search for all up the max
        elif key == "lowerValue" and (value == "" or value == None):
            searchData[key] = MINPOP
        # if type is blank or "both", use "%" wildcard to search for both cities and counties
        elif key == "type" and (value == '' or value == None or value == "Both" or value == "both"):
            searchData["type"] = "%"
        # if class blank, uses "%" wildcard to search for any class
        elif key == "class" and (value == '' or value== None):
            searchData["class"] = "%"

    return searchData

# Use "debug=True" for development server only
if __name__ == '__main__':
    app.run(debug=True) 