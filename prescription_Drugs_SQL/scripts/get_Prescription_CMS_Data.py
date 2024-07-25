import pandas as pd
import requests
import concurrent.futures

# Function to fetch a single batch of data
def fetch_batch(url, offset, limit):
    response = requests.get(f"{url}?$limit={limit}&$offset={offset}")
    if response.ok:
        return response.json()
    else:
        print(f"Failed to download data at offset {offset}. Status code:", response.status_code)
        return []

# Function to download data using concurrent requests
def download_data(url, csv_file):
    all_data = []
    offset = 0
    limit = 1000
    max_workers = 10  # Number of concurrent threads

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        while True:
            future = executor.submit(fetch_batch, url, offset, limit)
            futures.append(future)
            offset += limit

            # Check if the last batch was empty
            if futures[-1].result() == []:
                break

            # Print progress every 10,000 records
            if len(all_data) % 10000 < limit:
                print(f"Requested offset {offset}...")

        for future in concurrent.futures.as_completed(futures):
            data = future.result()
            if data:
                all_data.extend(data)
                if len(all_data) % 10000 < limit:
                    print(f"Downloaded {len(all_data)} records so far...")

    # Convert the list of data to a DataFrame and save as CSV
    df = pd.DataFrame(all_data)
    df.to_csv(csv_file, index=False)
    print(f"Data has been downloaded and saved to '{csv_file}'")

# URL to the dataset
data_url = 'https://data.cms.gov/data-api/v1/dataset/9552739e-3d05-4c1b-8eff-ecabf391e2e5/data'

# CSV file to save the data
csv_file = 'data/medicare_part_d_prescriptions.csv'

# Download and save the data
download_data(data_url, csv_file)