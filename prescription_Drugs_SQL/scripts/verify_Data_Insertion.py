import pandas as pd
import sqlite3
import os

# Path to the SQLite database file
db_file = os.path.abspath('prescription_Drugs_SQL/data/medicare_part_d_prescriptions.db')

# Function to create a connection to the SQLite database
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to the database {db_file}")
    except sqlite3.Error as e:
        print(f"Error: {e}")
    return conn

# Create a database connection
conn = create_connection(db_file)

# Function to fetch all records
def fetch_all_records(conn):
    try:
        query = "SELECT * FROM prescriptions"
        df = pd.read_sql_query(query, conn)
        return df
    except sqlite3.Error as e:
        print(e)

# Fetch and display all records
df_all_records = fetch_all_records(conn)
if df_all_records is not None:
    print(df_all_records.head())

# Close the database connection
conn.close()