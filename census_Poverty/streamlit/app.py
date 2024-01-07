import streamlit as st
import home
import poverty
import median_income
import acquisition
import cleaning
import analysis


# Navigation
st.sidebar.title("Navigation")
choice = st.sidebar.radio("Go to", ["Home", "Analysis"])

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


if __name__ == "__main__":
    # Page routing
    if choice == "Home":
        home.show()
    elif choice == "Poverty":
        poverty.show()
    elif choice == "Median Income":
        median_income.show()
    elif choice == "Acquisition":
        acquisition.show()
    elif choice == "Cleaning":
        cleaning.show()
    elif choice == "Analysis":
        analysis.show()
