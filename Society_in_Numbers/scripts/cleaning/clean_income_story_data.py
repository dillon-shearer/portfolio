import pandas as pd
import numpy as np
import os

# Define the file paths
input_file = "Society_in_Numbers/data/raw/raw_income_inequality_race_ethnicity_gender_education_gini.csv"
output_file = "Society_in_Numbers/data/clean/income_story_data_cleaned.csv"

# Load the dataset
df = pd.read_csv(input_file)

# Replace placeholder value -666666666 with NaN
df.replace(-666666666, np.nan, inplace=True)

# Ensure 'State' column is present and correctly set
df['State'] = df['State'].fillna('Unknown')

# Remove any duplicate rows based on 'State' and 'Year'
df = df.drop_duplicates(subset=['State', 'Year'])

# Remove any rows where 'State' is missing or invalid, but keep 'National'
df = df[(df['State'].notna()) & (df['State'] != 'Unknown')]

# Convert all the income and numeric columns to numeric (some might be strings)
numeric_columns = [
    "Median_Income_All", "Median_Income_White", "Median_Income_Black", "Median_Income_AIAN",
    "Median_Income_Asian", "Median_Income_NHPI", "Median_Income_Other", "Median_Income_Two_Races",
    "Median_Income_White_Non_Hispanic", "Median_Income_Hispanic", "Gini_Index",
    "Median_Family_Income", "Median_Earnings_All", "Median_Earnings_Male", "Median_Earnings_Female",
    "Total_Population_Education", "High_School_Graduate", "Some_College_No_Degree",
    "Associates_Degree", "Bachelors_Degree", "Graduate_Degree"
]

# Convert to numeric, forcing errors to NaN
df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

# Remove any rows where the income or key columns have too many NaN values
threshold = 0.5 * len(df.columns)  # Lowered threshold to 50%
df = df.dropna(thresh=threshold)

# Identify any remaining problematic rows (e.g., missing essential data like income or Gini)
df_cleaned = df.dropna(subset=["Median_Income_All", "Gini_Index", "State", "Year"])

# Final clean-up steps
# Strip leading and trailing spaces from all string columns if any
df_cleaned = df_cleaned.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

# Convert 'Year' to integer type
df_cleaned['Year'] = df_cleaned['Year'].astype(int)

# Sort the data by 'State' and 'Year'
df_cleaned = df_cleaned.sort_values(['State', 'Year'])

# Impute missing 2020 data using linear interpolation
# Define the years to include
desired_years = [2019, 2020, 2021, 2022]

# Function to interpolate missing years
def interpolate_years(group):
    group = group.set_index('Year').reindex(desired_years)
    # Interpolate numeric columns
    group[numeric_columns] = group[numeric_columns].interpolate(method='linear')
    # Fill 'State' column
    group['State'] = group['State'].fillna(method='ffill')
    group['State'] = group['State'].fillna(method='bfill')
    return group.reset_index()

# Apply the interpolation function to each State group
df_interpolated = df_cleaned.groupby('State', group_keys=False).apply(interpolate_years)

# Drop any remaining rows with missing essential data after interpolation
df_interpolated = df_interpolated.dropna(subset=["Median_Income_All", "Gini_Index", "State", "Year"])

# Save the cleaned and interpolated dataset to the clean data folder
output_dir = os.path.join("Society_in_Numbers", "data", "clean")
os.makedirs(output_dir, exist_ok=True)
df_interpolated.to_csv(output_file, index=False)

print(f"Data cleaning complete. Cleaned and interpolated data saved to {output_file}")
