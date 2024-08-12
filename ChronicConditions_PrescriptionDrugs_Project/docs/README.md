# **State-by-State Analysis of Chronic Condition Drug Utilization and Costs**

## **Project Overview**

This project provides a comprehensive analysis of drug utilization patterns, total costs, and average costs per claim across various chronic conditions in the United States. By examining both raw data and per capita adjusted values, this project uncovers critical insights into the healthcare challenges faced by different states and offers guidance for targeted interventions and policy development.

## **Key Features**

### **1. Data Cleaning and Transformation**
- **Data Integration**: Merged datasets from the Centers for Medicare & Medicaid Services (CMS) and the Centers for Disease Control and Prevention (CDC) to create a unified view of chronic condition management across the U.S.
- **Data Standardization**: Implemented geographic and condition-based standardization techniques to ensure consistent analysis across different states.
- **Missing Data Handling**: Applied techniques to manage missing values, ensuring robust and reliable analysis.

### **2. Data Analysis and Visualization**
- **Exploratory Data Analysis (EDA)**: Conducted in-depth exploratory data analysis to uncover trends, correlations, and outliers within the datasets.
- **Visualization**: Created compelling visualizations using Matplotlib and Seaborn to illustrate key insights, including:
  - Total Claims by Condition and State
  - Total Drug Costs by Condition and State
  - Average Cost per Claim by Condition and State
  - Per Capita Adjusted Metrics
- **Per Capita Analysis**: Adjusted key metrics for population size to provide a more equitable comparison between states, revealing the relative intensity of healthcare needs.

### **3. Database Operations**
- **SQL Integration**: Utilized SQLite to store, query, and manage the integrated dataset, demonstrating proficiency in database management.
- **Complex Queries**: Wrote and executed complex SQL queries to extract insights, calculate aggregates, and perform data transformations within the database.

### **4. Statistical Analysis**
- **Cost Efficiency**: Analyzed the cost efficiency of managing chronic conditions across different states by comparing average costs per claim relative to the total claims.
- **Correlation Analysis**: Explored correlations between drug utilization and various chronic conditions, identifying patterns that could inform healthcare policy and resource allocation.

## **Technologies Used**
- **Python**: For data cleaning, transformation, and analysis.
- **Pandas**: For data manipulation and integration.
- **Matplotlib & Seaborn**: For data visualization.
- **SQLite**: For database management and SQL operations.
- **Jupyter Notebook**: For interactive analysis and presentation.

## **Project Structure**
````data/`: Contains the raw and processed data files.
`notebooks/`: Jupyter notebooks with the analysis, visualizations, and SQL operations.
`scripts/`: Python scripts for data cleaning, transformation, and analysis.
`requirements.txt`: Lists the Python dependencies required to run the project.
`README.md`: Overview of the project, key features, and instructions.```

## **How to Run the Project**
1. **Clone the Repository**:
    ```bash
    git clone https://github.com/dillon-shearer/portfolio/tree/main/ChronicConditions_PrescriptionDrugs_Project
    cd ChronicConditions_PrescriptionDrugs_Project
    ```

2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Jupyter Notebooks**:
    Open the notebooks in the `notebooks/` directory to explore the analysis and visualizations interactively.

4. **Run the Scripts**:
    Execute the Python scripts in the `scripts/` directory for data processing and analysis.

## **Skills Demonstrated**
- **Data Wrangling**: Expertise in cleaning, transforming, and merging large datasets from multiple sources.
- **Data Visualization**: Proficiency in creating insightful and visually appealing charts and graphs.
- **SQL & Database Management**: Strong SQL skills for querying and managing relational databases.
- **Statistical Analysis**: Ability to perform complex statistical analyses to extract meaningful insights.
- **Python Programming**: Advanced use of Python for data analysis, visualization, and automation.

## **Conclusion**
This project showcases a wide range of data analysis, visualization, and database management skills, providing a deep dive into chronic condition drug utilization and costs across the United States. The findings from this analysis can inform healthcare policy, resource allocation, and targeted interventions to manage chronic conditions more effectively.

## **Contact**
For any questions or collaboration opportunities, please feel free to reach out via [LinkedIn](https://www.linkedin.com/in/dillonshearer/) or via or [dillshearer@outlook.com](mailto:dillshearer@outlook.com).
