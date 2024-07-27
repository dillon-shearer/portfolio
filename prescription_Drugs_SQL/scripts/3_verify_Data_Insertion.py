import sqlite3

def count_rows_in_table(db_file, table_name):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        query = f"SELECT COUNT(*) FROM {table_name}"
        cursor.execute(query)
        count = cursor.fetchone()[0]
        conn.close()
        return count
    except sqlite3.Error as e:
        print(f"Error counting rows: {e}")
        return 0

# Path to SQLite database file
db_file = 'prescription_Drugs_SQL/data/medicare_part_d_prescriptions.db'
table_name = 'prescriptions'

# Count the rows in the prescriptions table
row_count = count_rows_in_table(db_file, table_name)
print(f"Total row count in the '{table_name}' table: {row_count}")