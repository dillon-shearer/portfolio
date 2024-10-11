import panel as pn
import pandas as pd
import os
import hvplot.pandas  # For plotting
import geopandas as gpd  # For mapping
import numpy as np

# Define paths
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # Go up one level from stories directory
DATA_DIR = os.path.join(BASE_DIR, 'data')
CLEAN_DATA_DIR = os.path.join(DATA_DIR, 'clean')

# Define custom CSS class for dark grey panel
pn.extension(raw_css=[("""
    .custom-dark-panel {
        background-color: #4a4a4a;  /* Dark grey background */
        color: white;  /* Text color to contrast the dark background */
        border-radius: 10px;
        padding: 20px;
        box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.3); /* Optional shadow */
    }
""")])

def get_content():
    """
    Returns the content for the 'Income Inequality in America' dashboard.
    """
    title = 'Income Inequality in America'
    data_file = os.path.join(CLEAN_DATA_DIR, 'income_story_data_cleaned.csv')

    # Load the data
    try:
        data = pd.read_csv(data_file)
        print(f"Loaded data for story '{title}' from '{data_file}'")
    except FileNotFoundError:
        data = None
        print(f"Error: Data file '{data_file}' not found for story '{title}'.")

    # If data is None, display an error message
    if data is None:
        return pn.pane.Markdown("## Data not available.")

    # Data preprocessing
    data['Year'] = data['Year'].astype(int)
    data = data.sort_values(['State', 'Year'])
    data = data[data['Year'] >= 2019]

    # Impute missing 2020 data using linear interpolation
    def impute_2020(group):
        years = group['Year'].values
        if 2020 not in years and 2019 in years and 2021 in years:
            year_2019 = group[group['Year'] == 2019]
            year_2021 = group[group['Year'] == 2021]
            interpolated = year_2019.copy()
            interpolated['Year'] = 2020
            numeric_cols = interpolated.select_dtypes(include=np.number).columns
            for col in numeric_cols:
                interpolated[col] = (year_2019[col].values + year_2021[col].values) / 2
            group = pd.concat([group, interpolated], ignore_index=True)
        return group

    data = data.groupby('State', as_index=False).apply(impute_2020)
    data.reset_index(drop=True, inplace=True)
    data = data.sort_values(['State', 'Year'])

    # Prepare widgets
    year_slider = pn.widgets.IntSlider(
        name='Year',
        start=data['Year'].min(),
        end=data['Year'].max(),
        step=1,
        value=data['Year'].max(),
        sizing_mode='stretch_width'
    )

    # State selector
    states = ['All'] + sorted(data['State'].unique())
    state_selector = pn.widgets.Select(
        name='State',
        options=states,
        value='All',
        sizing_mode='stretch_width'
    )

    # Define demographic categories and subgroups
    demographic_categories = ['All', 'Gender', 'Race', 'Ethnicity']

    demographic_subgroups = {
        'All': {'All': 'Median_Income_All'},
        'Gender': {
            'Male': 'Median_Earnings_Male',
            'Female': 'Median_Earnings_Female'
        },
        'Race': {
            'White': 'Median_Income_White',
            'Black': 'Median_Income_Black',
            'AIAN': 'Median_Income_AIAN',
            'Asian': 'Median_Income_Asian',
            'NHPI': 'Median_Income_NHPI',
            'Other': 'Median_Income_Other',
            'Two Races': 'Median_Income_Two_Races'
        },
        'Ethnicity': {
            'White Non-Hispanic': 'Median_Income_White_Non_Hispanic',
            'Hispanic': 'Median_Income_Hispanic'
        }
    }

    # Main filter: Demographic Category
    demographic_category_selector = pn.widgets.Select(
        name='Demographic Category',
        options=demographic_categories,
        value='All',
        sizing_mode='stretch_width'
    )

    # Sub-filter: Subgroups CheckBoxGroup
    subgroups_widget = pn.widgets.CheckBoxGroup(name='Subgroups', options=['All'], value=['All'], sizing_mode='stretch_width')

    # Function to update subgroups based on selected demographic category
    def update_subgroups_widget(event=None):
        if event is not None:
            category = event.new
        else:
            category = demographic_category_selector.value  # Use the current value
        subgroups = list(demographic_subgroups[category].keys())
        subgroups_widget.options = subgroups
        subgroups_widget.value = subgroups  # Default to all selected

    demographic_category_selector.param.watch(update_subgroups_widget, 'value')

    # Initialize subgroups_widget with the initial category
    update_subgroups_widget()

    # Function to filter data based on widgets
    @pn.depends(
        year_slider.param.value,
        state_selector.param.value,
        demographic_category_selector.param.value,
        subgroups_widget.param.value
    )
    def update_plots(selected_year, selected_state, selected_category, selected_subgroups):
        filtered_data = data[data['Year'] == selected_year]

        if selected_state == 'All':
            # Use data where State == 'National'
            filtered_data = filtered_data[filtered_data['State'] == 'National']
        else:
            filtered_data = filtered_data[filtered_data['State'] == selected_state]

        if filtered_data.empty:
            return pn.pane.Markdown("## No data available for the selected filters.")

        # Get the columns corresponding to the selected subgroups
        subgroup_columns = [
            demographic_subgroups[selected_category][subgroup]
            for subgroup in selected_subgroups
            if subgroup in demographic_subgroups[selected_category]
        ]

        if not subgroup_columns:
            return pn.pane.Markdown("## No subgroups selected.")

        # Prepare data for plotting
        plot_data = filtered_data[['State', 'Year'] + subgroup_columns]

        # Melt the data for plotting
        plot_data_melted = plot_data.melt(
            id_vars=['State', 'Year'],
            var_name='Subgroup',
            value_name='Value'
        )

        # Map column names back to subgroup names
        column_to_subgroup = {v: k for k, v in demographic_subgroups[selected_category].items()}
        plot_data_melted['Subgroup'] = plot_data_melted['Subgroup'].map(column_to_subgroup)

        # Bar Plot Widget (Median Income/Earnings)
        plot_widget = pn.Card(
            plot_data_melted.hvplot.bar(
                x='Subgroup',
                y='Value',
                title=f'{selected_category} Median Income/Earnings',
                xlabel=selected_category,
                ylabel='Amount ($)',
                rot=45,
                width=400,
                height=300
            ).opts(bgcolor='white', toolbar=None, responsive=True),  # Enable responsive behavior
            title="Median Income/Earnings",
            css_classes=['custom-dark-panel'],
            sizing_mode='stretch_both',  # Ensures the card resizes dynamically
            margin=(10, 10, 10, 10)
        )

        # Gini Index Over Time Plot widget
        gini_data = data.copy()
        if selected_state == 'All':
            gini_data = gini_data[gini_data['State'] == 'National']
        else:
            gini_data = gini_data[gini_data['State'] == selected_state]

        # Gini Index Over Time Widget
        gini_widget = pn.Card(
            gini_data.hvplot.line(
                x='Year',
                y='Gini_Index',
                title='Gini Index Over Time',
                xlabel='Year',
                ylabel='',
                width=400,
                height=300
            ).opts(
                bgcolor='white',
                xformatter='%d',  # Formatter to ensure whole numbers
                xticks=list(range(gini_data['Year'].min(), gini_data['Year'].max() + 1)),  # Whole years
                toolbar=None, 
                responsive=True  # Enable responsive behavior
            ),
            title="Gini Index Over Time",
            css_classes=['custom-dark-panel'],
            sizing_mode='stretch_both',  # Ensures the card resizes dynamically
            margin=(10, 10, 10, 10)
        )

        # Map Visualization widget
        us_states_url = 'https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json'
        try:
            us_states = gpd.read_file(us_states_url)
            print("Loaded US states GeoJSON.")
        except Exception as e:
            us_states = None
            print(f"Error loading US states GeoJSON: {e}")

        if us_states is not None:
            map_variable = 'Median_Income_All'
            map_data = data[data['Year'] == selected_year]
            map_data = map_data[map_data['State'] != 'National']  # Exclude 'National' for mapping
            map_df = us_states.merge(map_data, left_on='name', right_on='State', how='left')

            # Map Widget (Median Income by State)
            map_widget = pn.Card(
                map_df.hvplot.polygons(
                    'geometry',
                    geo=True,
                    tiles='CartoLight',
                    c=map_variable,
                    cmap='viridis',
                    colorbar=True,
                    title=f'Median Income by State in {selected_year}',
                    clim=(map_data[map_variable].min(), map_data[map_variable].max()),
                    hover_cols=['State'],
                    width=800,
                    height=400,
                    responsive=True,  # Enable responsive behavior
                    xaxis=None,  # Disable x-axis
                    yaxis=None   # Disable y-axis
                ).opts(bgcolor='white', toolbar=None),
                title="Median Income by State Map",
                css_classes=['custom-dark-panel'],
                sizing_mode='stretch_both',  # Ensures the card resizes dynamically
                margin=(10, 10, 10, 10)
            )
        else:
            map_widget = pn.pane.Markdown("Unable to load US states GeoJSON for mapping.", width=400, height=300)

        # Arrange plots in widget/tile style
        plots = pn.Column(
            pn.Column(map_widget, sizing_mode='stretch_both'),  # Map widget full width
            pn.Spacer(height=15),
            pn.Row(
                pn.Column(plot_widget, sizing_mode='stretch_both'),
                pn.Spacer(width=15),
                pn.Column(gini_widget, sizing_mode='stretch_both'),
                sizing_mode='stretch_both'
            ),
            sizing_mode='stretch_both'
        )

        return plots

    # Dashboard Layout
    filters_row = pn.Row(
        pn.WidgetBox('#### Select Demographic Category', demographic_category_selector),
        pn.WidgetBox('#### Select Subgroups', subgroups_widget),
        pn.WidgetBox('#### Filters', year_slider, state_selector),
        sizing_mode='stretch_width'
    )

    # Reset button
    reset_button = pn.widgets.Button(name='Reset Filters', button_type='primary')

    def reset_filters(event):
        year_slider.value = data['Year'].max()  # Reset to most recent year
        state_selector.value = 'All'
        demographic_category_selector.value = 'All'
        subgroups_widget.value = ['All']

    reset_button.on_click(reset_filters)

    dashboard = pn.Column(
        pn.pane.Markdown(f"## {title}", sizing_mode='stretch_width'),
        pn.layout.Divider(),
        update_plots,
        pn.layout.Divider(),
        filters_row,
        reset_button,
        sizing_mode='stretch_both'  # Ensure the entire dashboard is responsive
    )

    return dashboard