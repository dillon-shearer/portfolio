import streamlit as st
import analysis
import home

# Navigation
st.sidebar.title("Navigation")
choice = st.sidebar.radio("Go to", ["Home", "Analysis"])


if __name__ == "__app__":
    # Page routing
    if choice == "Home":
        home.show_home()
    elif choice == "Analysis":
        analysis.show_analysis()