import sqlite3
import os
import gzip
import shutil

def vacuum_database(db_file):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("VACUUM")
        conn.commit()
        conn.close()
        print(f"Database {db_file} has been vacuumed.")
    except sqlite3.Error as e:
        print(f"Error vacuuming database: {e}")

def compress_file(input_file, output_file):
    with open(input_file, 'rb') as f_in, gzip.open(output_file, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
    print(f"Database {input_file} has been compressed to {output_file}.")

def main():
    db_file = 'prescription_Drugs_SQL/data/medicare_part_d_prescriptions.db'
    compressed_file = 'prescription_Drugs_SQL/data/medicare_part_d_prescriptions.db.gz'

    # Vacuum the database to compact it
    vacuum_database(db_file)

    # Compress the database file
    compress_file(db_file, compressed_file)

    os.remove(db_file)

if __name__ == "__main__":
    main()