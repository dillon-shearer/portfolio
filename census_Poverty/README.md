# 2022 Census SAIPE Poverty Data Analysis and Visualization

## Project Overview
This project involves analyzing and visualizing poverty data from the 2022 Census SAIPE. The main focus is on national, state, and county levels, exploring various poverty metrics and median household incomes. The project uses Python for data acquisition, cleaning, preprocessing, and visualization with libraries like Pandas, Matplotlib, and Plotly.

## Installation

To set up this project, follow these steps:

1. Clone the repository to your local machine.
2. Install the required packages using:
   <br>*pip install -r requirements.txt*

## Usage

To run the scripts, navigate to the project directory and execute the Python scripts in the following order:
1. Data Acquisition: 1_data_acquisition.ipynb
2. Data Preprocessing and Cleaning: 2_data_preprocessing.ipynb
3. Exploratory Data Analysis (EDA): 3_data_eda.ipynb

## Data Analysis Workflow

1. Data Acquisition
- Download the 2022 SAIPE data.
- Load and check the initial data frame.
2. Data Preprocessing and Cleaning
- Rename and fix headers.
- Add State/National/County identifier columns.
- Validate and clean data.
- Update data types for necessary columns.
- Create FIPS codes for mapping.
3. Exploratory Data Analysis (EDA)
- Perform National and State level EDA.
- Generate visualizations for poverty rates and median household incomes.
- Create interactive maps to visualize the data geographically.
4. Tableau Maps
- Create interactive maps for poverty statistics and median household income at National, State, and County level
- https://public.tableau.com/app/profile/dillon.shearer/viz/2022CensusSAIPEVisualizations/2022SAIPEMedianIncomeMaps

## Visualizations

The project generates several visualizations, including:
1. Bar charts of poverty rates.
2. Choropleth maps showing poverty percentages and median incomes by state.
3. Scatter plots comparing poverty rates and median household incomes.

## Interactive Web Application

In addition to the Python scripts and Jupyter notebooks, this project features an interactive web application developed using Streamlit. This app allows users to explore the data through interactive visualizations and charts, providing a more dynamic and accessible way to understand the SAIPE poverty data.

### [Explore the Poverty Data Analysis App](https://ds-saipe-analysis.streamlit.app/)

The Streamlit app includes the following features:
- Interactive maps and charts displaying poverty rates and median household incomes at national, state, and county levels.
- Filters to view specific data subsets based on regions.
- Responsive design for an optimal viewing experience across different devices.

#### How to Access
- The app is hosted online and can be accessed through the provided link: [SAIPE Poverty Data Analysis App](https://ds-saipe-analysis.streamlit.app/).
- No installation or setup is required; the app runs directly in the web browser.

#### Technologies Used
- Streamlit for web application development.
- Plotly and Matplotlib for interactive visualizations within the app.

#### Feedback and Contributions
- For feedback, suggestions, or contributions to the app, please reach out through the contact details provided or via GitHub issues and pull requests.

## Contact

For any queries or feedback, please reach out to Dillon Shearer (dillshearer@outlook.com).