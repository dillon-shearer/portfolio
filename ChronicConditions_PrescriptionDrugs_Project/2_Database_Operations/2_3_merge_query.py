import sqlite3
import pandas as pd

# Connect to the SQLite database
db_path = 'ChronicConditions_PrescriptionDrugs_Project/data/db/chronic_conditions_prescriptions_database.db'
conn = sqlite3.connect(db_path)

# SQL query to merge CDC and CMS data using the correct condition-drug mapping
query_sql = """
WITH condition_drug_mapping AS (
    SELECT 'Diabetes' AS Measure_Short, 'Insulin' AS Gnrc_Name UNION ALL
    SELECT 'Diabetes', 'Metformin' UNION ALL
    SELECT 'Diabetes', 'Glipizide' UNION ALL
    SELECT 'Diabetes', 'Glyburide' UNION ALL
    SELECT 'Diabetes', 'Glimepiride' UNION ALL
    SELECT 'Diabetes', 'Sitagliptin' UNION ALL
    SELECT 'Diabetes', 'Saxagliptin' UNION ALL
    SELECT 'Diabetes', 'Empagliflozin' UNION ALL
    SELECT 'Diabetes', 'Dapagliflozin' UNION ALL
    SELECT 'Diabetes', 'Liraglutide' UNION ALL
    SELECT 'Diabetes', 'Exenatide' UNION ALL
    
    SELECT 'Hypertension', 'Lisinopril' UNION ALL
    SELECT 'Hypertension', 'Enalapril' UNION ALL
    SELECT 'Hypertension', 'Ramipril' UNION ALL
    SELECT 'Hypertension', 'Losartan' UNION ALL
    SELECT 'Hypertension', 'Valsartan' UNION ALL
    SELECT 'Hypertension', 'Olmesartan' UNION ALL
    SELECT 'Hypertension', 'Metoprolol' UNION ALL
    SELECT 'Hypertension', 'Atenolol' UNION ALL
    SELECT 'Hypertension', 'Carvedilol' UNION ALL
    SELECT 'Hypertension', 'Amlodipine' UNION ALL
    SELECT 'Hypertension', 'Nifedipine' UNION ALL
    SELECT 'Hypertension', 'Diltiazem' UNION ALL
    SELECT 'Hypertension', 'Hydrochlorothiazide' UNION ALL
    SELECT 'Hypertension', 'Furosemide' UNION ALL
    SELECT 'Hypertension', 'Spironolactone' UNION ALL
    SELECT 'Hypertension', 'Doxazosin' UNION ALL
    SELECT 'Hypertension', 'Prazosin' UNION ALL
    SELECT 'Hypertension', 'Clonidine' UNION ALL
    SELECT 'Hypertension', 'Methyldopa' UNION ALL

    SELECT 'High_Cholesterol' AS Measure_Short, 'Atorvastatin' AS Gnrc_Name UNION ALL
    SELECT 'High_Cholesterol', 'Simvastatin' UNION ALL
    SELECT 'High_Cholesterol', 'Rosuvastatin' UNION ALL
    SELECT 'High_Cholesterol', 'Pravastatin' UNION ALL
    SELECT 'High_Cholesterol', 'Cholestyramine' UNION ALL
    SELECT 'High_Cholesterol', 'Colestipol' UNION ALL
    SELECT 'High_Cholesterol', 'Ezetimibe' UNION ALL
    SELECT 'High_Cholesterol', 'Alirocumab' UNION ALL
    SELECT 'High_Cholesterol', 'Evolocumab' UNION ALL
    SELECT 'High_Cholesterol', 'Fenofibrate' UNION ALL
    SELECT 'High_Cholesterol', 'Gemfibrozil' UNION ALL
    SELECT 'High_Cholesterol', 'Niacin' UNION ALL

    SELECT 'COPD' AS Measure_Short, 'Albuterol' AS Gnrc_Name UNION ALL
    SELECT 'COPD', 'Levalbuterol' UNION ALL
    SELECT 'COPD', 'Salmeterol' UNION ALL
    SELECT 'COPD', 'Formoterol' UNION ALL
    SELECT 'COPD', 'Fluticasone' UNION ALL
    SELECT 'COPD', 'Budesonide' UNION ALL
    SELECT 'COPD', 'Beclomethasone' UNION ALL
    SELECT 'COPD', 'Ipratropium' UNION ALL
    SELECT 'COPD', 'Tiotropium' UNION ALL
    SELECT 'COPD', 'Roflumilast' UNION ALL
    SELECT 'COPD', 'Theophylline' UNION ALL

    SELECT 'Heart_Disease' AS Measure_Short, 'Warfarin' AS Gnrc_Name UNION ALL
    SELECT 'Heart_Disease', 'Apixaban' UNION ALL
    SELECT 'Heart_Disease', 'Rivaroxaban' UNION ALL
    SELECT 'Heart_Disease', 'Aspirin' UNION ALL
    SELECT 'Heart_Disease', 'Clopidogrel' UNION ALL
    SELECT 'Heart_Disease', 'Ticagrelor' UNION ALL
    SELECT 'Heart_Disease', 'Metoprolol' UNION ALL
    SELECT 'Heart_Disease', 'Carvedilol' UNION ALL
    SELECT 'Heart_Disease', 'Lisinopril' UNION ALL
    SELECT 'Heart_Disease', 'Enalapril' UNION ALL
    SELECT 'Heart_Disease', 'Ramipril' UNION ALL
    SELECT 'Heart_Disease', 'Losartan' UNION ALL
    SELECT 'Heart_Disease', 'Valsartan' UNION ALL
    SELECT 'Heart_Disease', 'Nitroglycerin' UNION ALL
    SELECT 'Heart_Disease', 'Isosorbide Mononitrate' UNION ALL
    SELECT 'Heart_Disease', 'Atorvastatin' UNION ALL
    SELECT 'Heart_Disease', 'Simvastatin' UNION ALL

    SELECT 'Arthritis' AS Measure_Short, 'Ibuprofen' AS Gnrc_Name UNION ALL
    SELECT 'Arthritis', 'Naproxen' UNION ALL
    SELECT 'Arthritis', 'Diclofenac' UNION ALL
    SELECT 'Arthritis', 'Methotrexate' UNION ALL
    SELECT 'Arthritis', 'Hydroxychloroquine' UNION ALL
    SELECT 'Arthritis', 'Sulfasalazine' UNION ALL
    SELECT 'Arthritis', 'Etanercept' UNION ALL
    SELECT 'Arthritis', 'Adalimumab' UNION ALL
    SELECT 'Arthritis', 'Infliximab' UNION ALL
    SELECT 'Arthritis', 'Prednisone' UNION ALL
    SELECT 'Arthritis', 'Methylprednisolone' UNION ALL

    SELECT 'Asthma' AS Measure_Short, 'Fluticasone' AS Gnrc_Name UNION ALL
    SELECT 'Asthma', 'Budesonide' UNION ALL
    SELECT 'Asthma', 'Beclomethasone' UNION ALL
    SELECT 'Asthma', 'Albuterol' UNION ALL
    SELECT 'Asthma', 'Salmeterol' UNION ALL
    SELECT 'Asthma', 'Formoterol' UNION ALL
    SELECT 'Asthma', 'Montelukast' UNION ALL
    SELECT 'Asthma', 'Zafirlukast' UNION ALL
    SELECT 'Asthma', 'Cromolyn Sodium' UNION ALL

    SELECT 'Depression' AS Measure_Short, 'Fluoxetine' AS Gnrc_Name UNION ALL
    SELECT 'Depression', 'Sertraline' UNION ALL
    SELECT 'Depression', 'Citalopram' UNION ALL
    SELECT 'Depression', 'Escitalopram' UNION ALL
    SELECT 'Depression', 'Paroxetine' UNION ALL
    SELECT 'Depression', 'Venlafaxine' UNION ALL
    SELECT 'Depression', 'Duloxetine' UNION ALL
    SELECT 'Depression', 'Amitriptyline' UNION ALL
    SELECT 'Depression', 'Nortriptyline' UNION ALL
    SELECT 'Depression', 'Phenelzine' UNION ALL
    SELECT 'Depression', 'Tranylcypromine' UNION ALL
    SELECT 'Depression', 'Bupropion' UNION ALL
    SELECT 'Depression', 'Mirtazapine' UNION ALL

    SELECT 'CKD' AS Measure_Short, 'Lisinopril' AS Gnrc_Name UNION ALL
    SELECT 'CKD', 'Ramipril' UNION ALL
    SELECT 'CKD', 'Losartan' UNION ALL
    SELECT 'CKD', 'Valsartan' UNION ALL
    SELECT 'CKD', 'Furosemide' UNION ALL
    SELECT 'CKD', 'Spironolactone' UNION ALL
    SELECT 'CKD', 'Sevelamer' UNION ALL
    SELECT 'CKD', 'Calcium Acetate' UNION ALL
    SELECT 'CKD', 'Epoetin Alfa' UNION ALL
    SELECT 'CKD', 'Darbepoetin Alfa'
)
SELECT 
    cdc.GEO_TYPE,
    cdc.GEO_VALUE,
    cdc.Measure,
    cdc.Measure_Short,
    cdc.Weighted_Average,
    cdc.Total_Population,
    cms.Brnd_Name,
    cms.Gnrc_Name,
    cms.Tot_Clms,
    cms.Tot_Drug_Cst,
    cms.Tot_Benes
FROM 
    processed_cdc_data AS cdc
LEFT JOIN 
    processed_cms_data AS cms
ON 
    cdc.GEO_TYPE = cms.GEO_TYPE 
    AND cdc.GEO_VALUE = cms.GEO_VALUE 
    AND cms.Gnrc_Name IN (
        SELECT Gnrc_Name 
        FROM condition_drug_mapping 
        WHERE condition_drug_mapping.Measure_Short = cdc.Measure_Short
    )
"""

# Execute the SQL query and load the result into a DataFrame
df = pd.read_sql_query(query_sql, conn)

# Optionally, save the result to a CSV file
df.to_csv('ChronicConditions_PrescriptionDrugs_Project/data/processed/merged_data.csv', index=False)

# Load the DataFrame into a new table in the database
df.to_sql('final_merged_data', conn, if_exists='replace', index=False)

# Confirm the data has been loaded
print("Data loaded into the 'final_merged_data' table successfully.")

# Verification: Check the number of rows inserted
row_count_query = "SELECT COUNT(*) AS row_count FROM final_merged_data;"
row_count_df = pd.read_sql_query(row_count_query, conn)
print(f"Number of rows inserted: {row_count_df['row_count'].iloc[0]}")

# Verification: Display the first 5 rows of the table
sample_query = "SELECT * FROM final_merged_data LIMIT 5;"
sample_df = pd.read_sql_query(sample_query, conn)
print("Sample rows from the 'final_merged_data' table:")
print(sample_df)

# Close the connection
conn.close()