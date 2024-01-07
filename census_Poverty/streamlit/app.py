import streamlit as st
import analysis
import home

# Navigation
st.sidebar.title("Navigation")
choice = st.sidebar.radio("Go to", ["Home", "Analysis"])


if __name__ == "__main__":
    # Page routing
    if choice == "Home":
        home.show()
    elif choice == "Analysis":
        analysis.show()