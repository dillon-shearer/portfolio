import panel as pn
import pandas as pd
import os
from functools import partial

# Import the story modules
from stories import income_inequality
from stories import urbanization_trends
from stories import healthcare_access
from stories import education_gaps
# Add imports for other stories as needed

# Ensure no global template is set
pn.config.template = None

# Initialize Panel extension without setting a global template
pn.extension(sizing_mode="stretch_width")

# Define paths
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, 'data')
ASSETS_PATH = os.path.join(BASE_DIR, 'assets')
DATA_PATH = os.path.join(DATA_DIR, 'stories.csv')

# Load Stories Data
try:
    stories_df = pd.read_csv(DATA_PATH)
    print("Loaded stories:")
    print(stories_df)
except FileNotFoundError:
    stories_df = pd.DataFrame(columns=["Title", "Description", "Source Tables"])
    print(f"Error: '{DATA_PATH}' not found. Please ensure the CSV file exists.")

# Load Custom CSS
custom_css = os.path.join(ASSETS_PATH, 'styles.css')
if os.path.exists(custom_css):
    with open(custom_css) as f:
        css = f.read()
    pn.config.raw_css.append(css)
    print("Loaded custom CSS.")
else:
    print(f"Error: '{custom_css}' not found. Please ensure the CSS file exists.")

# Define the main content
main_content = pn.Column(
    pn.pane.Markdown("<h1 class='main-title'>Welcome to Society in Numbers</h1>", sizing_mode='stretch_width'),
    pn.pane.Markdown("""
    <div class='main-description'>
    This platform presents a collection of data-driven stories that delve into various societal issues. 
    Use the sidebar to navigate through different topics and explore the underlying data and analyses.

    <h2>Topics Include:</h2>
    <ul>
        <li><strong>Income Inequality</strong></li>
        <li><strong>Urbanization Trends</strong></li>
        <li><strong>Healthcare Access</strong></li>
        <li><strong>Education Gaps</strong></li>
        <li><strong>And many more!</strong></li>
    </ul>

    <p>Stay tuned for in-depth analyses and visualizations.</p>
    </div>
    <hr>
    """, sizing_mode='stretch_width'),
    sizing_mode='stretch_width',
    css_classes=['main-content']
)

# Function to update the sidebar collapsed state
def update_sidebar(show_sidebar):
    template.sidebar_collapsed = not show_sidebar

# Define functions to update the main content
def show_main_page(event=None):
    """
    Callback to display the main page.
    """
    print("Navigating to main page")
    main_content[:] = [
        pn.pane.Markdown("<h1 class='main-title'>Welcome to Society in Numbers</h1>", sizing_mode='stretch_width'),
        pn.pane.Markdown("""
        <div class='main-description'>
        This platform presents a collection of data-driven stories that delve into various societal issues. 
        Use the sidebar to navigate through different topics and explore the underlying data and analyses.

        <h2>Topics Include:</h2>
        <ul>
            <li><strong>Income Inequality</strong></li>
            <li><strong>Urbanization Trends</strong></li>
            <li><strong>Healthcare Access</strong></li>
            <li><strong>Education Gaps</strong></li>
            <li><strong>And many more!</strong></li>
        </ul>

        <p>Stay tuned for in-depth analyses and visualizations.</p>
        </div>
        <hr>
        """, sizing_mode='stretch_width')
    ]
    update_sidebar(show_sidebar=True)  # Show sidebar on main page

def show_story(index, event=None):
    """
    Callback to display a specific story page based on the index.
    """
    print(f"Navigating to story index: {index}")
    if index >= len(stories_df):
        back_button = pn.widgets.Button(name='← Back to Home', button_type='primary', css_classes=['sidebar-link'])
        back_button.on_click(show_main_page)
        main_content[:] = [
            pn.pane.Markdown("## Story Not Found", sizing_mode='stretch_width'),
            back_button
        ]
        update_sidebar(show_sidebar=False)  # Collapse sidebar on sub-pages
        return

    story = stories_df.iloc[index]
    title = story['Title']
    description = story['Description']
    source_tables = story['Source Tables']

    # Dispatch to the appropriate story module based on the title
    if title == 'Income Inequality in America':
        # Get the content from the income_inequality module
        content = income_inequality.get_content()
        main_content[:] = [content]
    elif title == 'The Changing Face of Urbanization':
        content = urbanization_trends.get_content()
        main_content[:] = [content]
    elif title == 'Healthcare Access and Outcomes':
        content = healthcare_access.get_content()
        main_content[:] = [content]
    elif title == 'Education Gaps Across Demographics':
        content = education_gaps.get_content()
        main_content[:] = [content]
    # Add more elif clauses for other stories
    else:
        # For stories without a specific module, show a placeholder
        back_button = pn.widgets.Button(name='← Back to Home', button_type='primary', css_classes=['sidebar-link'])
        back_button.on_click(show_main_page)
        main_content[:] = [
            pn.pane.Markdown(f"## {title}", sizing_mode='stretch_width'),
            pn.pane.Markdown(description, sizing_mode='stretch_width'),
            pn.pane.Markdown(f"**Source Tables:** {source_tables}", sizing_mode='stretch_width'),
            pn.pane.Markdown("### Content coming soon...", sizing_mode='stretch_width'),
            back_button
        ]
    update_sidebar(show_sidebar=False)  # Collapse sidebar on sub-pages

# Create sidebar buttons (without the Home button)
sidebar_buttons = []

for idx, row in stories_df.iterrows():
    button = pn.widgets.Button(name=row['Title'], button_type='primary', css_classes=['sidebar-link'])
    button.on_click(partial(show_story, idx))
    sidebar_buttons.append(button)

# Define the sidebar
sidebar = pn.Column(
    pn.pane.Markdown("## Stories", sizing_mode='stretch_width'),
    *sidebar_buttons,
    sizing_mode='stretch_height',
    css_classes=['sidebar'],
    width=325  # Match the CSS sidebar width
)

# Initialize the template without 'sidebar_collapsed' in the constructor
template = pn.template.FastListTemplate(
    title='Society in Numbers',
    header_background='#2c3e50',
    sidebar=[sidebar],
    main=[main_content],
    accent_base_color="#2980b9",
    theme='dark',  # Set to dark mode
    theme_toggle=False  # Disable theme toggle
    # Do not set sidebar_collapsed here
)

# Set sidebar_collapsed after initialization
template.sidebar_collapsed = False  # Sidebar visible on main page

# Serve the Application
template.servable()
