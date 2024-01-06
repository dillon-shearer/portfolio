#!/usr/bin/env python
# coding: utf-8

# ##### Import Libraries 

# In[15]:


import pandas as pd
import numpy as np

# ##### Load dataframe from 1_data_Acquisition output (data/RAW_2022_SAIPE_DATA.xlsx)

# In[16]:


data_filepath = f'../census_Poverty/data/RAW_2022_SAIPE_DATA.xlsx'
df = pd.read_excel(data_filepath)

# ##### Check dataframe once more

# In[17]:


df.head()

# ----
# Here are the steps which I will be following in this data cleaning/pre-processing/validation stage:
# ##### **1** - Rename/fix headers.
# - Headers are actually located in row 4, and I will combine them with additional header detail from row 3.
# - Rename row 1, drop rows 2-4.
# - Naming as follows:
#     - Table with column headers in rows 3 and 4 -> STATE_FIPS_ID
#     - Unnamed: 1 -> POSTAL_CODE
#     - Unnamed: 2 -> REGION_NAME
#     - Unnamed: 3 -> ALL_AGES_POVERTY_ESTIMATE
#     - Unnamed: 4 -> ALL_AGES_90_CI_LOWER_BOUND
#     - Unnamed: 5 -> ALL_AGES_90_CI_UPPER_BOUND
#     - Unnamed: 6 -> ALL_AGES_POVERTY_PERCENT
#     - Unnamed: 7 -> ALL_AGES_90_CI_LOWER_PERCENT
#     - Unnamed: 8 -> ALL_AGES_90_CI_UPPER_PERCENT
#     - Unnamed: 9 -> 0_17_POVERTY_ESTIMATE
#     - Unnamed: 10 -> 0_17_90_CI_LOWER_BOUND
#     - Unnamed: 11 -> 0_17_90_CI_UPPER_BOUND
#     - Unnamed: 12 -> 0_17_POVERTY_PERCENT
#     - Unnamed: 13 -> 0_17_90_CI_LOWER_PERCENT
#     - Unnamed: 14 -> 0_17_90_CI_UPPER_PERCENT
#     - Unnamed: 15 -> 5_17_POVERTY_ESTIMATE
#     - Unnamed: 16 -> 5_17_90_CI_LOWER_BOUND
#     - Unnamed: 17 -> 5_17_90_CI_UPPER_BOUND
#     - Unnamed: 18 -> 5_17_POVERTY_PERCENT
#     - Unnamed: 19 -> 5_17_90_CI_LOWER_PERCENT
#     - Unnamed: 20 -> 5_17_90_CI_UPPER_PERCENT
#     - Unnamed: 21 -> MEDIAN_HOUSEHOLD_INCOME
#     - Unnamed: 22 -> MEDIAN_HOUSEHOLD_INCOME_90_CI_LOWER_BOUND
#     - Unnamed: 23 -> MEDIAN_HOUSEHOLD_INCOME_90_CI_UPPER_BOUND
#     - Unnamed: 24 -> 0_4_POVERTY_ESTIMATE
#     - Unnamed: 25 -> 0_4_90_CI_LOWER_BOUND
#     - Unnamed: 26 -> 0_4_90_CI_UPPER_BOUND
#     - Unnamed: 27 -> 0_4_POVERTY_PERCENT
#     - Unnamed: 28 -> 0_4_CI_LOWER_PERCENT
#     - Unnamed: 29 -> 0_4_UPPER_PERCENT

# In[18]:


new_headers = {
    'Table with column headers in rows 3 and 4': 'STATE_FIPS_ID',
    'Unnamed: 1': 'COUNTY_ID',
    'Unnamed: 2': 'POSTAL_CODE',
    'Unnamed: 3': 'REGION_NAME',
    'Unnamed: 4': 'ALL_AGES_POVERTY_ESTIMATE',
    'Unnamed: 5': 'ALL_AGES_90_CI_LOWER_BOUND',
    'Unnamed: 6': 'ALL_AGES_90_CI_UPPER_BOUND',
    'Unnamed: 7': 'ALL_AGES_POVERTY_PERCENT',
    'Unnamed: 8': 'ALL_AGES_90_CI_LOWER_PERCENT',
    'Unnamed: 9': 'ALL_AGES_90_CI_UPPER_PERCENT',
    'Unnamed: 10': '0_17_POVERTY_ESTIMATE',
    'Unnamed: 11': '0_17_90_CI_LOWER_BOUND',
    'Unnamed: 12': '0_17_90_CI_UPPER_BOUND',
    'Unnamed: 13': '0_17_POVERTY_PERCENT',
    'Unnamed: 14': '0_17_90_CI_LOWER_PERCENT',
    'Unnamed: 15': '0_17_90_CI_UPPER_PERCENT',
    'Unnamed: 16': '5_17_POVERTY_ESTIMATE',
    'Unnamed: 17': '5_17_90_CI_LOWER_BOUND',
    'Unnamed: 18': '5_17_90_CI_UPPER_BOUND',
    'Unnamed: 19': '5_17_POVERTY_PERCENT',
    'Unnamed: 20': '5_17_90_CI_LOWER_PERCENT',
    'Unnamed: 21': '5_17_90_CI_UPPER_PERCENT',
    'Unnamed: 22': 'MEDIAN_HOUSEHOLD_INCOME',
    'Unnamed: 23': 'MEDIAN_HOUSEHOLD_INCOME_90_CI_LOWER_BOUND',
    'Unnamed: 24': 'MEDIAN_HOUSEHOLD_INCOME_90_CI_UPPER_BOUND',
    'Unnamed: 25': '0_4_POVERTY_ESTIMATE',
    'Unnamed: 26': '0_4_90_CI_LOWER_BOUND',
    'Unnamed: 27': '0_4_90_CI_UPPER_BOUND',
    'Unnamed: 28': '0_4_POVERTY_PERCENT',
    'Unnamed: 29': '0_4_CI_LOWER_PERCENT',
    'Unnamed: 30': '0_4_UPPER_PERCENT'
}

# Rename the headers based on the dictionary
df.columns = df.columns.map(new_headers)

# Drop rows 1 and 2
df = df.drop([0, 1, 2])

# Reset the index
df = df.reset_index(drop=True)

# Double check result.

# In[19]:


df.head()

# -----
# ##### **2** - Add State/National/County identifier column

# In[20]:


# Define the function to categorize each row
def categorize(row):
    if row['STATE_FIPS_ID'] == '00' and row['COUNTY_ID'] == '000':
        return 'NATIONAL'
    elif row['STATE_FIPS_ID'] != '00' and row['COUNTY_ID'] == '000':
        return 'STATE'
    else:
        return 'COUNTY'

# Apply the function and create the new column
df['REGION_TYPE'] = df.apply(categorize, axis=1)

# Check results - expected is 1 national, 51 state, and 3144 county

# In[21]:


# Count the occurrences of each value in the 'REGION_TYPE' column
counts = df['REGION_TYPE'].value_counts()

# Display the counts
print(counts)

# ----
# ##### **3** - Validate any abnormal data.

# In[22]:


df.info()

# -----
# ##### **4** - Clean '.' values to NaN

# In[23]:


# Replace '.' with NaN
df.replace('.', pd.NA, inplace=True)

# -----
# ##### **5** - Update data types for necessary columns

# In[24]:


df.dtypes

# In[25]:


# Create a dictionary mapping from current dtypes in df to the desired dtypes
dtype_map = {
    'POSTAL_CODE': object,
    'REGION_NAME': object,
    'ALL_AGES_POVERTY_ESTIMATE': int,
    'ALL_AGES_90_CI_LOWER_BOUND': int,
    'ALL_AGES_90_CI_UPPER_BOUND': int,
    'ALL_AGES_POVERTY_PERCENT': float,
    'ALL_AGES_90_CI_LOWER_PERCENT': float,
    'ALL_AGES_90_CI_UPPER_PERCENT': float,
    '0_17_POVERTY_ESTIMATE': int,
    '0_17_90_CI_LOWER_BOUND': int,
    '0_17_90_CI_UPPER_BOUND': int,
    '0_17_POVERTY_PERCENT': float,
    '0_17_90_CI_LOWER_PERCENT': float,
    '0_17_90_CI_UPPER_PERCENT': float,
    '5_17_POVERTY_ESTIMATE': int,
    '5_17_90_CI_LOWER_BOUND': int,
    '5_17_90_CI_UPPER_BOUND': int,
    '5_17_POVERTY_PERCENT': float,
    '5_17_90_CI_LOWER_PERCENT': float,
    '5_17_90_CI_UPPER_PERCENT': float,
    'MEDIAN_HOUSEHOLD_INCOME': int,
    'MEDIAN_HOUSEHOLD_INCOME_90_CI_LOWER_BOUND': int,
    'MEDIAN_HOUSEHOLD_INCOME_90_CI_UPPER_BOUND': int,
    '0_4_POVERTY_ESTIMATE': int,
    '0_4_90_CI_LOWER_BOUND': int,
    '0_4_90_CI_UPPER_BOUND': int,
    '0_4_POVERTY_PERCENT': float,
    '0_4_CI_LOWER_PERCENT': float,
    '0_4_UPPER_PERCENT': float,
    'REGION_TYPE': object
}

# Create a list of columns for each type
int_columns = [col for col, dtype in dtype_map.items() if dtype == int]
float_columns = [col for col, dtype in dtype_map.items() if dtype == float]

# Round float columns to 1 decimal place and convert to appropriate data types
df[float_columns] = df[float_columns].round(1).astype('Float64')
df[int_columns] = df[int_columns].astype('Int64')  # Use 'Int64' (capital "I") to handle NaN values as well.

# Check the result
df.dtypes

# ##### **6** - Create FIPS code (STATE_FIPS_ID + POSTAL_CODE) for mapping

# In[26]:


# Combining 'STATE_FIPS_ID' and 'POSTAL_CODE' to create a 5-digit FIPS code
df['FIPS_CODE'] = df['STATE_FIPS_ID'] + df['COUNTY_ID']
df

# ----
# ##### **7** - Send data back to Excel (census_Poverty/data/CLEANED_2022_SAIPE_DATA.xlsx)

# In[27]:


out_filepath = f'./data/CLEANED_2022_SAIPE_DATA.xlsx'
df.to_excel(out_filepath, index=False)
