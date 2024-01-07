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

    # Create three columns for the selectors
    numberpercent, geo, agelevel = st.columns(3)

    # Use each column to place a selector
    with numberpercent:
        percent_or_number = st.selectbox("Select between percentages or number values", ["Percentages", 'Numbers'])
    with geo:
        map_level = st.selectbox("Select Map Geo Level", ["National", "State", "County"])
    with agelevel:
        age_level = st.selectbox("Select Age Group of Interest", ["All Ages", "0-4", "5-17", "0-17"])

# Percentages
    if percent_or_number == 'Percentages':
    # ALL AGES
        if age_level == "All Ages":
        # NATIONAL DISPLAY
            # Display map based on user selection
            if map_level == "National":
                df_national = df[df['REGION_TYPE'] == 'NATIONAL']

                df_national['error_upper'] = df_national['ALL_AGES_90_CI_UPPER_PERCENT'] - df_national['ALL_AGES_POVERTY_PERCENT']
                df_national['error_lower'] = df_national['ALL_AGES_POVERTY_PERCENT'] - df_national['ALL_AGES_90_CI_LOWER_PERCENT']

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
                    error_y='error_upper',
                    error_y_minus='error_lower',
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

                df_state['error_upper'] = df_state['ALL_AGES_90_CI_UPPER_PERCENT'] - df_state['ALL_AGES_POVERTY_PERCENT']
                df_state['error_lower'] = df_state['ALL_AGES_POVERTY_PERCENT'] - df_state['ALL_AGES_90_CI_LOWER_PERCENT']

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
                    error_y='error_upper',
                    error_y_minus='error_lower',
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

                df_county['error_upper'] = df_county['ALL_AGES_90_CI_UPPER_PERCENT'] - df_county['ALL_AGES_POVERTY_PERCENT']
                df_county['error_lower'] = df_county['ALL_AGES_POVERTY_PERCENT'] - df_county['ALL_AGES_90_CI_LOWER_PERCENT']

                # Create the choropleth map for counties
                fig = px.choropleth(
                    df_county,
                    geojson="https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json",
                    locations='FIPS_CODE',
                    color='ALL_AGES_POVERTY_PERCENT',
                    color_continuous_scale='Reds',
                    scope='usa',
                    labels={'ALL_AGES_POVERTY_PERCENT': 'All Ages Poverty Percent', 'REGION_NAME': 'Region Name'},  # Label for color scale
                    title='Poverty',  # Title of the map
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
                    error_y='error_upper',
                    error_y_minus='error_lower',
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

    # 0-4
        if age_level == "0-4":
        # NATIONAL DISPLAY
            # Display map based on user selection
            if map_level == "National":
                df_national = df[df['REGION_TYPE'] == 'NATIONAL']

                df_national['error_upper'] = df_national['0_4_UPPER_PERCENT'] - df_national['0_4_POVERTY_PERCENT']
                df_national['error_lower'] = df_national['0_4_POVERTY_PERCENT'] - df_national['0_4_UPPER_PERCENT']

                # Create the choropleth map
                fig = px.choropleth(
                    df_national,
                    locations='REGION_NAME', 
                    locationmode='country names',  # Location mode set to USA
                    color='0_4_POVERTY_PERCENT',  # Column for coloring
                    color_continuous_scale='Reds',  # Color scale
                    scope="usa",  # Focus the map on the USA
                    labels={'0_4_POVERTY_PERCENT': 'Age 0-4 Poverty Percent', 'REGION_NAME': 'Region Name'},  # Label for color scale
                    title='Poverty',  # Title of the map
                    hover_data={'REGION_NAME': True, '0_4_POVERTY_PERCENT': True}  # Add this line to specify the tooltip content
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
                    y='0_4_POVERTY_PERCENT',
                    error_y='error_upper',
                    error_y_minus='error_lower',
                    labels={'REGION_NAME': 'Region Name', '0_4_POVERTY_PERCENT': 'All Ages Poverty Percent'},
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
                st.dataframe(df_national[['REGION_NAME', '0_4_POVERTY_PERCENT', '0_4_UPPER_PERCENT', '0_4_CI_LOWER_PERCENT']])


            # STATE DISPLAY
                
            elif map_level == "State":
                df_state = df[df['REGION_TYPE'] == 'STATE']

                df_state['error_upper'] = df_state['0_4_UPPER_PERCENT'] - df_state['0_4_POVERTY_PERCENT']
                df_state['error_lower'] = df_state['0_4_POVERTY_PERCENT'] - df_state['0_4_UPPER_PERCENT']

                # Create the choropleth map
                fig = px.choropleth(
                    df_state,
                    locations='POSTAL_CODE', 
                    locationmode='USA-states',  # Location mode set to USA
                    color='0_4_POVERTY_PERCENT',  # Column for coloring
                    color_continuous_scale='Reds',  # Color scale
                    scope="usa",  # Focus the map on the USA
                    labels={'0_4_POVERTY_PERCENT': 'Age 0-4 Poverty Percent', 'REGION_NAME': 'Region Name'},  # Label for color scale
                    title='Poverty',  # Title of the map
                    hover_data={'POSTAL_CODE': False, 'REGION_NAME': True, '0_4_POVERTY_PERCENT': True}  # Add this line to specify the tooltip content
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
                    y='0_4_POVERTY_PERCENT',
                    error_y='error_upper',
                    error_y_minus='error_lower',
                    labels={'REGION_NAME': 'Region Name', '0_4_POVERTY_PERCENT': 'Age 0-4 Poverty Percent'},
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
                st.dataframe(df_state[['REGION_NAME', '0_4_POVERTY_PERCENT', '0_4_UPPER_PERCENT', '0_4_CI_LOWER_PERCENT']])

            # COUNTY DISPLAY

            elif map_level == "County":
                df_county = df[df['REGION_TYPE'] == 'COUNTY']

                st.write("County data not available for ages 0-4.")

    # 5-17 AGES
        if age_level == "5-17":
        # NATIONAL DISPLAY
            # Display map based on user selection
            if map_level == "National":
                df_national = df[df['REGION_TYPE'] == 'NATIONAL']

                df_national['error_upper'] = df_national['5_17_90_CI_UPPER_PERCENT'] - df_national['5_17_POVERTY_PERCENT']
                df_national['error_lower'] = df_national['5_17_POVERTY_PERCENT'] - df_national['5_17_90_CI_LOWER_PERCENT']

                # Create the choropleth map
                fig = px.choropleth(
                    df_national,
                    locations='REGION_NAME', 
                    locationmode='country names',  # Location mode set to USA
                    color='5_17_POVERTY_PERCENT',  # Column for coloring
                    color_continuous_scale='Reds',  # Color scale
                    scope="usa",  # Focus the map on the USA
                    labels={'5_17_POVERTY_PERCENT': 'Age 5-17 Poverty Percent', 'REGION_NAME': 'Region Name'},  # Label for color scale
                    title='Poverty',  # Title of the map
                    hover_data={'REGION_NAME': True, '5_17_POVERTY_PERCENT': True}  # Add this line to specify the tooltip content
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
                    y='5_17_POVERTY_PERCENT',
                    error_y='error_upper',
                    error_y_minus='error_lower',
                    labels={'REGION_NAME': 'Region Name', '5_17_POVERTY_PERCENT': 'Ages 5-17 Poverty Percent'},
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
                st.dataframe(df_national[['REGION_NAME', '5_17_POVERTY_PERCENT', '5_17_90_CI_UPPER_PERCENT', '5_17_90_CI_LOWER_PERCENT']])


            # STATE DISPLAY
                
            elif map_level == "State":
                df_state = df[df['REGION_TYPE'] == 'STATE']

                df_state['error_upper'] = df_state['5_17_90_CI_UPPER_PERCENT'] - df_state['5_17_POVERTY_PERCENT']
                df_state['error_lower'] = df_state['5_17_POVERTY_PERCENT'] - df_state['5_17_90_CI_LOWER_PERCENT']

                # Create the choropleth map
                fig = px.choropleth(
                    df_state,
                    locations='POSTAL_CODE', 
                    locationmode='USA-states',  # Location mode set to USA
                    color='5_17_POVERTY_PERCENT',  # Column for coloring
                    color_continuous_scale='Reds',  # Color scale
                    scope="usa",  # Focus the map on the USA
                    labels={'5_17_POVERTY_PERCENT': 'Age 5-17 Poverty Percent', 'REGION_NAME': 'Region Name'},  # Label for color scale
                    title='Poverty',  # Title of the map
                    hover_data={'POSTAL_CODE': False, 'REGION_NAME': True, '5_17_POVERTY_PERCENT': True}  # Add this line to specify the tooltip content
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
                    y='5_17_POVERTY_PERCENT',
                    error_y='error_upper',
                    error_y_minus='error_lower',
                    labels={'REGION_NAME': 'Region Name', '5_17_POVERTY_PERCENT': 'Age 5-17 Poverty Percent'},
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
                st.dataframe(df_state[['REGION_NAME', '5_17_POVERTY_PERCENT', '5_17_90_CI_UPPER_PERCENT', '5_17_90_CI_LOWER_PERCENT']])

            # COUNTY DISPLAY

            elif map_level == "County":
                df_county = df[df['REGION_TYPE'] == 'COUNTY']

                df_county['error_upper'] = df_county['5_17_90_CI_UPPER_PERCENT'] - df_county['5_17_POVERTY_PERCENT']
                df_county['error_lower'] = df_county['5_17_POVERTY_PERCENT'] - df_county['5_17_90_CI_LOWER_PERCENT']

                # Create the choropleth map for counties
                fig = px.choropleth(
                    df_county,
                    geojson="https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json",
                    locations='FIPS_CODE',
                    color='5_17_POVERTY_PERCENT',
                    color_continuous_scale='Reds',
                    scope='usa',
                    labels={'5_17_POVERTY_PERCENT': 'Age 5-17 Poverty Percent', 'REGION_NAME': 'Region Name'},  # Label for color scale
                    title='Poverty',  # Title of the map
                    hover_data={'FIPS_CODE': False, 'REGION_NAME': True, '5_17_POVERTY_PERCENT': True}  # Add this line to specify the tooltip content
                )

                fig.update_layout(margin=dict(l=0, r=0, t=50, b=0), geo_scope='usa')
                
                # Display in Streamlit
                st.plotly_chart(fig, use_container_width=True)

                # Scatter plot with Error Bars
                fig = px.scatter(
                    df_county, 
                    x='REGION_NAME', 
                    y='5_17_POVERTY_PERCENT',
                    error_y='error_upper',
                    error_y_minus='error_lower',
                    labels={'REGION_NAME': 'Region Name', '5_17_POVERTY_PERCENT': 'Age 5-17 Poverty Percent'},
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
                st.dataframe(df_county[['REGION_NAME', '5_17_POVERTY_PERCENT', '5_17_90_CI_UPPER_PERCENT', '5_17_90_CI_LOWER_PERCENT']])

    # 0-17 AGES
        if age_level == "0-17":
        # NATIONAL DISPLAY
            # Display map based on user selection
            if map_level == "National":
                df_national = df[df['REGION_TYPE'] == 'NATIONAL']

                df_national['error_upper'] = df_national['0_17_90_CI_UPPER_PERCENT'] - df_national['0_17_POVERTY_PERCENT']
                df_national['error_lower'] = df_national['0_17_POVERTY_PERCENT'] - df_national['0_17_90_CI_LOWER_PERCENT']

                # Create the choropleth map
                fig = px.choropleth(
                    df_national,
                    locations='REGION_NAME', 
                    locationmode='country names',  # Location mode set to USA
                    color='0_17_POVERTY_PERCENT',  # Column for coloring
                    color_continuous_scale='Reds',  # Color scale
                    scope="usa",  # Focus the map on the USA
                    labels={'0_17_POVERTY_PERCENT': 'Age 0-17 Poverty Percent', 'REGION_NAME': 'Region Name'},  # Label for color scale
                    title='Poverty',  # Title of the map
                    hover_data={'REGION_NAME': True, '0_17_POVERTY_PERCENT': True}  # Add this line to specify the tooltip content
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
                    y='0_17_POVERTY_PERCENT',
                    error_y='error_upper',
                    error_y_minus='error_lower',
                    labels={'REGION_NAME': 'Region Name', '0_17_POVERTY_PERCENT': 'Ages 0-17 Poverty Percent'},
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
                st.dataframe(df_national[['REGION_NAME', '0_17_POVERTY_PERCENT', '0_17_90_CI_UPPER_PERCENT', '0_17_90_CI_LOWER_PERCENT']])


            # STATE DISPLAY
                
            elif map_level == "State":
                df_state = df[df['REGION_TYPE'] == 'STATE']

                df_state['error_upper'] = df_state['0_17_90_CI_UPPER_PERCENT'] - df_state['0_17_POVERTY_PERCENT']
                df_state['error_lower'] = df_state['0_17_POVERTY_PERCENT'] - df_state['0_17_90_CI_LOWER_PERCENT']

                # Create the choropleth map
                fig = px.choropleth(
                    df_state,
                    locations='POSTAL_CODE', 
                    locationmode='USA-states',  # Location mode set to USA
                    color='0_17_POVERTY_PERCENT',  # Column for coloring
                    color_continuous_scale='Reds',  # Color scale
                    scope="usa",  # Focus the map on the USA
                    labels={'0_17_POVERTY_PERCENT': 'Age 0-17 Poverty Percent', 'REGION_NAME': 'Region Name'},  # Label for color scale
                    title='Poverty',  # Title of the map
                    hover_data={'POSTAL_CODE': False, 'REGION_NAME': True, '0_17_POVERTY_PERCENT': True}  # Add this line to specify the tooltip content
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
                    y='0_17_POVERTY_PERCENT',
                    error_y='error_upper',
                    error_y_minus='error_lower',
                    labels={'REGION_NAME': 'Region Name', '0_17_POVERTY_PERCENT': 'Age 0-17 Poverty Percent'},
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
                st.dataframe(df_state[['REGION_NAME', '0_17_POVERTY_PERCENT', '0_17_90_CI_UPPER_PERCENT', '0_17_90_CI_LOWER_PERCENT']])

            # COUNTY DISPLAY

            elif map_level == "County":
                df_county = df[df['REGION_TYPE'] == 'COUNTY']

                df_county['error_upper'] = df_county['0_17_90_CI_UPPER_PERCENT'] - df_county['0_17_POVERTY_PERCENT']
                df_county['error_lower'] = df_county['0_17_POVERTY_PERCENT'] - df_county['0_17_90_CI_LOWER_PERCENT']

                # Create the choropleth map for counties
                fig = px.choropleth(
                    df_county,
                    geojson="https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json",
                    locations='FIPS_CODE',
                    color='0_17_POVERTY_PERCENT',
                    color_continuous_scale='Reds',
                    scope='usa',
                    labels={'0_17_POVERTY_PERCENT': 'Age 0-17 Poverty Percent', 'REGION_NAME': 'Region Name'},  # Label for color scale
                    title='Poverty',  # Title of the map
                    hover_data={'FIPS_CODE': False, 'REGION_NAME': True, '0_17_POVERTY_PERCENT': True}  # Add this line to specify the tooltip content
                )

                fig.update_layout(margin=dict(l=0, r=0, t=50, b=0), geo_scope='usa')
                
                # Display in Streamlit
                st.plotly_chart(fig, use_container_width=True)

                # Scatter plot with Error Bars
                fig = px.scatter(
                    df_county, 
                    x='REGION_NAME', 
                    y='0_17_POVERTY_PERCENT',
                    error_y='error_upper',
                    error_y_minus='error_lower',
                    labels={'REGION_NAME': 'Region Name', '0_17_POVERTY_PERCENT': 'Age 0-17 Poverty Percent'},
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
                st.dataframe(df_county[['REGION_NAME', '0_17_POVERTY_PERCENT', '0_17_90_CI_UPPER_PERCENT', '0_17_90_CI_LOWER_PERCENT']])

# Numbers
    if percent_or_number == 'Numbers':
    # ALL AGES
        if age_level == "All Ages":
        # NATIONAL DISPLAY
            # Display map based on user selection
            if map_level == "National":
                df_national = df[df['REGION_TYPE'] == 'NATIONAL']

                df_national['error_upper'] = df_national['ALL_AGES_90_CI_UPPER_BOUND'] - df_national['ALL_AGES_POVERTY_ESTIMATE']
                df_national['error_lower'] = df_national['ALL_AGES_POVERTY_ESTIMATE'] - df_national['ALL_AGES_90_CI_LOWER_BOUND']

                # Create the choropleth map
                fig = px.choropleth(
                    df_national,
                    locations='REGION_NAME', 
                    locationmode='country names',  # Location mode set to USA
                    color='ALL_AGES_POVERTY_ESTIMATE',  # Column for coloring
                    color_continuous_scale='Reds',  # Color scale
                    scope="usa",  # Focus the map on the USA
                    labels={'ALL_AGES_POVERTY_ESTIMATE': 'All Ages Poverty Value', 'REGION_NAME': 'Region Name'},  # Label for color scale
                    title='Poverty',  # Title of the map
                    hover_data={'REGION_NAME': True, 'ALL_AGES_POVERTY_ESTIMATE': True}  # Add this line to specify the tooltip content
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
                    y='ALL_AGES_POVERTY_ESTIMATE',
                    error_y='error_upper',
                    error_y_minus='error_lower',
                    labels={'REGION_NAME': 'Region Name', 'ALL_AGES_POVERTY_ESTIMATE': 'All Ages Poverty Value'},
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
                st.dataframe(df_national[['REGION_NAME', 'ALL_AGES_POVERTY_ESTIMATE', 'ALL_AGES_90_CI_UPPER_BOUND', 'ALL_AGES_90_CI_LOWER_BOUND']])


        # STATE DISPLAY
                
            elif map_level == "State":
                df_state = df[df['REGION_TYPE'] == 'STATE']

                df_state['error_upper'] = df_state['ALL_AGES_90_CI_UPPER_BOUND'] - df_state['ALL_AGES_POVERTY_ESTIMATE']
                df_state['error_lower'] = df_state['ALL_AGES_POVERTY_ESTIMATE'] - df_state['ALL_AGES_90_CI_LOWER_BOUND']

                # Create the choropleth map
                fig = px.choropleth(
                    df_state,
                    locations='POSTAL_CODE', 
                    locationmode='USA-states',  # Location mode set to USA
                    color='ALL_AGES_POVERTY_ESTIMATE',  # Column for coloring
                    color_continuous_scale='Reds',  # Color scale
                    scope="usa",  # Focus the map on the USA
                    labels={'ALL_AGES_POVERTY_ESTIMATE': 'All Ages Poverty Value', 'REGION_NAME': 'Region Name'},  # Label for color scale
                    title='Poverty',  # Title of the map
                    hover_data={'POSTAL_CODE': False, 'REGION_NAME': True, 'ALL_AGES_POVERTY_ESTIMATE': True}  # Add this line to specify the tooltip content
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
                    y='ALL_AGES_POVERTY_ESTIMATE',
                    error_y='error_upper',
                    error_y_minus='error_lower',
                    labels={'REGION_NAME': 'Region Name', 'ALL_AGES_POVERTY_ESTIMATE': 'All Ages Poverty Value'},
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
                st.dataframe(df_state[['REGION_NAME', 'ALL_AGES_POVERTY_ESTIMATE', 'ALL_AGES_90_CI_UPPER_BOUND', 'ALL_AGES_90_CI_LOWER_BOUND']])

            # COUNTY DISPLAY

            elif map_level == "County":
                df_county = df[df['REGION_TYPE'] == 'COUNTY']

                df_county['error_upper'] = df_county['ALL_AGES_90_CI_UPPER_BOUND'] - df_county['ALL_AGES_POVERTY_ESTIMATE']
                df_county['error_lower'] = df_county['ALL_AGES_POVERTY_ESTIMATE'] - df_county['ALL_AGES_90_CI_LOWER_BOUND']

                # Create the choropleth map for counties
                fig = px.choropleth(
                    df_county,
                    geojson="https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json",
                    locations='FIPS_CODE',
                    color='ALL_AGES_POVERTY_ESTIMATE',
                    color_continuous_scale='Reds',
                    scope='usa',
                    labels={'ALL_AGES_POVERTY_ESTIMATE': 'All Ages Poverty Value', 'REGION_NAME': 'Region Name'},  # Label for color scale
                    title='Poverty',  # Title of the map
                    hover_data={'FIPS_CODE': False, 'REGION_NAME': True, 'ALL_AGES_POVERTY_ESTIMATE': True}  # Add this line to specify the tooltip content
                )

                fig.update_layout(margin=dict(l=0, r=0, t=50, b=0), geo_scope='usa')
                
                # Display in Streamlit
                st.plotly_chart(fig, use_container_width=True)

                # Scatter plot with Error Bars
                fig = px.scatter(
                    df_county, 
                    x='REGION_NAME', 
                    y='ALL_AGES_POVERTY_ESTIMATE',
                    error_y='error_upper',
                    error_y_minus='error_lower',
                    labels={'REGION_NAME': 'Region Name', 'ALL_AGES_POVERTY_ESTIMATE': 'All Ages Poverty Value'},
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

    # 0-4
        if age_level == "0-4":
        # NATIONAL DISPLAY
            # Display map based on user selection
            if map_level == "National":
                df_national = df[df['REGION_TYPE'] == 'NATIONAL']

                df_national['error_upper'] = df_national['0_4_90_CI_UPPER_BOUND'] - df_national['0_4_POVERTY_ESTIMATE']
                df_national['error_lower'] = df_national['0_4_POVERTY_ESTIMATE'] - df_national['0_4_90_CI_LOWER_BOUND']

                # Create the choropleth map
                fig = px.choropleth(
                    df_national,
                    locations='REGION_NAME', 
                    locationmode='country names',  # Location mode set to USA
                    color='0_4_POVERTY_ESTIMATE',  # Column for coloring
                    color_continuous_scale='Reds',  # Color scale
                    scope="usa",  # Focus the map on the USA
                    labels={'0_4_POVERTY_ESTIMATE': 'Age 0-4 Poverty Value', 'REGION_NAME': 'Region Name'},  # Label for color scale
                    title='Poverty',  # Title of the map
                    hover_data={'REGION_NAME': True, '0_4_POVERTY_ESTIMATE': True}  # Add this line to specify the tooltip content
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
                    y='0_4_POVERTY_ESTIMATE',
                    error_y='error_upper',
                    error_y_minus='error_lower',
                    labels={'REGION_NAME': 'Region Name', '0_4_POVERTY_ESTIMATE': 'All Ages Poverty Value'},
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
                st.dataframe(df_national[['REGION_NAME', '0_4_POVERTY_ESTIMATE', '0_4_90_CI_UPPER_BOUND', '0_4_90_CI_LOWER_BOUND']])


            # STATE DISPLAY
                
            elif map_level == "State":
                df_state = df[df['REGION_TYPE'] == 'STATE']

                df_state['error_upper'] = df_state['0_4_90_CI_UPPER_BOUND'] - df_state['0_4_POVERTY_ESTIMATE']
                df_state['error_lower'] = df_state['0_4_POVERTY_ESTIMATE'] - df_state['0_4_90_CI_LOWER_BOUND']

                # Create the choropleth map
                fig = px.choropleth(
                    df_state,
                    locations='POSTAL_CODE', 
                    locationmode='USA-states',  # Location mode set to USA
                    color='0_4_POVERTY_ESTIMATE',  # Column for coloring
                    color_continuous_scale='Reds',  # Color scale
                    scope="usa",  # Focus the map on the USA
                    labels={'0_4_POVERTY_ESTIMATE': 'Age 0-4 Poverty Value', 'REGION_NAME': 'Region Name'},  # Label for color scale
                    title='Poverty',  # Title of the map
                    hover_data={'POSTAL_CODE': False, 'REGION_NAME': True, '0_4_POVERTY_ESTIMATE': True}  # Add this line to specify the tooltip content
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
                    y='0_4_POVERTY_ESTIMATE',
                    error_y='error_upper',
                    error_y_minus='error_lower',
                    labels={'REGION_NAME': 'Region Name', '0_4_POVERTY_ESTIMATE': 'Age 0-4 Poverty Value'},
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
                st.dataframe(df_state[['REGION_NAME', '0_4_POVERTY_ESTIMATE', '0_4_90_CI_UPPER_BOUND', '0_4_90_CI_LOWER_BOUND']])

            # COUNTY DISPLAY

            elif map_level == "County":
                df_county = df[df['REGION_TYPE'] == 'COUNTY']

                st.write("County data not available for ages 0-4.")

    # 5-17 AGES
        if age_level == "5-17":
        # NATIONAL DISPLAY
            # Display map based on user selection
            if map_level == "National":
                df_national = df[df['REGION_TYPE'] == 'NATIONAL']

                df_national['error_upper'] = df_national['5_17_90_CI_UPPER_BOUND'] - df_national['5_17_POVERTY_ESTIMATE']
                df_national['error_lower'] = df_national['5_17_POVERTY_ESTIMATE'] - df_national['5_17_90_CI_LOWER_BOUND']

                # Create the choropleth map
                fig = px.choropleth(
                    df_national,
                    locations='REGION_NAME', 
                    locationmode='country names',  # Location mode set to USA
                    color='5_17_POVERTY_ESTIMATE',  # Column for coloring
                    color_continuous_scale='Reds',  # Color scale
                    scope="usa",  # Focus the map on the USA
                    labels={'5_17_POVERTY_ESTIMATE': 'Age 5-17 Poverty Value', 'REGION_NAME': 'Region Name'},  # Label for color scale
                    title='Poverty',  # Title of the map
                    hover_data={'REGION_NAME': True, '5_17_POVERTY_ESTIMATE': True}  # Add this line to specify the tooltip content
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
                    y='5_17_POVERTY_ESTIMATE',
                    error_y='error_upper',
                    error_y_minus='error_lower',
                    labels={'REGION_NAME': 'Region Name', '5_17_POVERTY_ESTIMATE': 'Ages 5-17 Poverty Value'},
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
                st.dataframe(df_national[['REGION_NAME', '5_17_POVERTY_ESTIMATE', '5_17_90_CI_UPPER_BOUND', '5_17_90_CI_LOWER_BOUND']])


            # STATE DISPLAY
                
            elif map_level == "State":
                df_state = df[df['REGION_TYPE'] == 'STATE']

                df_state['error_upper'] = df_state['5_17_90_CI_UPPER_BOUND'] - df_state['5_17_POVERTY_ESTIMATE']
                df_state['error_lower'] = df_state['5_17_POVERTY_ESTIMATE'] - df_state['5_17_90_CI_LOWER_BOUND']

                # Create the choropleth map
                fig = px.choropleth(
                    df_state,
                    locations='POSTAL_CODE', 
                    locationmode='USA-states',  # Location mode set to USA
                    color='5_17_POVERTY_ESTIMATE',  # Column for coloring
                    color_continuous_scale='Reds',  # Color scale
                    scope="usa",  # Focus the map on the USA
                    labels={'5_17_POVERTY_ESTIMATE': 'Age 5-17 Poverty Value', 'REGION_NAME': 'Region Name'},  # Label for color scale
                    title='Poverty',  # Title of the map
                    hover_data={'POSTAL_CODE': False, 'REGION_NAME': True, '5_17_POVERTY_ESTIMATE': True}  # Add this line to specify the tooltip content
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
                    y='5_17_POVERTY_ESTIMATE',
                    error_y='error_upper',
                    error_y_minus='error_lower',
                    labels={'REGION_NAME': 'Region Name', '5_17_POVERTY_ESTIMATE': 'Age 5-17 Poverty Value'},
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
                st.dataframe(df_state[['REGION_NAME', '5_17_POVERTY_ESTIMATE', '5_17_90_CI_UPPER_BOUND', '5_17_90_CI_LOWER_BOUND']])

            # COUNTY DISPLAY

            elif map_level == "County":
                df_county = df[df['REGION_TYPE'] == 'COUNTY']

                df_county['error_upper'] = df_county['5_17_90_CI_UPPER_BOUND'] - df_county['5_17_POVERTY_ESTIMATE']
                df_county['error_lower'] = df_county['5_17_POVERTY_ESTIMATE'] - df_county['5_17_90_CI_LOWER_BOUND']

                # Create the choropleth map for counties
                fig = px.choropleth(
                    df_county,
                    geojson="https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json",
                    locations='FIPS_CODE',
                    color='5_17_POVERTY_ESTIMATE',
                    color_continuous_scale='Reds',
                    scope='usa',
                    labels={'5_17_POVERTY_ESTIMATE': 'Age 5-17 Poverty Value', 'REGION_NAME': 'Region Name'},  # Label for color scale
                    title='Poverty',  # Title of the map
                    hover_data={'FIPS_CODE': False, 'REGION_NAME': True, '5_17_POVERTY_ESTIMATE': True}  # Add this line to specify the tooltip content
                )

                fig.update_layout(margin=dict(l=0, r=0, t=50, b=0), geo_scope='usa')
                
                # Display in Streamlit
                st.plotly_chart(fig, use_container_width=True)

                # Scatter plot with Error Bars
                fig = px.scatter(
                    df_county, 
                    x='REGION_NAME', 
                    y='5_17_POVERTY_ESTIMATE',
                    error_y='error_upper',
                    error_y_minus='error_lower',
                    labels={'REGION_NAME': 'Region Name', '5_17_POVERTY_ESTIMATE': 'Age 5-17 Poverty Value'},
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
                st.dataframe(df_county[['REGION_NAME', '5_17_POVERTY_ESTIMATE', '5_17_90_CI_UPPER_BOUND', '5_17_90_CI_LOWER_BOUND']])

    # 0-17 AGES
        if age_level == "0-17":
        # NATIONAL DISPLAY
            # Display map based on user selection
            if map_level == "National":
                df_national = df[df['REGION_TYPE'] == 'NATIONAL']

                df_national['error_upper'] = df_national['0_17_90_CI_UPPER_BOUND'] - df_national['0_17_POVERTY_ESTIMATE']
                df_national['error_lower'] = df_national['0_17_POVERTY_ESTIMATE'] - df_national['0_17_90_CI_LOWER_BOUND']

                # Create the choropleth map
                fig = px.choropleth(
                    df_national,
                    locations='REGION_NAME', 
                    locationmode='country names',  # Location mode set to USA
                    color='0_17_POVERTY_ESTIMATE',  # Column for coloring
                    color_continuous_scale='Reds',  # Color scale
                    scope="usa",  # Focus the map on the USA
                    labels={'0_17_POVERTY_ESTIMATE': 'Age 0-17 Poverty Value', 'REGION_NAME': 'Region Name'},  # Label for color scale
                    title='Poverty',  # Title of the map
                    hover_data={'REGION_NAME': True, '0_17_POVERTY_ESTIMATE': True}  # Add this line to specify the tooltip content
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
                    y='0_17_POVERTY_ESTIMATE',
                    error_y='error_upper',
                    error_y_minus='error_lower',
                    labels={'REGION_NAME': 'Region Name', '0_17_POVERTY_ESTIMATE': 'Ages 0-17 Poverty Value'},
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
                st.dataframe(df_national[['REGION_NAME', '0_17_POVERTY_ESTIMATE', '0_17_90_CI_UPPER_BOUND', '0_17_90_CI_LOWER_BOUND']])


            # STATE DISPLAY
                
            elif map_level == "State":
                df_state = df[df['REGION_TYPE'] == 'STATE']

                df_state['error_upper'] = df_state['0_17_90_CI_UPPER_BOUND'] - df_state['0_17_POVERTY_ESTIMATE']
                df_state['error_lower'] = df_state['0_17_POVERTY_ESTIMATE'] - df_state['0_17_90_CI_LOWER_BOUND']

                # Create the choropleth map
                fig = px.choropleth(
                    df_state,
                    locations='POSTAL_CODE', 
                    locationmode='USA-states',  # Location mode set to USA
                    color='0_17_POVERTY_ESTIMATE',  # Column for coloring
                    color_continuous_scale='Reds',  # Color scale
                    scope="usa",  # Focus the map on the USA
                    labels={'0_17_POVERTY_ESTIMATE': 'Age 0-17 Poverty Value', 'REGION_NAME': 'Region Name'},  # Label for color scale
                    title='Poverty',  # Title of the map
                    hover_data={'POSTAL_CODE': False, 'REGION_NAME': True, '0_17_POVERTY_ESTIMATE': True}  # Add this line to specify the tooltip content
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
                    y='0_17_POVERTY_ESTIMATE',
                    error_y='error_upper',
                    error_y_minus='error_lower',
                    labels={'REGION_NAME': 'Region Name', '0_17_POVERTY_ESTIMATE': 'Age 0-17 Poverty Value'},
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
                st.dataframe(df_state[['REGION_NAME', '0_17_POVERTY_ESTIMATE', '0_17_90_CI_UPPER_BOUND', '0_17_90_CI_LOWER_BOUND']])

            # COUNTY DISPLAY

            elif map_level == "County":
                df_county = df[df['REGION_TYPE'] == 'COUNTY']

                df_county['error_upper'] = df_county['0_17_90_CI_UPPER_BOUND'] - df_county['0_17_POVERTY_ESTIMATE']
                df_county['error_lower'] = df_county['0_17_POVERTY_ESTIMATE'] - df_county['0_17_90_CI_LOWER_BOUND']

                # Create the choropleth map for counties
                fig = px.choropleth(
                    df_county,
                    geojson="https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json",
                    locations='FIPS_CODE',
                    color='0_17_POVERTY_ESTIMATE',
                    color_continuous_scale='Reds',
                    scope='usa',
                    labels={'0_17_POVERTY_ESTIMATE': 'Age 0-17 Poverty Value', 'REGION_NAME': 'Region Name'},  # Label for color scale
                    title='Poverty',  # Title of the map
                    hover_data={'FIPS_CODE': False, 'REGION_NAME': True, '0_17_POVERTY_ESTIMATE': True}  # Add this line to specify the tooltip content
                )

                fig.update_layout(margin=dict(l=0, r=0, t=50, b=0), geo_scope='usa')
                
                # Display in Streamlit
                st.plotly_chart(fig, use_container_width=True)

                # Scatter plot with Error Bars
                fig = px.scatter(
                    df_county, 
                    x='REGION_NAME', 
                    y='0_17_POVERTY_ESTIMATE',
                    error_y='error_upper',
                    error_y_minus='error_lower',
                    labels={'REGION_NAME': 'Region Name', '0_17_POVERTY_ESTIMATE': 'Age 0-17 Poverty Value'},
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
                st.dataframe(df_county[['REGION_NAME', '0_17_POVERTY_ESTIMATE', '0_17_90_CI_UPPER_BOUND', '0_17_90_CI_LOWER_BOUND']])