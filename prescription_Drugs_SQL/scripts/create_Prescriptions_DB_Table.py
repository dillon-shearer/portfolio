import sqlite3
import os

# Ensure the directory exists
os.makedirs('prescription_Drugs_SQL/data', exist_ok=True)

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

# Function to create the prescriptions table
def create_table(conn):
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS prescriptions (
        Prscrbr_NPI TEXT,
        Prscrbr_Type TEXT,
        Brnd_Name TEXT,
        Gnrc_Name TEXT,
        Tot_Clms NUMERIC,
        Tot_Day_Suply NUMERIC,
        Tot_Drug_Cst NUMERIC,
        Tot_Benes NUMERIC,
        Prscrbr_State_Abrvtn TEXT,
        GE65_Tot_Clms NUMERIC,
        UNIQUE(Prscrbr_NPI, Brnd_Name)
    );
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        conn.commit()
        print("Table created successfully.")
    except sqlite3.Error as e:
        print(e)

# Create the table
if conn is not None:
    create_table(conn)
else:
    print("Error! Cannot create the database connection.")

# Close the connection
conn.close()
