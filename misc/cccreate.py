''' This program createst the sqlite3 database to use with the city county program
    It reads from two cvs file containing the city and county population and classification
    data. 

    County schema: id, name, population, class, township, seat
    City schema: id, name, population, class, county, seat
'''
import pandas as pd
import csv
import sqlite3

def main():

    # set database and csv file names
    database = "citycounty.db"
    county_data = "data/county2022.csv"
    city_data = "data/city2022.csv"

    create_database(database)

    create_county_table(database, county_data)

    create_city_table(database, city_data)

    add_seat(database, county_data, city_data)


def create_database(database):

    # create the database file and city/county tables
    try:
        with sqlite3.connect(database) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS county (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL UNIQUE,
                    population INTEGER NOT NULL,
                    class TEXT,
                    township TEXT DEFAULT "No",
                    seat TEXT
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS city (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL UNIQUE,
                    population INTEGER NOT NULL,
                    class TEXT NOT NULL,
                    county TEXT NOT NULL,
                    seat TEXT
                )
            ''')

            conn.commit() # Commit changes to the database
        print(f"Database {database} created or connected successfully.")
    except sqlite3.Error as e:
        print(f"Error connecting to or creating database: {e}")

def create_county_table(database, county_data):

    # load county data to county table
    try:
        # Read CSV into pandas DataFrame
        df = pd.read_csv(county_data)

        # Connect to SQLite database
        conn = sqlite3.connect(database)

        # Write DataFrame to SQLite table
        table_name = "county"
        df.to_sql(table_name, conn, if_exists='replace', index=False) # 'replace' will overwrite if table exists

        print(f"Data from {county_data} successfully loaded into {table_name} in {database} using pandas.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.commit()
            conn.close()

def create_city_table(database, city_data):

    # load city data to city table
    try:
        # Read CSV into pandas DataFrame
        df = pd.read_csv(city_data)

        # Connect to SQLite database
        conn = sqlite3.connect(database)

        # Write DataFrame to SQLite table
        table_name = "city"
        df.to_sql(table_name, conn, if_exists='replace', index=False) # 'replace' will overwrite if table exists

        print(f"Data from {city_data} successfully loaded into {table_name} in {database} using pandas.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.commit()
            conn.close()

def add_seat(database, county_data, city_data):

    # add "Yes" to "seat" columan in city table if that city is the county seat
    try:
        df_county = pd.read_csv(county_data)
        df_city = pd.read_csv(city_data)
        conn = sqlite3.connect(database)
        c = conn.cursor()

        # Iterating over rows
        count = 0
        for index, row in df_county.iterrows():
            if not pd.isnull(row["Seat"]):
                city_name = row["Seat"]
                county_name = row["Name"]
                print(county_name, city_name)
                stm = f"UPDATE city SET Seat = 'Yes' WHERE Name = '{city_name}'"
                c.execute(stm)
                count += 1

        print(count)


    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.commit()
            conn.close()
    

if __name__ == "__main__":
    main()