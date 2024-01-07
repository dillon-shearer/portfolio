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

# Navigation
st.sidebar.title("Navigation")
choice = st.sidebar.radio("Go to", ["Home", "Poverty Map", "Median Income Map", "Analysis"])

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
