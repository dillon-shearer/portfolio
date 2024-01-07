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
