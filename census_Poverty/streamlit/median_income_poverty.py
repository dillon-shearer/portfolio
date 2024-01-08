import streamlit as st
import plotly.express as px
import pandas as pd

# Function to load data
def load_data():
    clean_data_filepath = 'census_Poverty/data/CLEANED_2022_SAIPE_DATA.xlsx'
    df = pd.read_excel(clean_data_filepath, dtype={'FIPS_CODE': str})
    return df

# Callback function for click event, now accepts the dataframe as an argument
def display_county_data(df, selected_state_code, selected_state_name):
    # Filter for county data of the selected state
    df_county = df[(df['REGION_TYPE'] == 'COUNTY') & (df['POSTAL_CODE'] == selected_state_code)]

    # Retrieve the state data used in the state-level chart
    state_data = df[(df['REGION_TYPE'] == 'STATE') & (df['POSTAL_CODE'] == selected_state_code)].iloc[0]

    # Use the state's median income and poverty percentage
    state_avg_income = state_data['MEDIAN_HOUSEHOLD_INCOME']
    state_avg_poverty = state_data['ALL_AGES_POVERTY_PERCENT']

    fig_county = px.scatter(df_county, 
                            x='MEDIAN_HOUSEHOLD_INCOME', 
                            y='ALL_AGES_POVERTY_PERCENT', 
                            hover_data=['REGION_NAME'],
                            labels={'REGION_NAME': 'Region Name',
                                    'MEDIAN_HOUSEHOLD_INCOME': 'Median Household Income', 
                                    'ALL_AGES_POVERTY_PERCENT': 'Poverty Percentage'},
                            title=f'County-Level Data for {selected_state_name}')

    # Add lines for state averages
    fig_county.add_hline(y=state_avg_poverty, line_dash="dash", line_color="red")
    fig_county.add_vline(x=state_avg_income, line_dash="dash", line_color="blue")

    # Add annotations for state averages
    fig_county.add_annotation(x=state_avg_income, y=max(df_county['ALL_AGES_POVERTY_PERCENT']),
                              text=f"State Avg Household Income: ${state_avg_income:,.0f}",
                              showarrow=False, yshift=10)
    fig_county.add_annotation(y=state_avg_poverty, x=min(df_county['MEDIAN_HOUSEHOLD_INCOME']),
                              text=f"State Avg Poverty (%): {state_avg_poverty:.2f}%",
                              showarrow=False, xshift=-50)

    st.plotly_chart(fig_county)


# Main function for the analysis pages
def show():
    st.title("SAIPE Poverty/Income: Median Income x Poverty Plot")
    st.write("*Explore a comprehensive and interactive analysis of poverty data intersecting with median income data across the United States.*")
    st.write("Dillon Shearer - 2024")
    st.write("------")

    df = load_data()  # Load the data

    # Calculate National Averages
    national_avg_income = df[df['REGION_TYPE'] == 'NATIONAL']['MEDIAN_HOUSEHOLD_INCOME'].mean()
    national_avg_poverty = df[df['REGION_TYPE'] == 'NATIONAL']['ALL_AGES_POVERTY_PERCENT'].mean()

    # Filtering the dataframe to include only state data
    df_state = df[df['REGION_TYPE'] == 'STATE']

    # Create a mapping from postal code to state name
    state_name_mapping = df_state.set_index('POSTAL_CODE')['REGION_NAME'].to_dict()

    # Generating a scatter plot for state data
    fig_state = px.scatter(df_state, 
                           x='MEDIAN_HOUSEHOLD_INCOME', 
                           y='ALL_AGES_POVERTY_PERCENT', 
                           hover_data=['REGION_NAME'],
                           labels={'REGION_NAME': 'Region Name',
                                    'MEDIAN_HOUSEHOLD_INCOME': 'Median Household Income', 
                                   'ALL_AGES_POVERTY_PERCENT': 'Poverty Percentage'},
                           title='State-Level Median Household Income vs Poverty Percentage')

    # Add lines for national averages
    fig_state.add_hline(y=national_avg_poverty, line_dash="dash", line_color="red")
    fig_state.add_vline(x=national_avg_income, line_dash="dash", line_color="blue")

    # Add annotations for national averages
    fig_state.add_annotation(x=national_avg_income, y=max(df_state['ALL_AGES_POVERTY_PERCENT']),
                             text=f"National Avg Household Income: ${national_avg_income:,.0f}",
                             showarrow=False, yshift=10)
    fig_state.add_annotation(y=national_avg_poverty, x=min(df_state['MEDIAN_HOUSEHOLD_INCOME']),
                             text=f"National Avg Poverty (%): {national_avg_poverty:.2f}%",
                             showarrow=False, xshift=-50)

    st.plotly_chart(fig_state)

    # Create session state for displaying county data
    if 'display_county_data' not in st.session_state:
        st.session_state.display_county_data = False

    # Use state names in the selector
    selected_state_name = st.selectbox('Select a State', options=list(state_name_mapping.values()))
    selected_state_code = [code for code, name in state_name_mapping.items() if name == selected_state_name][0]

    # Inline buttons for showing and clearing county data
    col1, col2, _ = st.columns([1, 1, 3.8])  # The underscore '_' is used to ignore the third column
    with col1:
        if st.button('Show County Data'):
            st.session_state.display_county_data = True
    # Apply custom style to the 'Clear' button
    with col2:
        if st.button('Clear', key="clear_button"):
            st.session_state.display_county_data = False

    # Display county data based on session state
    if st.session_state.display_county_data:
        display_county_data(df, selected_state_code, selected_state_name)

    st.write("State data:")
    st.dataframe(df_state)

    st.write("County data:")
    st.dataframe(df_county)
