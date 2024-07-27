import pandas as pd
import requests
import sqlite3
import os
import zipfile
import io
import ctypes
import sys
import shutil

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def download_and_extract_zip(url, extract_to):
    response = requests.get(url)
    if response.ok:
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            z.extractall(extract_to)
            print(f"Extracted files to {extract_to}")
            for root, dirs, files in os.walk(extract_to):
                for file in files:
                    if file.endswith('.csv'):
                        return os.path.join(root, file)
    else:
        print(f"Failed to download ZIP file. Status code:", response.status_code)
        return None

def insert_data_to_db(db_conn, df):
    df.columns = [col.strip() for col in df.columns]

    expected_columns = ['Prscrbr_NPI', 'Prscrbr_Last_Org_Name', 'Prscrbr_First_Name', 'Prscrbr_City', 'Prscrbr_State_Abrvtn',
                        'Prscrbr_State_FIPS', 'Prscrbr_Type', 'Prscrbr_Type_Src', 'Brnd_Name', 'Gnrc_Name',
                        'Tot_Clms', 'Tot_30day_Fills', 'Tot_Day_Suply', 'Tot_Drug_Cst', 'Tot_Benes', 'GE65_Sprsn_Flag',
                        'GE65_Tot_Clms', 'GE65_Tot_30day_Fills', 'GE65_Tot_Drug_Cst', 'GE65_Tot_Day_Suply',
                        'GE65_Bene_Sprsn_Flag', 'GE65_Tot_Benes']

    for col in expected_columns:
        if col not in df.columns:
            df[col] = None

    df = df[expected_columns]
    data_tuples = list(df.itertuples(index=False, name=None))

    insert_query = '''
        INSERT OR REPLACE INTO prescriptions (
            Prscrbr_NPI, Prscrbr_Last_Org_Name, Prscrbr_First_Name, Prscrbr_City, Prscrbr_State_Abrvtn,
            Prscrbr_State_FIPS, Prscrbr_Type, Prscrbr_Type_Src, Brnd_Name, Gnrc_Name,
            Tot_Clms, Tot_30day_Fills, Tot_Day_Suply, Tot_Drug_Cst, Tot_Benes, GE65_Sprsn_Flag,
            GE65_Tot_Clms, GE65_Tot_30day_Fills, GE65_Tot_Drug_Cst, GE65_Tot_Day_Suply,
            GE65_Bene_Sprsn_Flag, GE65_Tot_Benes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''

    try:
        cursor = db_conn.cursor()
        total_inserted = 0
        duplicates = 0

        for i, record in enumerate(data_tuples, start=1):
            try:
                cursor.execute(insert_query, record)
            except sqlite3.IntegrityError as e:
                duplicates += 1
            if i % 100 == 0 or i == len(data_tuples):
                db_conn.commit()
                total_inserted += 100 if i % 100 == 0 else i % 100
                sys.stdout.flush()

        return total_inserted, duplicates
    except sqlite3.Error as e:
        print(f"Error inserting data: {e}")
        return 0, 0

def download_data(url, db_file):
    extract_to = 'prescription_Drugs_SQL/data/extracted'
    os.makedirs(extract_to, exist_ok=True)

    csv_file_path = download_and_extract_zip(url, extract_to)

    if csv_file_path:
        conn = sqlite3.connect(db_file)
        chunk_size = 10000
        total_inserted = 0
        total_duplicates = 0

        clear_screen()

        for chunk in pd.read_csv(csv_file_path, low_memory=False, chunksize=chunk_size):
            inserted, duplicates = insert_data_to_db(conn, chunk)
            total_inserted += inserted
            total_duplicates += duplicates
            print(f"\rTotal inserted so far: {total_inserted}.", end="")

        conn.close()
        print(f"\nData has been downloaded and saved to '{db_file}'")

        shutil.rmtree(extract_to)
        print(f"Removed extracted files and folder '{extract_to}'")
        print(f"Duplicates: {total_duplicates}.")
    else:
        print("No CSV file found in the extracted content.")

def prevent_sleep():
    if os.name == 'nt':
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000002)
    elif os.name == 'posix':
        os.system('caffeinate &')

data_url = 'https://data.cms.gov/sites/default/files/dataset_zips/93464ebcc251a36ee1ff4b6095f3fbfb/Medicare%20Part%20D%20Prescribers%20-%20by%20Provider%20and%20Drug.zip'
os.makedirs('prescription_Drugs_SQL/data', exist_ok=True)
db_file = 'prescription_Drugs_SQL/data/medicare_part_d_prescriptions.db'
prevent_sleep()
download_data(data_url, db_file)