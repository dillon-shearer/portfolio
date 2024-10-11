import requests
import pandas as pd
import os

# Define your API key and API endpoint
api_key = ""  # Replace with your actual API key
base_url = "https://api.census.gov/data/{year}/acs/acs1"

# Define the variables of interest (income, race, ethnicity, sex, Gini Index, education attainment, etc.)
variables = [
    "B19013_001E",  # Median Household Income (All)
    "B19013A_001E", # Median Household Income: White alone
    "B19013B_001E", # Median Household Income: Black or African American alone
    "B19013C_001E", # Median Household Income: American Indian and Alaska Native alone
    "B19013D_001E", # Median Household Income: Asian alone
    "B19013E_001E", # Median Household Income: Native Hawaiian and Other Pacific Islander alone
    "B19013F_001E", # Median Household Income: Some Other Race alone
    "B19013G_001E", # Median Household Income: Two or More Races
    "B19013H_001E", # Median Household Income: White alone, not Hispanic or Latino
    "B19013I_001E", # Median Household Income: Hispanic or Latino origin
    "B19083_001E",  # Gini Index (Income Inequality Measure)
    "B19113_001E",  # Median Family Income (All)
    # Educational attainment breakdowns (all levels)
    "B15003_001E",  # Total Population (Education)
    "B15003_017E",  # High School Graduate
    "B15003_018E",  # Some College (no degree)
    "B15003_019E",  # Associate's Degree
    "B15003_022E",  # Bachelor's Degree
    "B15003_025E",  # Graduate or Professional Degree
    # Gender-based breakdowns for income
    "B20002_001E",  # Median Earnings (All)
    "B20002_002E",  # Median Earnings (Male)
    "B20002_003E",  # Median Earnings (Female)
]

# Define the years to pull data for
years = [2019, 2021, 2022]

# Create a list to hold the combined data for all years
combined_data = []

# Loop over each year and pull data
for year in years:
    # Loop over geographies: state and national
    for geo, geo_name in [("state:*", "States"), ("us:1", "National")]:
        # Create the API request URL
        api_url = base_url.format(year=year)

        # Define parameters for the API request
        params = {
            "get": ",".join(variables),
            "for": geo,
            "key": api_key
        }

        # Make the API request
        response = requests.get(api_url, params=params)

        # Check for successful API response
        if response.status_code == 200:
            print(f"Data successfully retrieved for {year} - {geo_name}.")
            data = response.json()

            # Convert to a DataFrame and add a 'Year' column
            df = pd.DataFrame(data[1:], columns=data[0])
            df['Year'] = year

            # Add a 'Geo' column to identify state or national data
            df['Geo'] = geo_name

            # Append the DataFrame to the list
            combined_data.append(df)
        else:
            print(f"Error: Failed to retrieve data for {year} - {geo_name}. Status code {response.status_code}")

# Combine all data into a single DataFrame
income_df = pd.concat(combined_data, ignore_index=True)

# Map state codes to state names
state_mapping = {
    '01': 'Alabama', '02': 'Alaska', '04': 'Arizona', '05': 'Arkansas', '06': 'California',
    '08': 'Colorado', '09': 'Connecticut', '10': 'Delaware', '11': 'District of Columbia',
    '12': 'Florida', '13': 'Georgia', '15': 'Hawaii', '16': 'Idaho', '17': 'Illinois',
    '18': 'Indiana', '19': 'Iowa', '20': 'Kansas', '21': 'Kentucky', '22': 'Louisiana',
    '23': 'Maine', '24': 'Maryland', '25': 'Massachusetts', '26': 'Michigan', '27': 'Minnesota',
    '28': 'Mississippi', '29': 'Missouri', '30': 'Montana', '31': 'Nebraska', '32': 'Nevada',
    '33': 'New Hampshire', '34': 'New Jersey', '35': 'New Mexico', '36': 'New York', '37': 'North Carolina',
    '38': 'North Dakota', '39': 'Ohio', '40': 'Oklahoma', '41': 'Oregon', '42': 'Pennsylvania',
    '44': 'Rhode Island', '45': 'South Carolina', '46': 'South Dakota', '47': 'Tennessee',
    '48': 'Texas', '49': 'Utah', '50': 'Vermont', '51': 'Virginia', '53': 'Washington',
    '54': 'West Virginia', '55': 'Wisconsin', '56': 'Wyoming'
}

# Map state codes to state names, or set 'National' for US data
def get_state_name(row):
    if row['Geo'] == 'States':
        return state_mapping.get(row['state'], 'Unknown')
    elif row['Geo'] == 'National':
        return 'National'
    else:
        return 'Unknown'

income_df['State'] = income_df.apply(get_state_name, axis=1)

# Reorder columns for clarity
columns = [
    "State", "Year", "B19013_001E", "B19013A_001E", "B19013B_001E", "B19013C_001E", "B19013D_001E", "B19013E_001E", 
    "B19013F_001E", "B19013G_001E", "B19013H_001E", "B19013I_001E", "B19083_001E", "B19113_001E",
    "B20002_001E", "B20002_002E", "B20002_003E", "B15003_001E", "B15003_017E", "B15003_018E", 
    "B15003_019E", "B15003_022E", "B15003_025E"
]

# Keep only relevant columns and rename them
income_df = income_df[columns]
income_df.columns = [
    "State", "Year", "Median_Income_All", "Median_Income_White", "Median_Income_Black", "Median_Income_AIAN", 
    "Median_Income_Asian", "Median_Income_NHPI", "Median_Income_Other", "Median_Income_Two_Races", 
    "Median_Income_White_Non_Hispanic", "Median_Income_Hispanic", "Gini_Index", "Median_Family_Income", 
    "Median_Earnings_All", "Median_Earnings_Male", "Median_Earnings_Female", "Total_Population_Education", 
    "High_School_Graduate", "Some_College_No_Degree", "Associates_Degree", "Bachelors_Degree", "Graduate_Degree"
]

# Save the DataFrame to a CSV in the appropriate raw data folder
output_dir = os.path.join(os.getcwd(), "Society_in_Numbers", "data", "raw")
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, "income_inequality_race_ethnicity_gender_education_gini_2019_2022.csv")
income_df.to_csv(output_file, index=False)

print(f"Data saved to {output_file}")