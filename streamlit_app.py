import streamlit as st
import pandas as pd

# Title of the app
st.title('Oldest and Newest Dates Finder')

# Upload the file
uploaded_file = st.file_uploader("Upload your Excel or CSV file", type=["xlsx", "csv"])

if uploaded_file is not None:
    # Determine the file type and read the file accordingly
    if uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)
    elif uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    
    # Display the dataframe
    st.write("DataFrame", df)
    
    # Assuming the date column is named 'data'
    if 'data' in df.columns:
        # Convert the date column to datetime format
        df['data'] = pd.to_datetime(df['data'])
        
        # Find the oldest and newest dates
        oldest_date = df['data'].min()
        newest_date = df['data'].max()
        
        # Display the results
        st.write("Oldest Date:", oldest_date)
        st.write("Newest Date:", newest_date)
    else:
        st.write("The uploaded file does not contain a 'date' column.")
else:
    st.write("Please upload an Excel or CSV file to proceed.")
