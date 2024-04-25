import streamlit as st

st.set_page_config(
    page_title="Homepage",
    page_icon="🎯",
)

st.title("Olympic Analyzer")
    
st.image('../images/olympics 1.png')
st.write("""
    ## Welcome to the Olympic Analyzer!
    
    This project helps you store data & perform some analysis related to the Olympic event including data about athletes, sports type, and medals earned.
    
    Navigate through the sidebar to perform various operations.
    
    ### Features:
    - Perform CRUD operations on all the possible data
    - Visualize data to calculate metrics
    - Search Functionality to search for specific athletes, events, or medals
    
    ### Get Started:
    - Click on the sidebar to explore different functionalities.
    """)







