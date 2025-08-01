from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
import os
from datetime import datetime
from dotenv import load_dotenv
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
app.secret_key = os.getenv("FLASK_SECRET_KEY")


load_dotenv() # Load environment variables from .env

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com' 
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')

mail = Mail(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle POST request (e.g., process form data)
        searchData = get_search_data()
        searchResults = get_search_results(searchData)
        log_entry(searchData)

        if len(searchResults) > 0:
            flash(f'{len(searchResults)} entries found!', 'success')
            # render results.html with search results in table form
            return render_template("results.html", searchResults=searchResults)
        else:
            flash(f'No entries found!', 'warning')
            # return user to home/search from
            return render_template('index.html')

    else:
        # Handle GET request (e.g., display blank search form)
        return render_template('index.html')


@app.route("/about")
def about():
    return render_template("about.html")


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        email = request.form.get('email')
        subject = request.form.get('subject')
        text = request.form.get('text')
        name = request.form.get('name')

        body = f"{name}, {email}, sent an email about {subject}: {text}"

        if email and subject and text:
            try:
                msg = Message(
                    subject=F"New message from {name}",
                    recipients=[app.config['MAIL_DEFAULT_SENDER']],
                    body=body
                )
                mail.send(msg)
                flash('Email sent successfully!', 'success')
                # return user home if sucessful
                return redirect(url_for("index"))
            except Exception as e:
                flash(f'Error sending email: {e}', 'error')
        else:
            flash('Please fill in all fields.', 'warning')

    return render_template('contact.html')


@app.route("/faq")
def faq():
    return render_template("faq.html")


@app.route("/map")
def map():
    return render_template("map.html")


@app.route("/results", methods=["GET", "POST"])
def results():

    # User reached route via POST/user clicked "New Search" button
    if request.method == "POST":
        return redirect(url_for("index"))

    # User reached route via GET/no reason to view this page unless as search result
    else:
        return redirect(url_for("index"))


def clean_data(searchData):
    
    ''' Modifies search form criteria so that the search terms 
        match sqlite syntax and database schema
    '''

    # iterate over the dictionary to clean data
    for key, value in searchData.items():
        # if name is blank, the "%" wildcard will allow sqlite to return all entries
        if key == "name" and (value == "" or value == None):
            searchData[key] = "%"
        # this strips any whitespace and uses "%pattern%" to match partial names
        # note: sqlite search is case insensitive for ASCII characters
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

    # return dictionary of cleaned data
    return searchData


def get_search_data():
        
    ''' Rretrieves search terms from user input 
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
            # execute users query
            cursor.execute(query, placeholders)
            # return all rows to results
            return cursor.fetchall()
    except sqlite3.Error as e:
        flash(f"Error connecting to database: {e}")
        return None


def log_entry(searchData):
    
    ''' After user query, increment log:
        log table schema: user_id, dt, query
        Not currently storing user specific information
        Storing "query" as string of searchData/dictionary values
    '''
    
    # prepare log entry
    user_id = '' # not currently using

    # connect to database and insert log entry
    db = sqlite3.connect(DATABASE)
    try:
        with db:
            cursor = db.cursor()
            cursor.execute('''INSERT INTO log 
                                (user_id, datetime, query) 
                                VALUES (?, ?, ?)''',
                                (user_id, 
                                datetime.now().isoformat(), 
                                str(searchData))
                           )
            db.commit()
    except sqlite3.Error as e:
        flash(f"Error updating log: {e}", "warning")
    return None


# Use "debug=True" for development server only
if __name__ == '__main__':
    app.run(debug=True) 