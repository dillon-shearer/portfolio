import pandas as pd
import requests
import sqlite3
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import ctypes
from tqdm import tqdm

# File to store the current offset and total inserted records
offset_file = 'prescription_Drugs_SQL/data/current_offset.txt'

# Function to fetch a single batch of data
def fetch_batch(url, offset, limit):
    response = requests.get(f"{url}?$limit={limit}&$offset={offset}")
    if response.ok:
        return response.json()
    else:
        print(f"Failed to download data at offset {offset}. Status code:", response.status_code)
        return []

# Function to insert data into SQLite database
def insert_data_to_db(db_conn, data):
    df = pd.DataFrame(data)
    df.columns = [col.strip() for col in df.columns]  # Ensure no leading/trailing spaces
    df = df[['Prscrbr_NPI', 'Prscrbr_Type', 'Brnd_Name', 'Gnrc_Name', 'Tot_Clms',
             'Tot_Day_Suply', 'Tot_Drug_Cst', 'Tot_Benes', 'Prscrbr_State_Abrvtn', 'GE65_Tot_Clms']]

    # Convert dataframe to list of tuples for insertion
    data_tuples = list(df.itertuples(index=False, name=None))

    # Prepare the SQL query for insertion with conflict resolution
    insert_query = '''
        INSERT OR REPLACE INTO prescriptions (
            Prscrbr_NPI, Prscrbr_Type, Brnd_Name, Gnrc_Name, Tot_Clms,
            Tot_Day_Suply, Tot_Drug_Cst, Tot_Benes, Prscrbr_State_Abrvtn, GE65_Tot_Clms
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''

    try:
        db_conn.executemany(insert_query, data_tuples)
        db_conn.commit()
        return len(data_tuples)
    except sqlite3.Error as e:
        print(f"Error inserting data: {e}")
        return 0

# Function to download data using concurrent requests and pipe into SQLite DB
def download_data(url, db_file):
    limit = 5000  # Increased batch size to 5000
    max_workers = 10  # Number of concurrent threads

    # Read the last offset and total inserted from file
    if os.path.exists(offset_file):
        with open(offset_file, 'r') as f:
            offset, total_inserted = map(int, f.read().strip().split(','))
    else:
        offset = 0
        total_inserted = 0

    # Connect to SQLite database
    conn = sqlite3.connect(db_file)

    with tqdm(total=total_inserted, desc="Progress", unit=" records") as pbar:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            while True:
                future = executor.submit(fetch_batch, url, offset, limit)
                futures.append(future)
                offset += limit

                if len(futures) % max_workers == 0:
                    for future in as_completed(futures):
                        data = future.result()
                        if data:
                            inserted = insert_data_to_db(conn, data)
                            total_inserted += inserted
                            pbar.update(inserted)

                            # Write the new offset and total inserted to file
                            with open(offset_file, 'w') as f:
                                f.write(f"{offset},{total_inserted}")
                        futures.remove(future)

                    # Check if last batch fetched no data
                    if not data:
                        break

            # Process any remaining futures
            for future in as_completed(futures):
                data = future.result()
                if data:
                    inserted = insert_data_to_db(conn, data)
                    total_inserted += inserted
                    pbar.update(inserted)

                    # Write the new offset and total inserted to file
                    with open(offset_file, 'w') as f:
                        f.write(f"{offset},{total_inserted}")

    conn.close()
    print(f"Data has been downloaded and saved to '{db_file}'")

# Function to prevent the system from sleeping
def prevent_sleep():
    if os.name == 'nt':  # Windows
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000002)
    elif os.name == 'posix':  # macOS
        os.system('caffeinate &')

# URL to the dataset
data_url = 'https://data.cms.gov/data-api/v1/dataset/9552739e-3d05-4c1b-8eff-ecabf391e2e5/data'

# Directory for storing the database
os.makedirs('prescription_Drugs_SQL/data', exist_ok=True)

# SQLite database file
db_file = 'prescription_Drugs_SQL/data/medicare_part_d_prescriptions.db'

# Prevent the system from sleeping
prevent_sleep()

# Download and save the data
download_data(data_url, db_file)