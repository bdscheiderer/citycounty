import os
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
import sqlite3


# set name of database
# citycounty.db has two tables: city & county
DATABASE = "citycounty.db"

def main():

    # set database name, usernmae and passord
    # username, password, database = load_env_var() 

    string = input("Enter search string: ")
    results = []

    #establish database connection
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()

        # query tables for search string
        c.execute("SELECT * FROM county WHERE Name LIKE ?", ("%{}%".format(string),))
        rows = c.fetchall()

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            # conn.commit()
            conn.close()

    if len(rows) == 0:
        print("No results found.")
    elif len(rows) == 1:
        print("Printing result: ")
        print(rows)
    else:
        print(f"Printing {len(rows)} results:")
        for row in rows:
            print(row)

# def load_env_var():
#     # load env variables and return database name, usernmae and passord
#     load_dotenv()
#     username = os.environ.get('USER')
#     password = os.environ.get('PASSWORD')
#     database = os.environ.get("DATABASE")

#     if username and password and database:
#         return username, password, database
#     else:
#         print("Username, password or database name variables not set.")
#         # return apology


if __name__ == "__main__":
    main()