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
    
    # Check if the 'Data' column exists
    if 'Data' in df.columns:
        # Convert the 'Data' column to datetime format
        df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
        
        # Find the oldest and newest dates
        oldest_date = df['Data'].min()
        newest_date = df['Data'].max()
        
        # Display the results
        st.write("Date Column: Data")
        st.write("Oldest Date:", oldest_date)
        st.write("Newest Date:", newest_date)
    else:
        st.write("The uploaded file does not contain a 'Data' column.")
    
    # Search for the specific string in the "Histórico" column and sum the values in the "Valor" column
    if 'Histórico' in df.columns and 'Valor' in df.columns:
        # Convert 'Valor' column to numeric, forcing errors to NaN and then fill NaN with 0
        df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce').fillna(0)
        mask = df['Histórico'].str.contains('Tarifas - Pagamento', na=False)
        total_value = df.loc[mask, 'Valor'].sum()
        st.write("Total Value for 'Tarifas - Pagamento':", total_value)
    else:
        st.write("The uploaded file does not contain the required 'Histórico' or 'Valor' columns.")
else:
    st.write("Please upload an Excel or CSV file to proceed.")
