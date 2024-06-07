import streamlit as st
import pandas as pd

# Title of the app
st.title('Oldest and Newest Dates Finder')

# Upload the Excel file
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file is not None:
    # Read the Excel file
    df = pd.read_excel(uploaded_file)
    
    # Display the dataframe
    st.write("DataFrame", df)
    
    # Assuming the date column is named 'date'
    if 'date' in df.columns:
        # Convert the date column to datetime format
        df['date'] = pd.to_datetime(df['date'])
        
        # Find the oldest and newest dates
        oldest_date = df['date'].min()
        newest_date = df['date'].max()
        
        # Display the results
        st.write("Oldest Date:", oldest_date)
        st.write("Newest Date:", newest_date)
    else:
        st.write("The uploaded file does not contain a 'date' column.")
else:
    st.write("Please upload an Excel file to proceed.")
