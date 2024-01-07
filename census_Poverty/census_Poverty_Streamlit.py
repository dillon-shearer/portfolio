# Import Libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly
import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="2022 SAIPE Poverty Data Exploration",
    page_icon="📊",  # Example: using an emoji as icon
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a Bug': None,  # Removing the 'Report a Bug' option
        'About': "This app is used for analyzing poverty/median income data."
    }
)

# Function to load data
def load_data():
    clean_data_filepath = f'C:\\Users\\dills\\portfolio\\portfolio\\census_Poverty\\data\\CLEANED_2022_SAIPE_DATA.xlsx'
    df = pd.read_excel(clean_data_filepath)
    return df

# Main function for the Streamlit app
def main():
    # Set up the page
    st.title("Census Poverty Data Exploration")
    st.write("*This app explores the 2022 SAIPE dataset for poverty analysis.*")
    st.write("Dillon Shearer - 2024")
    st.write("-----")
    st.write("**Complete dataset** (post-cleaning): ")

    # Load and display the data
    df = load_data()
    st.dataframe(df)

    # Create secondary dataframe to hold only National data
    df_national = df[df['REGION_TYPE'] == 'NATIONAL']

    # National EDA
    st.write("-----")
    st.write("## National EDA:")
    st.dataframe(df_national)

    st.write("**Region**: " + df_national['REGION_NAME'].values[0] + "\n\n"
      + 'Poverty Estimate for ALL Ages (int): ' + str(df_national['ALL_AGES_POVERTY_ESTIMATE'].values[0]) + "\n\n"
      + 'Poverty Estimate for ALL Ages (percent): ' + str(df_national['ALL_AGES_POVERTY_PERCENT'].values[0]) + '%' + "\n\n"
      + 'Poverty Estimate for Ages 0-17 (int): ' + str(df_national['0_17_POVERTY_ESTIMATE'].values[0]) + "\n\n"
      + 'Poverty Estimate for Ages 0-17 (percent): ' + str(df_national['0_17_POVERTY_PERCENT'].values[0]) + '%' + "\n\n"
      + 'Median Household Income: $' + str(df_national['MEDIAN_HOUSEHOLD_INCOME'].values[0]) + "\n\n"
      )
    
    # Data
    categories = ['All Ages', 'Ages 0-17']
    all_ages_percentage = df_national['ALL_AGES_POVERTY_PERCENT'].values[0]
    ages_0_17_percentage = df_national['0_17_POVERTY_PERCENT'].values[0]

    poverty_percentages = [all_ages_percentage, ages_0_17_percentage]

    # Create a bar chart
    plt.figure(figsize=(8, 6))
    plt.bar(categories, poverty_percentages, color=['blue', 'red', 'green'])
    plt.xlabel('Age Categories')
    plt.ylabel('Poverty Rate (%)')
    plt.title('Poverty Rates in the United States')
    plt.ylim(0, 20)  # Set the y-axis limit to ensure all bars are visible

    # Add data labels above the bars
    for i, percentage in enumerate(poverty_percentages):
        plt.text(i, percentage + 1, f"{percentage:.1f}%", ha='center', va='bottom', fontsize=12)

    # Show the plot
    st.pyplot(plt)

    st.write("Based on the above National data we can find a few interesting discussions.\n\n" + 
        "1. In the United States, we see a national poverty level of 12.6% in 2022 (40,951,625 individuals). One important note is that this figure accounts for ALL ages - both adults and children.\n\n"
        "2. The child poverty rate is significantly higher than the overall poverty rate at 16.3% in 2022 (or 11,582,950 individuals ages 0 to 17).\n\n"
        "Overall, these statistics suggest that there is a portion of the population, particularly children, who are experiencing poverty in the United States. While the overall poverty rate is below 13%, the child poverty rate is notably higher, indicating that child poverty remains a concern. Additionally, the median household income provides a snapshot of the economic conditions for the typical American household, which can be used for various policy and economic assessments.")

    st.write("----------")
    st.write("## State EDA:")

    # Create secondary dataframe to hold only State data
    df_state = df[df['REGION_TYPE'] == 'STATE']

    st.dataframe(df_state)

    st.write("*All Ages Poverty Percent Statistics*")

    # Create statistics for All Ages **Poverty Percent**
    st.write(df_state['ALL_AGES_POVERTY_PERCENT'].describe())

    st.write("**Count**: There are 51 data points, which include the 50 states plus the District of Columbia." + "\n\n")
    st.write("**Mean**: The average poverty percentage across these regions is approximately 12.36%." + "\n\n")
    st.write("**Standard Deviation**: The standard deviation is about 2.58%, indicating that there is some variation in poverty rates between the states, but it's not extremely wide." + "\n\n")
    st.write("**Minimum**: The lowest recorded poverty percentage among the states is 7.4%." + "\n\n")
    st.write("**25th Percentile**: About a quarter of the states have a poverty percentage at or below 10.55%." + "\n\n")
    st.write("**Median**: The median poverty percentage, which reduces the effect of outliers, is 11.9%. This is slightly lower than the mean, suggesting a skew towards higher poverty rates in fewer states." + "\n\n")
    st.write("**75th Percentile**: About three-quarters of the states have a poverty percentage at or below 13.35%." + "\n\n")
    st.write("**Maximum**: The highest poverty percentage in any state is 19.2%." + "\n\n")
    st.write("From these statistics, we can infer that while the majority of states have poverty rates close to the national average, there are some states with significantly higher poverty percentages, which increase the mean above the median. The state with the highest poverty rate (19.2%) is an outlier, considerably higher than the 75th percentile of 13.35%." + "\n\n")

    # Create the choropleth map
    fig = px.choropleth(
        df_state,
        locations='POSTAL_CODE',  # State abbreviations
        locationmode='USA-states',  # Location mode set to USA states
        color='ALL_AGES_POVERTY_PERCENT',  # Column for coloring
        color_continuous_scale='Reds',  # Color scale
        scope="usa",  # Focus the map on the USA
        labels={'ALL_AGES_POVERTY_ESTIMATE': 'Poverty Estimate'},  # Label for color scale
        title='All Ages: Poverty Percentages by State'  # Title of the map
    )
    st.plotly_chart()

# Show the figure
fig.show()

# Run the app
if __name__ == "__main__":
    main()