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
    
    # Convert the 'Data' column to datetime format if it exists
    if 'Data' in df.columns:
        df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
        
        # Find the oldest and newest dates
        oldest_date = df['Data'].min().strftime('%d-%m-%Y')
        newest_date = df['Data'].max().strftime('%d-%m-%Y')
    else:
        st.write("The uploaded file does not contain a 'Data' column.")
        oldest_date = newest_date = total_value_formatted = None
    
    # Search for the specific string in the "Histórico" column and sum the values in the "Valor" column
    if 'Histórico' in df.columns and 'Valor' in df.columns:
        df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce').fillna(0)
        mask = df['Histórico'].str.contains('Tarifas - Pagamento', na=False)
        total_value = df.loc[mask, 'Valor'].sum()
        total_value_formatted = f"R$ {total_value:.2f}"
    else:
        st.write("The uploaded file does not contain the required 'Histórico' or 'Valor' columns.")
        total_value_formatted = None
    
    # Display the dataframe and results side by side
    st.markdown(
        f"""
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div style="flex: 1; width: 48%; font-size: 12px; margin-right: 2%;">
                {df.to_html(index=False)}
            </div>
            <div style="flex: 0 0 48%; text-align: right; font-size: 20px; font-weight: bold;">
                <p>Oldest Date: {oldest_date}</p>
                <p>Newest Date: {newest_date}</p>
                <p>Total Value for 'Tarifas - Pagamento': {total_value_formatted}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.write("Please upload an Excel or CSV file to proceed.")
