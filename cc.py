import os
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
import mysql.connector


def main():

    # set MySQL database name, usernmae and passord
    username, password, database = load_env_var() 



def load_env_var():
    # load env variables and return MySQL database name, usernmae and passord
    load_dotenv()
    username = os.environ.get('USER')
    password = os.environ.get('PASSWORD')
    database = os.environ.get("DATABASE")

    if username and password and database:
        return username, password, database
    else:
        print("Username, password or database name environment variables not set.")
        # return apology


if __name__ == "__main__":
    main()