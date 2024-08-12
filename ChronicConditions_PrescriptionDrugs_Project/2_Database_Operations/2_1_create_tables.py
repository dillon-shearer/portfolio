import os
import sqlite3

# Ensure the directory structure is correct
db_dir = os.path.join(os.getcwd(), 'ChronicConditions_PrescriptionDrugs_Project', 'data', 'db')
os.makedirs(db_dir, exist_ok=True)

# Create a connection to the SQLite database (this will create the database if it doesn't exist)
db_path = os.path.join(db_dir, 'chronic_conditions_prescriptions_database.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# SQL command to create tables
create_tables_sql = """
DROP TABLE IF EXISTS processed_cdc_data;
DROP TABLE IF EXISTS processed_cms_data;

CREATE TABLE processed_cdc_data (
    GEO_TYPE TEXT,
    GEO_VALUE TEXT,
    Measure TEXT,
    Measure_Short TEXT,
    Weighted_Average REAL,
    Total_Population INTEGER
);

CREATE TABLE processed_cms_data (
    GEO_TYPE TEXT,
    GEO_VALUE TEXT,
    Brnd_Name TEXT,
    Gnrc_Name TEXT,
    Tot_Clms INTEGER,
    Tot_Drug_Cst REAL,
    Tot_Benes INTEGER
);
"""

# Execute the SQL command
cursor.executescript(create_tables_sql)

# Commit and close the connection
conn.commit()
conn.close()

print(f"Database created and tables set up successfully at: {db_path}")