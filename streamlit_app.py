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
        
        # Sum values for 'Tarifas - Pagamento'
        tarifas_mask = df['Histórico'].str.contains('Tarifas - Pagamento', na=False)
        total_value = df.loc[tarifas_mask, 'Valor'].sum()
        total_value_formatted = f"R$ {total_value:.2f}"
        
        # Sum values for 'Pix'
        pix_mask = df['Histórico'].str.contains('Pix', na=False, case=False)
        pix_values = df.loc[pix_mask, 'Valor']
        pix_recebido = pix_values[pix_values > 0].sum()
        pagamento_via_pix = pix_values[pix_values < 0].sum()
        
        pix_recebido_formatted = f"R$ {pix_recebido:.2f}"
        pagamento_via_pix_formatted = f"R$ {pagamento_via_pix:.2f}"
    else:
        st.write("The uploaded file does not contain the required 'Histórico' or 'Valor' columns.")
        total_value_formatted = pix_recebido_formatted = pagamento_via_pix_formatted = None
    
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
                <p>Pix Recebido: {pix_recebido_formatted}</p>
                <p>Pagamento via Pix: {pagamento_via_pix_formatted}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Toggle button state using session state
    if 'show_chart' not in st.session_state:
        st.session_state.show_chart = False
    
    if st.button("Total de Tarifas"):
        st.session_state.show_chart = not st.session_state.show_chart
    
    if st.session_state.show_chart:
        st.write("## Total Value for 'Tarifas - Pagamento'")
        st.bar_chart(pd.DataFrame({'Total Value': [total_value]}))
else:
    st.write("Please upload an Excel or CSV file to proceed.")
