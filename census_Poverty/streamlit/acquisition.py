import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="SAIPE Data Acquisition",
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
def show():
    # Set up the page
    st.title("SAIPE Poverty/Income: Data Acquisition")
    st.write("Dillon Shearer")
