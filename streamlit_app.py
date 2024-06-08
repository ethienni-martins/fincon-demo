import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
    
    # Use Streamlit columns for layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write(df)
    
    with col2:
        st.markdown(
            f"""
            <div style="text-align: right; font-size: 20px; font-weight: bold;">
                <p>Oldest Date: {oldest_date}</p>
                <p>Newest Date: {newest_date}</p>
                <p>Total Value for 'Tarifas - Pagamento': {total_value_formatted}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Display bar chart below the dataframe
    st.write("## Total Value for 'Tarifas - Pagamento'")
    fig, ax = plt.subplots()
    ax.bar(['Total Value'], [total_value])
    ax.set_ylabel('Value (R$)')
    ax.set_title("Total Value for 'Tarifas - Pagamento'")
    st.pyplot(fig)

else:
    st.write("Please upload an Excel or CSV file to proceed.")
