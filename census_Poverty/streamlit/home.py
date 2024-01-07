import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="SAIPE Data Analysis Home",
    page_icon="📊",  # Example: using an emoji as icon
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a Bug': None,  # Removing the 'Report a Bug' option
        'About': "This app is used for analyzing poverty/median income data."
    }
)

# Main function for the analysis pages
def show_home():
    # Set up the page
    st.title("Census Poverty Data Exploration")
    st.show("Dillon Shearer")
