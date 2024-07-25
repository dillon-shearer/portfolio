import sqlite3
import os

# Directory for storing the database
os.makedirs('prescription_Drugs_SQL/data', exist_ok=True)

# SQLite database file
db_file = 'prescription_Drugs_SQL/data/medicare_part_d_prescriptions.db'

# Connect to SQLite database
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Create the table with the correct schema
cursor.execute('''
    CREATE TABLE IF NOT EXISTS prescriptions (
        Prscrbr_NPI TEXT,
        Prscrbr_Last_Org_Name TEXT,
        Prscrbr_First_Name TEXT,
        Prscrbr_City TEXT,
        Prscrbr_State_Abrvtn TEXT,
        Prscrbr_State_FIPS TEXT,
        Prscrbr_Type TEXT,
        Prscrbr_Type_Src TEXT,
        Brnd_Name TEXT,
        Gnrc_Name TEXT,
        Tot_Clms TEXT,
        Tot_30day_Fills TEXT,
        Tot_Day_Suply TEXT,
        Tot_Drug_Cst TEXT,
        Tot_Benes TEXT,
        GE65_Sprsn_Flag TEXT,
        GE65_Tot_Clms TEXT,
        GE65_Tot_30day_Fills TEXT,
        GE65_Tot_Drug_Cst TEXT,
        GE65_Tot_Day_Suply TEXT,
        GE65_Bene_Sprsn_Flag TEXT,
        GE65_Tot_Benes TEXT
    )
''')
conn.commit()

# Close the connection
conn.close()

print(f"Database and table 'prescriptions' created successfully in '{db_file}'.")