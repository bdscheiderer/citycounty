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

load_dotenv() # Load environment variables from .env

# start Flask session
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")


# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com' 
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')
mail = Mail(app)


# route for "index" home page
@app.route('/', methods=['GET', 'POST'])
def index():

    # Handle POST request (e.g., process form data)
    if request.method == 'POST':

        # first check if advanced search button clicked
        if 'advanced' in request.form:
            description = request.form.get('description')
            if description is not None and description != '':
                search_data = get_adv_search_data(description)
            else:
                flash("Missing city-county description")
                return redirect(url_for("index"))
        
        # else basic search button clicked (TO DO: what about enter button???)
        else:
            search_data = get_search_data()

        # query db for search results
        search_results = get_search_results(search_data)
        log_entry(search_data)

        # check for no results and send search results to results page
        if len(search_results) > 0:
            flash(f'{len(search_results)} entries found!', 'success')
            # render results.html with search results in table form
            return render_template("results.html", search_results=search_results)
        else:
            flash(f'No entries found!', 'warning')
            # return user to home/search from
            return redirect(url_for("index"))
        
    # Handle GET request (e.g., display blank search form) 
    else:
        return render_template('index.html')


# route for about page, currently includes legal and privacy
@app.route("/about")
def about():
    return render_template("about.html")


# route for contact page, email using using gmail smtp
@app.route('/contact', methods=['GET', 'POST'])
def contact():

    # route if user completes form and clicks submit button
    if request.method == 'POST':
        email = request.form.get('email')
        subject = request.form.get('subject')
        text = request.form.get('text')
        name = request.form.get('name')
        body = f"{name}, {email}, sent an email about {subject}: {text}"

        # proceed to send email and return user to home page,
        # but only if user fills out form, else return to contact form
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

    # GET route, user loads page from link
    return render_template('contact.html')


# route for FAQs page
@app.route("/faq")
def faq():
    return render_template("faq.html")


# route for page with Map of Missouri
@app.route("/map")
def map():
    return render_template("map.html")


# route to results page to display search results
@app.route("/results", methods=["GET", "POST"])
def results():

    # User reached route via POST/user clicked "New Search" button
    if request.method == "POST":
        return redirect(url_for("index"))

    # User reached route via GET/no reason to view this page unless as search result
    else:
        return redirect(url_for("index"))
    

def clean_data(search_data):
    
    ''' Modifies search form criteria so that the search terms 
        match sqlite syntax and database schema
    '''

    # iterate over the dictionary to clean data
    for key, value in search_data.items():
        # if name is blank, the "%" wildcard will allow sqlite to return all entries
        if key == "name" and (value == "" or value == None):
            search_data[key] = "%"
        # this strips any whitespace and uses "%pattern%" to match partial names
        # note: sqlite search is case insensitive for ASCII characters
        elif key == 'name':
             search_data[key] = f"%{value.strip()}%"
        # if max population is blank, set to a high value to return all greater than the min
        elif key == "upperValue" and (value == "" or value == None):
            search_data[key] = MAXPOP
        # if min population is blank, set to zero to search for all up the max
        elif key == "lowerValue" and (value == "" or value == None):
            search_data[key] = MINPOP
        # if type is blank or "both", use "%" wildcard to search for both cities and counties
        elif key == "type" and (value == '' or value == None or value == "Both" or value == "both"):
            search_data["type"] = "%"
        # if class blank, uses "%" wildcard to search for any class
        elif key == "class" and (value == '' or value== None):
            search_data["class"] = "%"

    # return dictionary of cleaned data
    return search_data


def get_search_data():
        
    ''' Rretrieves search terms from user input 
        entered on the index.html search form
    '''
    
    # using dictionary to store the data from the row.factory sqlite3 option
    search_data = {}
    search_data['name'] = request.form.get('name')
    search_data['lowerValue'] = request.form.get('lowerValue')
    search_data['upperValue']= request.form.get('upperValue')
    search_data['type'] = request.form.get('type')
    search_data['class'] = request.form.get('class')

    # run the clean_data function prior to return
    return clean_data(search_data)


def get_search_results(search_data):

    ''' Takes the search criteria from user input, establishes db 
        connection, performs sql query, and returns search results
    '''

    # establish database connection
    # db_path = os.path.join(os.environ['HOME'], 'citycounty', 'citycounty.db')
    # db = sqlite3.connect(db_path)
    db = sqlite3.connect(DATABASE)

    # use row factory for dictionary-like data access (instead of a tuple)
    db.row_factory = sqlite3.Row

    # create query as string and tuple of ? parameters
    query = f"Select * FROM {TABLENAME} WHERE name LIKE ? AND population >= ? AND population <= ? AND class LIKE ? AND type LIKE ?"
    placeholders = (search_data['name'], search_data['lowerValue'], search_data['upperValue'], search_data['class'], search_data['type'])

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


def get_adv_search_data(description):
    ''' TO DO: parse natural languge description 
        to get search data for db query
    '''
    search_data = {}
    
    # to do fill in parsing algorithm




    # test data
    search_data['name'] = None
    search_data['lowerValue'] = 999
    search_data['upperValue']= 999999
    search_data['type'] = None
    search_data['class'] = None

    return clean_data(search_data)


def log_entry(search_data):   # TO DO: switch to proper logging
    
    ''' After user query, increment log and store query as a
        string of the "search_data" dictionary values
        log table schema: user_id, dt, query
        Not currently storing user specific information
    '''
    
    # prepare log entry
    user_id = '' # not currently using


    # connect to database and insert log entry
    # db_path = os.path.join(os.environ['HOME'], 'citycounty', 'citycounty.db')
    # db = sqlite3.connect(db_path)
    db = sqlite3.connect(DATABASE)

    try:
        with db:
            cursor = db.cursor()
            cursor.execute('''INSERT INTO log 
                                (user_id, datetime, query) 
                                VALUES (?, ?, ?)''',
                                (user_id, 
                                datetime.now().isoformat(), 
                                str(search_data))
                           )
            db.commit()
    except sqlite3.Error as e:
        flash(f"Error updating log: {e}", "warning")
    return None


# Use "debug=True" for development server only
if __name__ == '__main__':
    app.run(debug=True) 