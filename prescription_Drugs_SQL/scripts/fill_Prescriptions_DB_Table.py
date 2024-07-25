import pandas as pd
import requests
import sqlite3
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import ctypes

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
    df.to_sql('prescriptions', db_conn, if_exists='append', index=False)
    return len(df)

# Function to download data using concurrent requests and pipe into SQLite DB
def download_data(url, db_file):
    offset = 0
    limit = 1000
    max_workers = 10  # Number of concurrent threads
    total_inserted = 0  # Keep track of the total number of records inserted

    # Connect to SQLite database
    conn = sqlite3.connect(db_file)

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
                        print(f"Total records downloaded and inserted so far: {total_inserted}")
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
                print(f"Total records downloaded and inserted so far: {total_inserted}")

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