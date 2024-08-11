# Database Schema Documentation

## Database: Chronic Conditions and Prescription Drugs

This document provides an overview of the schema for the SQLite database used in the "Chronic Conditions and Prescription Drugs" project. The database consists of one main table: `final_merged_data`, which contains merged data from the CDC and CMS datasets.

---

## Table: `final_merged_data`

This table contains the final merged dataset of chronic conditions and their corresponding prescription drugs, along with relevant geographic and statistical data.

### Columns:

| Column Name       | Data Type | Description                                                                 |
|-------------------|-----------|-----------------------------------------------------------------------------|
| **GEO_TYPE**      | TEXT      | The type of geographic region (e.g., "State", "County").                    |
| **GEO_VALUE**     | TEXT      | The specific geographic region (e.g., state name, county name).             |
| **Measure**       | TEXT      | The full name of the chronic condition (e.g., "Diabetes", "Hypertension").  |
| **Measure_Short** | TEXT      | A shorthand version of the chronic condition name (e.g., "Diabetes", "CKD").|
| **Weighted_Average** | REAL  | The weighted average of the measure across the geographic region.           |
| **Total_Population** | INTEGER | The total population in the geographic region.                              |
| **Brnd_Name**     | TEXT      | The brand name of the prescribed drug (if available).                       |
| **Gnrc_Name**     | TEXT      | The generic name of the prescribed drug.                                     |
| **Tot_Clms**      | INTEGER   | The total number of claims for the drug.                                     |
| **Tot_Drug_Cst**  | REAL      | The total cost associated with the drug claims.                              |
| **Tot_Benes**     | INTEGER   | The total number of beneficiaries receiving the drug.                        |

---

## Example Queries

### 1. **Count Total Rows in `final_merged_data` Table:**

```sql
SELECT COUNT(*) AS total_rows FROM final_merged_data;
