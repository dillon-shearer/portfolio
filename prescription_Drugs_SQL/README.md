# **Dillon Shearer** || Prescriptions Database Project

## Overview

This project involves creating and analyzing a prescriptions database to provide insights into prescription patterns, costs, and potential issues related to specific medications, such as opioids. The project includes scripts to create and populate the database, verify data insertion, and perform exploratory data analysis (EDA).

## Project Structure

The project consists of the following files:

1. `1_create_Prescriptions_DB_Table.py`: Script to create the prescriptions database table.
2. `2_fill_Prescriptions_DB_Table.py`: Script to fill the prescriptions database table with data.
3. `3_verify_Data_Insertion.py`: Script to verify the data insertion into the prescriptions database.
4. `4_prescriptions_EDA.ipynb`: Jupyter notebook to perform exploratory data analysis on the prescriptions database.

## Scripts

### 1. Create Prescriptions Database Table

**File**: `1_create_Prescriptions_DB_Table.py`

This script creates the `prescriptions` table in the SQLite database. The table includes the following columns:

- `Prscrbr_NPI`: National Provider Identifier for the performing provider on the claim.
- `Prscrbr_Last_Org_Name`: Last name or organization name of the provider.
- `Prscrbr_First_Name`: First name of the provider.
- `Prscrbr_City`: City where the provider is located.
- `Prscrbr_State_Abrvtn`: State abbreviation where the provider is located.
- `Prscrbr_State_FIPS`: FIPS code for the provider's state.
- `Prscrbr_Type`: Specialty type of the provider.
- `Prscrbr_Type_Src`: Source of the provider specialty.
- `Brnd_Name`: Brand name of the drug.
- `Gnrc_Name`: Generic name of the drug.
- `Tot_Clms`: Total number of Medicare Part D claims.
- `Tot_30day_Fills`: Total number of standardized 30-day fills.
- `Tot_Day_Suply`: Total number of days supplied.
- `Tot_Drug_Cst`: Total drug cost.
- `Tot_Benes`: Total number of Medicare beneficiaries.
- `GE65_Sprsn_Flag`: Reason for suppression of data for beneficiaries age 65 and older.
- `GE65_Tot_Clms`: Total number of claims for beneficiaries age 65 and older.
- `GE65_Tot_30day_Fills`: Total number of standardized 30-day fills for beneficiaries age 65 and older.
- `GE65_Tot_Drug_Cst`: Total drug cost for beneficiaries age 65 and older.
- `GE65_Tot_Day_Suply`: Total number of days supplied for beneficiaries age 65 and older.
- `GE65_Bene_Sprsn_Flag`: Reason for suppression of data for beneficiaries age 65 and older.
- `GE65_Tot_Benes`: Total number of beneficiaries age 65 and older.

### 2. Fill Prescriptions Database Table

**File**: `2_fill_Prescriptions_DB_Table.py`

This script downloads the prescriptions dataset, extracts the CSV file, and populates the `prescriptions` table in the SQLite database. It processes the data in chunks to handle large datasets efficiently and provides progress updates during the insertion process.

### 3. Verify Data Insertion

**File**: `3_verify_Data_Insertion.py`

This script verifies the data insertion by querying the total row count from the `prescriptions` table. It ensures that the number of inserted rows matches the expected count from the data source.

### 4. Prescriptions EDA

**File**: `4_prescriptions_EDA.ipynb`

This Jupyter notebook performs exploratory data analysis on the prescriptions database. The analysis includes:

1. **Top Prescribed Drugs**: Identifies the most commonly prescribed drugs based on the total number of claims.
2. **Prescriptions by State**: Shows the distribution of prescriptions across different states.
3. **Top Prescribers**: Lists the top prescribers based on the total number of claims.
4. **Total Cost by Drug**: Displays the total cost for each drug.
5. **Average Cost per Prescription by Drug**: Calculates the average cost per prescription for each drug.
6. **Prescriptions for Beneficiaries Age 65 and Older**: Provides the distribution of prescriptions for beneficiaries aged 65 and older.
7. **Baseline Stats for Specific Drugs**: Allows for the analysis of specific drugs of interest compared to standard medications.

## How to Use

1. **Create the Prescriptions Database Table**:
   Run the `1_create_Prescriptions_DB_Table.py` script to create the `prescriptions` table in the SQLite database.

   ```sh
   python 1_create_Prescriptions_DB_Table.py

2. **Fill the Prescriptions Database Table**:
    Run the `2_fill_Prescriptions_DB_Table.py` script to download and populate the prescriptions data into the database.

    ```sh
    python 2_fill_Prescriptions_DB_Table.py

3. **Verify Data Insertion**:
    Run the `3_verify_Data_Insertion.py` script to verify the data insertion.

    ```sh
    python 3_verify_Data_Insertion.py

4. **Perform Exploratory Data Analysis**:
    Open and run the `4_prescriptions_EDA.ipynb` Jupyter notebook to perform the EDA.

    ```sh
    jupyter notebook 4_prescriptions_EDA.ipyn
