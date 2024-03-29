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
    map_level = st.selectbox("Select Map Geo Level", ["National", "State", "County"])

# NATIONAL DISPLAY

    # Display map based on user selection
    if map_level == "National":
        df_national = df[df['REGION_TYPE'] == 'NATIONAL']

        df_national['error_upper'] = df_national['MEDIAN_HOUSEHOLD_INCOME_90_CI_UPPER_BOUND'] - df_national['MEDIAN_HOUSEHOLD_INCOME']
        df_national['error_lower'] = df_national['MEDIAN_HOUSEHOLD_INCOME'] - df_national['MEDIAN_HOUSEHOLD_INCOME_90_CI_LOWER_BOUND']

        # Create the choropleth map
        fig = px.choropleth(
            df_national,
            locations='REGION_NAME', 
            locationmode='country names',  # Location mode set to USA
            color='MEDIAN_HOUSEHOLD_INCOME',  # Column for coloring
            color_continuous_scale='Greens',  # Color scale
            scope="usa",  # Focus the map on the USA
            labels={'MEDIAN_HOUSEHOLD_INCOME': 'Median Household Income', 'REGION_NAME': 'Region Name'},  # Label for color scale
            title='Median Income',  # Title of the map
            hover_data={'REGION_NAME': True, 'MEDIAN_HOUSEHOLD_INCOME': True}  # Add this line to specify the tooltip content
        )
        # Adjust the layout of the figure for better display
        fig.update_layout(
        margin=dict(l=0, r=0, t=50, b=0)  # Reducing the margin for full-width display
        )

        # Show the figure
        st.plotly_chart(fig, use_container_width=True)

        # Scatter plot with Error Bars
        fig = px.scatter(
            df_national, 
            x='REGION_NAME', 
            y='MEDIAN_HOUSEHOLD_INCOME',
            error_y='error_upper',
            error_y_minus='error_lower',
            labels={'REGION_NAME': 'Region Name', 'MEDIAN_HOUSEHOLD_INCOME': 'Median Household Income'},
            title='Median Household Income by Region with Confidence Intervals'
        )

        fig.update_traces(
            error_y=dict(type='data', symmetric=False, color='green'),
            marker=dict(color='green')
        )
        
        # Adjust the layout of the figure for better display
        fig.update_layout(
        margin=dict(l=0, r=0, t=50, b=0)  # Reducing the margin for full-width display
        )

        # Show the figure
        st.plotly_chart(fig, use_container_width=True)

        # Show underlying data
        st.write("Data:")
        st.dataframe(df_national[['REGION_NAME', 'MEDIAN_HOUSEHOLD_INCOME', 'MEDIAN_HOUSEHOLD_INCOME_90_CI_UPPER_BOUND', 'MEDIAN_HOUSEHOLD_INCOME_90_CI_LOWER_BOUND']])


# STATE DISPLAY
        
    elif map_level == "State":
        df_state = df[df['REGION_TYPE'] == 'STATE']

        df_state['error_upper'] = df_state['MEDIAN_HOUSEHOLD_INCOME_90_CI_UPPER_BOUND'] - df_state['MEDIAN_HOUSEHOLD_INCOME']
        df_state['error_lower'] = df_state['MEDIAN_HOUSEHOLD_INCOME'] - df_state['MEDIAN_HOUSEHOLD_INCOME_90_CI_LOWER_BOUND']

        # Create the choropleth map
        fig = px.choropleth(
            df_state,
            locations='POSTAL_CODE', 
            locationmode='USA-states',  # Location mode set to USA
            color='MEDIAN_HOUSEHOLD_INCOME',  # Column for coloring
            color_continuous_scale='Greens',  # Color scale
            scope="usa",  # Focus the map on the USA
            labels={'MEDIAN_HOUSEHOLD_INCOME': 'Median Household Income', 'REGION_NAME': 'Region Name'},  # Label for color scale
            title='Median Income',  # Title of the map
            hover_data={'POSTAL_CODE': False, 'REGION_NAME': True, 'MEDIAN_HOUSEHOLD_INCOME': True}  # Add this line to specify the tooltip content
        )
        # Adjust the layout of the figure for better display
        fig.update_layout(
        margin=dict(l=0, r=0, t=50, b=0)  # Reducing the margin for full-width display
        )

        # Show the figure
        st.plotly_chart(fig, use_container_width=True)

        # Scatter plot with Error Bars
        fig = px.scatter(
            df_state, 
            x='REGION_NAME', 
            y='MEDIAN_HOUSEHOLD_INCOME',
            error_y='error_upper',
            error_y_minus='error_lower',
            labels={'REGION_NAME': 'Region Name', 'MEDIAN_HOUSEHOLD_INCOME': 'Median Household Income'},
            title='Median Household Income by Region with Confidence Intervals'
        )

        fig.update_traces(
            error_y=dict(type='data', symmetric=False, color='green'),
            marker=dict(color='green')
        )
        
        # Adjust the layout of the figure for better display
        fig.update_layout(
        margin=dict(l=0, r=0, t=50, b=0)  # Reducing the margin for full-width display
        )

        # Show the figure
        st.plotly_chart(fig, use_container_width=True)

        # Show underlying data
        st.write("Data:")
        st.dataframe(df_state[['REGION_NAME', 'MEDIAN_HOUSEHOLD_INCOME', 'MEDIAN_HOUSEHOLD_INCOME_90_CI_UPPER_BOUND', 'MEDIAN_HOUSEHOLD_INCOME_90_CI_LOWER_BOUND']])

# COUNTY DISPLAY

    elif map_level == "County":
        df_county = df[df['REGION_TYPE'] == 'COUNTY']

        df_county['error_upper'] = df_county['MEDIAN_HOUSEHOLD_INCOME_90_CI_UPPER_BOUND'] - df_county['MEDIAN_HOUSEHOLD_INCOME']
        df_county['error_lower'] = df_county['MEDIAN_HOUSEHOLD_INCOME'] - df_county['MEDIAN_HOUSEHOLD_INCOME_90_CI_LOWER_BOUND']

        # Create the choropleth map for counties
        fig = px.choropleth(
            df_county,
            geojson="https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json",
            locations='FIPS_CODE',
            color='MEDIAN_HOUSEHOLD_INCOME',
            color_continuous_scale='Greens',
            scope='usa',
            labels={'MEDIAN_HOUSEHOLD_INCOME': 'Median Household Income', 'REGION_NAME': 'Region Name'},  # Label for color scale
            title='Median Income',  # Title of the map
            hover_data={'FIPS_CODE': False, 'REGION_NAME': True, 'MEDIAN_HOUSEHOLD_INCOME': True}  # Add this line to specify the tooltip content
        )

        fig.update_layout(margin=dict(l=0, r=0, t=50, b=0), geo_scope='usa')
        
        # Display in Streamlit
        st.plotly_chart(fig, use_container_width=True)

        # Scatter plot with Error Bars
        fig = px.scatter(
            df_county, 
            x='REGION_NAME', 
            y='MEDIAN_HOUSEHOLD_INCOME',
            error_y='error_upper',
            error_y_minus='error_lower',
            labels={'REGION_NAME': 'Region Name', 'MEDIAN_HOUSEHOLD_INCOME': 'Median Household Income'},
            title='Median Household Income by Region with Confidence Intervals'
        )

        fig.update_traces(
            error_y=dict(type='data', symmetric=False, color='green'),
            marker=dict(color='green')
        )
        
        # Adjust the layout of the figure for better display
        fig.update_layout(
        margin=dict(l=0, r=0, t=50, b=0)  # Reducing the margin for full-width display
        )

        # Show the figure
        st.plotly_chart(fig, use_container_width=True)

        # Show underlying data
        st.write("Data:")
        st.dataframe(df_county[['REGION_NAME', 'POSTAL_CODE', 'MEDIAN_HOUSEHOLD_INCOME', 'MEDIAN_HOUSEHOLD_INCOME_90_CI_UPPER_BOUND', 'MEDIAN_HOUSEHOLD_INCOME_90_CI_LOWER_BOUND']])
