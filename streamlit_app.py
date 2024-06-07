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
    
    # Try to find the date column
    date_column = None
    for col in df.columns:
        try:
            # Attempt to convert to datetime with the specified format
            df[col] = pd.to_datetime(df[col], format='%Y-%m-%d', errors='coerce')
            if df[col].notna().all():
                date_column = col
                break
        except (ValueError, TypeError):
            continue
    
    if date_column:
        # Find the oldest and newest dates
        oldest_date = df[date_column].min()
        newest_date = df[date_column].max()
        
        # Display the results
        st.write(f"Date Column: {date_column}")
        st.write("Oldest Date:", oldest_date)
        st.write("Newest Date:", newest_date)
    else:
        st.write("The uploaded file does not contain a recognizable date column in 'YYYY-MM-DD' format.")
    
    # Search for the specific string in the "Histórico" column and sum the values in the "Valor" column
    if 'Histórico' in df.columns and 'Valor' in df.columns:
        # Convert 'Valor' column to numeric, forcing errors to NaN and then fill NaN with 0
        df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce').fillna(0)
        mask = df['Histórico'] == 'Tarifas - Pagamento recebido:'
        total_value = df.loc[mask, 'Valor'].sum()
        st.write("Total Value for 'Tarifas - Pagamento recebido:':", total_value)
    else:
        st.write("The uploaded file does not contain the required 'Histórico' or 'Valor' columns.")
else:
    st.write("Please upload an Excel or CSV file to proceed.")
