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
    st.title("SAIPE Poverty/Income: Poverty Map")
    st.write("*This app explores the 2022 SAIPE dataset Poverty interactive map.*")
    st.write("Dillon Shearer - 2024")
    st.write("-----")

    df = load_data()

    # User selects map level
    map_level = st.selectbox("Select Map Geo Level", ["National", "State", "County"])

# NATIONAL DISPLAY

    # Display map based on user selection
    if map_level == "National":
        df_national = df[df['REGION_TYPE'] == 'NATIONAL']

        # Create the choropleth map
        fig = px.choropleth(
            df_national,
            locations='REGION_NAME', 
            locationmode='country names',  # Location mode set to USA
            color='ALL_AGES_POVERTY_PERCENT',  # Column for coloring
            color_continuous_scale='Reds',  # Color scale
            scope="usa",  # Focus the map on the USA
            labels={'ALL_AGES_POVERTY_PERCENT': 'All Ages Poverty Percent', 'REGION_NAME': 'Region Name'},  # Label for color scale
            title='Poverty',  # Title of the map
            hover_data={'REGION_NAME': True, 'ALL_AGES_POVERTY_PERCENT': True}  # Add this line to specify the tooltip content
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
            y='ALL_AGES_POVERTY_PERCENT',
            error_y='ALL_AGES_90_CI_UPPER_PERCENT',
            error_y_minus='ALL_AGES_90_CI_LOWER_PERCENT',
            labels={'REGION_NAME': 'Region Name', 'ALL_AGES_POVERTY_PERCENT': 'All Ages Poverty Percent'},
            title='Poverty by Region with Confidence Intervals'
        )

        fig.update_traces(
            error_y=dict(type='data', symmetric=False, color='red'),
            marker=dict(color='red')
        )
        
        # Adjust the layout of the figure for better display
        fig.update_layout(
        margin=dict(l=0, r=0, t=50, b=0)  # Reducing the margin for full-width display
        )

        # Show the figure
        st.plotly_chart(fig, use_container_width=True)

        # Show underlying data
        st.write("Data:")
        st.dataframe(df_national[['REGION_NAME', 'ALL_AGES_POVERTY_PERCENT', 'ALL_AGES_90_CI_UPPER_PERCENT', 'ALL_AGES_90_CI_LOWER_PERCENT']])


# STATE DISPLAY
        
    elif map_level == "State":
        df_state = df[df['REGION_TYPE'] == 'STATE']

        # Create the choropleth map
        fig = px.choropleth(
            df_state,
            locations='POSTAL_CODE', 
            locationmode='USA-states',  # Location mode set to USA
            color='ALL_AGES_POVERTY_PERCENT',  # Column for coloring
            color_continuous_scale='Reds',  # Color scale
            scope="usa",  # Focus the map on the USA
            labels={'ALL_AGES_POVERTY_PERCENT': 'All Ages Poverty Percent', 'REGION_NAME': 'Region Name'},  # Label for color scale
            title='Poverty',  # Title of the map
            hover_data={'POSTAL_CODE': False, 'REGION_NAME': True, 'ALL_AGES_POVERTY_PERCENT': True}  # Add this line to specify the tooltip content
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
            y='ALL_AGES_POVERTY_PERCENT',
            error_y='ALL_AGES_90_CI_UPPER_PERCENT',
            error_y_minus='ALL_AGES_90_CI_LOWER_PERCENT',
            labels={'REGION_NAME': 'Region Name', 'ALL_AGES_POVERTY_PERCENT': 'All Ages Poverty Percent'},
            title='Poverty by Region with Confidence Intervals'
        )

        fig.update_traces(
            error_y=dict(type='data', symmetric=False, color='red'),
            marker=dict(color='red')
        )
        
        # Adjust the layout of the figure for better display
        fig.update_layout(
        margin=dict(l=0, r=0, t=50, b=0)  # Reducing the margin for full-width display
        )

        # Show the figure
        st.plotly_chart(fig, use_container_width=True)

        # Show underlying data
        st.write("Data:")
        st.dataframe(df_state[['REGION_NAME', 'ALL_AGES_POVERTY_PERCENT', 'ALL_AGES_90_CI_UPPER_PERCENT', 'ALL_AGES_90_CI_LOWER_PERCENT']])

# COUNTY DISPLAY

    elif map_level == "County":
        df_county = df[df['REGION_TYPE'] == 'COUNTY']

        # Create the choropleth map for counties
        fig = px.choropleth(
            df_county,
            geojson="https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json",
            locations='FIPS_CODE',
            color='ALL_AGES_POVERTY_PERCENT',
            color_continuous_scale='Reds',
            scope='usa',
            labels={'ALL_AGES_POVERTY_PERCENT': 'All Ages Poverty Percent', 'REGION_NAME': 'Region Name'},  # Label for color scale
            title='Median Income',  # Title of the map
            hover_data={'FIPS_CODE': False, 'REGION_NAME': True, 'ALL_AGES_POVERTY_PERCENT': True}  # Add this line to specify the tooltip content
        )

        fig.update_layout(margin=dict(l=0, r=0, t=50, b=0), geo_scope='usa')
        
        # Display in Streamlit
        st.plotly_chart(fig, use_container_width=True)

        # Scatter plot with Error Bars
        fig = px.scatter(
            df_county, 
            x='REGION_NAME', 
            y='ALL_AGES_POVERTY_PERCENT',
            error_y='ALL_AGES_90_CI_UPPER_PERCENT',
            error_y_minus='ALL_AGES_90_CI_LOWER_PERCENT',
            labels={'REGION_NAME': 'Region Name', 'ALL_AGES_POVERTY_PERCENT': 'All Ages Poverty Percent'},
            title='Poverty by Region with Confidence Intervals'
        )

        fig.update_traces(
            error_y=dict(type='data', symmetric=False, color='red'),
            marker=dict(color='red')
        )
        
        # Adjust the layout of the figure for better display
        fig.update_layout(
        margin=dict(l=0, r=0, t=50, b=0)  # Reducing the margin for full-width display
        )

        # Show the figure
        st.plotly_chart(fig, use_container_width=True)

        # Show underlying data
        st.write("Data:")
        st.dataframe(df_county[['REGION_NAME', 'ALL_AGES_POVERTY_PERCENT', 'ALL_AGES_90_CI_UPPER_PERCENT', 'ALL_AGES_90_CI_LOWER_PERCENT']])
