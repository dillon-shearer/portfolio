import streamlit as st
import home
import poverty
import median_income
import analysis

# Set page configuration
st.set_page_config(
    page_title="SAIPE Data Analysis",
    page_icon="📊",  # Example: using an emoji as icon
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a Bug': None,  # Removing the 'Report a Bug' option
        'About': "This app is used for analyzing poverty/median income data."
    }
)

import streamlit as st

# Custom CSS to improve the appearance of the sidebar
st.markdown("""
    <style>
    .sidebar .sidebar-content {
        color: #333;               /* Darker text for better readability */
        font-family: 'Arial';      /* Modern font */
    }
    .css-1d391kg {
        padding-top: 1rem;        /* More space at the top */
        padding-bottom: 1rem;     /* More space at the bottom */
    }
    .stRadio > label {
        display: block;
        color: #4a4a4a;          /* Dark grey for radio options */
        font-weight: bold;       /* Bold font for options */
        font-size: 16px;         /* Larger font size */
        margin-bottom: 15px;     /* Spacing between options */
    }
    .stRadio > div {
        border-radius: 10px;       /* Rounded corners for radio buttons area */
        padding: 10px;             /* Padding inside the radio buttons area */
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("Navigation")
choice = st.sidebar.radio("Go to", ["Home", "Poverty Map", "Median Income Map", "Analysis"])

# Footer or additional information
st.sidebar.markdown("---")
st.sidebar.info("Streamlit App v1.0")

if __name__ == "__main__":
    # Page routing
    if choice == "Home":
        home.show()
    elif choice == "Poverty Map":
        poverty.show()
    elif choice == "Median Income Map":
        median_income.show()
    elif choice == "Analysis":
        analysis.show()
