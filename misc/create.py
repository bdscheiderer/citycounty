''' This program createst the sqlite3 database to use with the city county program
    It reads from two cvs file containing the city and county population and classification
    data. 

    County schema: id, name, population, class, township, seat
    City schema: id, name, population, class, county, seat
'''
import pandas as pd
import csv
import sqlite3
import datetime

def main():

    # set database and csv file names
    database = "citycounty.db"
    datafile = "data/cc2022.csv"

    # create database and load csv data to table
    #create_database(database)
    #create_log_table(database)
    #create_table(database, datafile)

    test_log(database)


def test_log(database):
    try:
        with sqlite3.connect(database) as conn:
            cursor = conn.cursor()
            
#INSERT INTO table_name (column1, column2, column3, ...) VALUES (value1, value2, value3, ...);

            user_id = ""
            dt = datetime.datetime.now().isoformat()
            query = "test query"

            cursor.execute('''
                INSERT INTO log (
                           user_id, datetime, query)
                           VALUES (?, ?, ?)
            ''', (user_id, dt, query))

            conn.commit() # Commit changes to the database
        print(f"Database {database} updated successfully.")
    except sqlite3.Error as e:
        print(f"Error connecting to or creating database: {e}")

# def create_log_table(database):
#     # create log table
#     try:
#         with sqlite3.connect(database) as conn:
#             cursor = conn.cursor()
            
#             cursor.execute('''
#                 CREATE TABLE IF NOT EXISTS log (
#                     id INTEGER PRIMARY KEY,
#                     user_id TEXT,
#                     datetime TIMESTAMP,   
#                     query TEXT
#                 )
#             ''')

#             conn.commit() # Commit changes to the database
#         print(f"Database {database} updated successfully.")
#     except sqlite3.Error as e:
#         print(f"Error connecting to or creating database: {e}")



def create_database(database):

    # create the database file and city/county tables
    try:
        with sqlite3.connect(database) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS citycounty2 (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    type TEXT,   
                    population INTEGER,
                    class TEXT,
                    countyseat TEXT
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS log (
                    id INTEGER PRIMARY KEY,
                    user_id TEXT,
                    datetime TIMESTAMP,   
                    query TEXT
                )
            ''')

            conn.commit() # Commit changes to the database
        print(f"Database {database} created or connected successfully.")
    except sqlite3.Error as e:
        print(f"Error connecting to or creating database: {e}")

def create_table(database, datafile):

    # load county data to county table
    try:
        # Read CSV into pandas DataFrame
        df = pd.read_csv(datafile)

        # Connect to SQLite database
        conn = sqlite3.connect(database)

        # Write DataFrame to SQLite table
        table_name = "citycounty2"
        df.to_sql(table_name, conn, if_exists='replace', index=False) # 'replace' will overwrite if table exists

        print(f"Data from {datafile} successfully loaded into {table_name} in {database} using pandas.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.commit()
            conn.close()
    

if __name__ == "__main__":
    main()