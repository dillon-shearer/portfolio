import sqlite3
import pandas as pd
import os

cwd = os.getcwd()

# Connect to the SQLite database
db_path = 'ChronicConditions_PrescriptionDrugs_Project/data/db/chronic_conditions_prescriptions_database.db'
conn = sqlite3.connect(db_path)

# Load and import CDC data
cdc_df = pd.read_csv('ChronicConditions_PrescriptionDrugs_Project/data/processed/processed_CDC_PLACES_data.csv')
cdc_df.to_sql('processed_cdc_data', conn, if_exists='replace', index=False)

# Load and import CMS data
cms_df = pd.read_csv('ChronicConditions_PrescriptionDrugs_Project/data/processed/processed_Medicare_Prescriptions_data.csv')
cms_df.to_sql('processed_cms_data', conn, if_exists='replace', index=False)

# Commit and close the connection
conn.commit()
conn.close()

print("Data imported successfully.")