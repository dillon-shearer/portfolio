import streamlit as st
import plotly.express as px

# Main function for the analysis pages
def show():
    # Set up the page
    st.title("SAIPE Poverty/Income: Project Home")
    st.write("Dillon Shearer - 2024")
    st.write("------")

    st.write("## Welcome to the 2022 Census SAIPE Poverty Data Analysis and Visualization App")
    st.write("*Explore a comprehensive and interactive analysis of poverty data across the United States.*")
    st.write("This app provides insights into poverty metrics at national, state, and county levels based on the 2022 Census SAIPE data. Dive into various visualizations to understand the landscape of poverty and median household incomes in different regions.")
    st.write("**Features**:")
    st.write("- Interactive maps highlighting poverty rates and median incomes.")
    st.write("- Detailed bar and line charts showcasing demographic and economic trends.")
    st.write("- Customizable data views with intuitive filters and selectors.")
    st.write("Whether you're a policy maker, researcher, student, or just curious about socioeconomic trends, this app offers valuable data-driven perspectives.")
    st.write("-----")
    st.write("### **Get Started**: Use the sidebar to navigate through different sections and visualizations.")