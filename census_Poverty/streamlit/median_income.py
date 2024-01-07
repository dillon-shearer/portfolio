import streamlit as st
import plotly.express as px
import pandas as pd

# Function to load data
def load_data():
    clean_data_filepath = 'census_Poverty/data/CLEANED_2022_SAIPE_DATA.xlsx'
    df = pd.read_excel(clean_data_filepath,  dtype={'FIPS_CODE': str})
    return df

# Main function for the analysis pages
def show():
    # Set up the page
    st.title("SAIPE Poverty/Income: Median Income Map")
    st.write("*This app explores the 2022 SAIPE dataset Median Income interactive map.*")
    st.write("Dillon Shearer - 2024")
    st.write("-----")

    df = load_data()

    # User selects map level
    map_level = st.selectbox("Select Map Level", ["National", "State", "County"])

    # Display map based on user selection
    if map_level == "National":
        df_national = df[df['REGION_TYPE'] == 'NATIONAL']

        # Create the choropleth map
        fig = px.choropleth(
            df_national,
            locations='REGION_NAME', 
            locationmode='country names',  # Location mode set to USA
            color='MEDIAN_HOUSEHOLD_INCOME',  # Column for coloring
            color_continuous_scale='Greens',  # Color scale
            scope="usa",  # Focus the map on the USA
            labels={'MEDIAN_HOUSEHOLD_INCOME': 'Median Household Income'},  # Label for color scale
            title='Median Income (National)'  # Title of the map
        )
        # Adjust the layout of the figure for better display
        fig.update_layout(
        margin=dict(l=0, r=0, t=50, b=0)  # Reducing the margin for full-width display
        )

        # Show the figure
        st.plotly_chart(fig, use_container_width=True)

    elif map_level == "State":
        df_state = df[df['REGION_TYPE'] == 'STATE']

        # Create the choropleth map
        fig = px.choropleth(
            df_state,
            locations='POSTAL_CODE', 
            locationmode='USA-states',  # Location mode set to USA
            color='MEDIAN_HOUSEHOLD_INCOME',  # Column for coloring
            color_continuous_scale='Greens',  # Color scale
            scope="usa",  # Focus the map on the USA
            labels={'MEDIAN_HOUSEHOLD_INCOME': 'Median Household Income'},  # Label for color scale
            title='Median Income (State)'  # Title of the map
        )
        # Adjust the layout of the figure for better display
        fig.update_layout(
        margin=dict(l=0, r=0, t=50, b=0)  # Reducing the margin for full-width display
        )

        # Show the figure
        st.plotly_chart(fig, use_container_width=True)

    elif map_level == "County":
        df_county = df[df['REGION_TYPE'] == 'COUNTY']

        # Create the choropleth map for counties
        fig = px.choropleth(
            df_county,
            geojson="https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json",
            locations='FIPS_CODE',
            color='MEDIAN_HOUSEHOLD_INCOME',
            color_continuous_scale='Greens',
            scope='usa',
            labels={'MEDIAN_HOUSEHOLD_INCOME': 'Median Household Income'},
            title='Median Income (County)'
        )

        fig.update_layout(margin=dict(l=0, r=0, t=50, b=0), geo_scope='usa')
        
        # Display in Streamlit
        st.plotly_chart(fig, use_container_width=True)
