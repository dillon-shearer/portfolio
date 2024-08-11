import sqlite3

# Connect to the SQLite database
db_path = 'ChronicConditions_PrescriptionDrugs_Project/data/db/chronic_conditions_prescriptions_database.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# SQL command to optimize the database
optimization_sql = """
CREATE INDEX idx_cdc_geo ON processed_cdc_data (GEO_TYPE, GEO_VALUE);
CREATE INDEX idx_cms_geo ON processed_cms_data (GEO_TYPE, GEO_VALUE);
CREATE INDEX idx_cdc_measure_short ON processed_cdc_data (Measure_Short);
CREATE INDEX idx_cms_gnrc_name ON processed_cms_data (Gnrc_Name);
"""

# Execute the SQL command
cursor.executescript(optimization_sql)

# Commit and close the connection
conn.commit()
conn.close()

print("Database optimized successfully.")