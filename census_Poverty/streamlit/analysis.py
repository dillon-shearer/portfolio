# Import Libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly
import streamlit as st

# Function to load data
def load_data():
    clean_data_filepath = 'census_Poverty/data/CLEANED_2022_SAIPE_DATA.xlsx'
    df = pd.read_excel(clean_data_filepath)
    return df

# Main function for the analysis pages
def show():
    # Set up the page
    st.title("Census Poverty/Median Income Data Exploration")
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
    st.write("## 1 - National EDA:")
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
    st.write("## 2 - State EDA:")

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

    st.write("-----")

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
    # Adjust the layout of the figure for better display
    fig.update_layout(
    margin=dict(l=0, r=0, t=50, b=0)  # Reducing the margin for full-width display
)
    st.plotly_chart(fig, use_container_width=True)

    st.write("-----")

    # Create the choropleth map
    fig = px.choropleth(
        df_state,
        locations='POSTAL_CODE',  # State abbreviations
        locationmode='USA-states',  # Location mode set to USA states
        color='0_17_POVERTY_PERCENT',  # Column for coloring
        color_continuous_scale='Blues',  # Color scale
        scope="usa",  # Focus the map on the USA
        labels={'0_17_POVERTY_ESTIMATE': 'Poverty Estimate'},  # Label for color scale
        title='Age 0-17: Poverty Percentages by State'  # Title of the map
    )
        # Adjust the layout of the figure for better display
    fig.update_layout(
    margin=dict(l=0, r=0, t=50, b=0)  # Reducing the margin for full-width display
    )
    st.plotly_chart(fig, use_container_width=True)

    st.write("-----")
    st.write("## 3 - Median Income Analysis:")

    # Filter the data to exclude the 'US' aggregate row and select only the required columns
    df_median_income = df[df['REGION_TYPE'] == 'STATE'][['POSTAL_CODE', 'MEDIAN_HOUSEHOLD_INCOME']]

    # Sort the data by median household income for better visualization
    df_median_income_sorted = df_median_income.sort_values('MEDIAN_HOUSEHOLD_INCOME', ascending=True)

    # Now we create the bar graph using Plotly
    fig_income = px.bar(
        df_median_income_sorted,
        x='MEDIAN_HOUSEHOLD_INCOME',
        y='POSTAL_CODE',
        orientation='h',
        title='Median Household Incomes by State',
        labels={'MEDIAN_HOUSEHOLD_INCOME': 'Median Household Income', 'POSTAL_CODE': 'State'},
        color='MEDIAN_HOUSEHOLD_INCOME',
        color_continuous_scale=px.colors.sequential.Greens
    )
    # Adjust the layout of the figure for better display
    fig_income.update_layout(
    margin=dict(l=0, r=0, t=50, b=0)  # Reducing the margin for full-width display
    )
    st.plotly_chart(fig_income, use_container_width=True)

    st.write("-----")

    # Create the choropleth map
    fig = px.choropleth(
        df_state,
        locations='POSTAL_CODE',  # State abbreviations
        locationmode='USA-states',  # Location mode set to USA states
        color='MEDIAN_HOUSEHOLD_INCOME',  # Column for coloring
        color_continuous_scale='Greens',  # Color scale
        scope="usa",  # Focus the map on the USA
        labels={'MEDIAN_HOUSEHOLD_INCOME': 'Median Household Income'},  # Label for color scale
        title='Median Income by State'  # Title of the map
    )
    # Adjust the layout of the figure for better display
    fig.update_layout(
    margin=dict(l=0, r=0, t=50, b=0)  # Reducing the margin for full-width display
    )

    # Show the figure
    st.plotly_chart(fig, use_container_width=True)
    
    st.write("-----")

    # Create the scatter plot using Plotly
    fig_scatter = px.scatter(
        df_state,
        x='MEDIAN_HOUSEHOLD_INCOME',
        y='ALL_AGES_POVERTY_PERCENT',
        text='POSTAL_CODE',  # Display state abbreviations on the plot
        title='Poverty Rate vs. Median Household Income by State',
        labels={
            'MEDIAN_HOUSEHOLD_INCOME': 'Median Household Income ($)',
            'ALL_AGES_POVERTY_PERCENT': 'All Ages Poverty Rate (%)'
        },
        color='ALL_AGES_POVERTY_PERCENT',  # Color the points by poverty rate
        color_continuous_scale=px.colors.sequential.Reds
    )
    # Adjust the layout of the figure for better display
    fig_scatter.update_layout(
    margin=dict(l=0, r=0, t=50, b=0)  # Reducing the margin for full-width display
    )

    # Adding state labels to the points for better readability
    fig_scatter.update_traces(textposition='top center')

    st.plotly_chart(fig_scatter, use_container_width=True)

    st.write("1. **Inverse Relationship**: As expected, there is a clear inverse relationship between the median household income and the poverty rate. States with higher median incomes generally have lower poverty rates." + "\n\n"
        "2. **High Poverty and Low Income**: States like Mississippi (MS), Louisiana (LA), West Virginia (WV), and Arkansas (AR) appear in the top left corner, indicating they have higher poverty rates and lower median household incomes." + "\n\n"
        "3. **Low Poverty and High Income**: Conversely, states such as New Hampshire (NH), Maryland (MD), New Jersey (NJ), and Hawaii (HI) are located in the bottom right, showing they have lower poverty rates and higher median household incomes." + "\n\n"
        "4. **Outliers**: The District of Columbia (DC) stands out as an outlier with a high median income but also a high poverty rate, suggesting a large income disparity within the district." + "\n\n"
        "5. **Middle Cluster**: A large cluster of states falls around the center of the plot, indicating a grouping of states with moderate income levels and poverty rates. This cluster suggests a level of consistency in economic conditions across a significant portion of the country." + "\n\n"
        "6. **Regional Patterns**: While this plot doesn't explicitly show regional groupings, you can infer regional trends based on the states' abbreviations. For example, Southern states tend to have lower median incomes and higher poverty rates." + "\n\n"
        "7. **Data Spread**: The spread of the data points indicates variability in the strength of the correlation between median household income and poverty rates among states. For instance, some states with similar median incomes have different poverty rates, which could be due to other socio-economic factors not captured in this plot." + "\n\n")

    st.write("-----")
    st.write("## 4 - Actions and Insights: Conclusion ")
    st.write("From the visualizations and data analysis performed on the provided dataset, several actionable insights can be derived:" + "\n\n"
        "1. **Targeted Poverty Alleviation Programs**: States with high poverty rates and low median household incomes may benefit from increased federal and state assistance programs. Policy-makers could focus on creating or expanding education and job training programs to improve employment opportunities, which in turn can help raise median incomes and reduce poverty." + "\n\n"
        "2. **Income Disparity Analysis**: In areas like the District of Columbia, which exhibit high median incomes alongside high poverty rates, local governments could investigate the root causes of such income disparities. This may include studying the cost of living, housing affordability, and wage distribution within the job market." + "\n\n"
        "3. **Economic Development Initiatives**: States with lower median household incomes could be targets for economic development initiatives. This might involve attracting new businesses, supporting small businesses, improving infrastructure, or providing tax incentives for industries that offer higher-paying jobs." + "\n\n"
        "4. **Healthcare and Education Accessibility**: Improving access to healthcare and education can be a powerful tool in reducing poverty. Investments in these areas can lead to better health outcomes and higher earning potential over the long term." + "\n\n"
        "5. **Customized State Policies**: Each state has a unique economic environment. The data suggests that a one-size-fits-all approach may not be effective. Instead, states should tailor their economic policies to address their specific challenges and opportunities." + "\n\n"
        "6. **Addressing Underlying Issues**: For states that are outliers or those that don't follow the general inverse trend between income and poverty, it's crucial to understand the underlying issues. This could include examining factors such as the availability of full-time work, the impact of part-time work on poverty rates, access to childcare, or other social services." + "\n\n"
        "7. **Strengthening Social Safety Nets**: States with higher poverty rates might need to strengthen their social safety nets. This can include ensuring adequate food security, access to affordable housing, and financial assistance for those in need." + "\n\n"
        "8. **Regional Collaboration**: States that share similar economic profiles could benefit from regional collaboration to address common issues such as poverty, unemployment, and economic development." + "\n\n"
        "9. **Monitoring and Evaluation**: Implementing robust monitoring and evaluation systems to track the effectiveness of poverty reduction programs can help ensure that resources are being used effectively and that programs are adjusted based on outcomes." + "\n\n"
        "These insights can guide policy-makers, community leaders, and stakeholders in making informed decisions to foster economic growth and reduce poverty. Each insight should be considered within the context of broader economic trends and the specific needs of each state's population." + "\n\n")