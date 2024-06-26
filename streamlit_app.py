import streamlit as st
import pandas as pd
import altair as alt

# Function to format currency in Brazilian notation with parentheses for negative values
def format_currency(value):
    if value < 0:
        return f"(R$ {abs(value):,.2f})".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# Function to convert Brazilian formatted string to float
def convert_to_float(value):
    return float(value.replace('R$ ', '').replace('.', '').replace(',', '.'))

# Display the logo at the top of the page
st.image("Rationiric_Logo_(Name)_white background.jpg", width=250)
st.markdown("---")


# Title of the app
st.title('Extrato Completo')

# Upload the file
uploaded_file = st.file_uploader("Faca o upload do arquivo Excel ou CSV ", type=["xlsx", "csv"])

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
    
    # Ensure all currency columns are numeric for calculations
    currency_columns = ['Saldo Inicial', 'Valor', 'Saldo Final']
    for col in currency_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col].replace({'R\$ ': '', '\.': '', ',': '.'}, regex=True), errors='coerce').fillna(0)
    
    # Apply currency formatting for display
    for col in currency_columns:
        if col in df.columns:
            df[f'{col}_formatted'] = df[col].apply(format_currency)
    
    # Search for the specific string in the "Histórico" column and sum the values in the "Valor" column
    if 'Histórico' in df.columns and 'Valor' in df.columns:
        # Sum values for 'Tarifas - Pagamento'
        tarifas_mask = df['Histórico'].str.contains('Tarifas - Pagamento', na=False)
        total_value = df.loc[tarifas_mask, 'Valor'].sum()
        total_value_formatted = format_currency(total_value)
        
        # Sum values for 'Pix'
        pix_mask = df['Histórico'].str.contains('Pix', na=False, case=False)
        pix_values = df.loc[pix_mask, 'Valor']
        pix_recebido = pix_values[pix_values > 0].sum()
        pagamento_via_pix = pix_values[pix_values < 0].sum()
        
        pix_recebido_formatted = format_currency(pix_recebido)
        pagamento_via_pix_formatted = format_currency(pagamento_via_pix)
    else:
        st.write("O arquivo carregado não tem a coluna 'Histórico' ou 'Valor' ")
        total_value_formatted = pix_recebido_formatted = pagamento_via_pix_formatted = None
    
    # Use Streamlit columns for layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write(df)
    
    with col2:
        st.markdown(
            f"""
            <div style="text-align: right; font-size: 20px; font-weight: bold;">
                <p>Data Inicial: {oldest_date}</p>
                <p>Data Final: {newest_date}</p>
                <p>Valor Total de 'Tarifas - Pagamento': {total_value_formatted}</p>
                <p>Pix Recebido: {pix_recebido_formatted}</p>
                <p>Pagamento - Pix: {pagamento_via_pix_formatted}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Toggle button state using session state for both charts
    if 'show_tarifas_chart' not in st.session_state:
        st.session_state.show_tarifas_chart = False
    if 'show_pix_chart' not in st.session_state:
        st.session_state.show_pix_chart = False
    
    # Buttons to show charts
    col3, col4 = st.columns([1, 1])
    with col3:
        if st.button("Total de Tarifas"):
            st.session_state.show_tarifas_chart = not st.session_state.show_tarifas_chart
            st.session_state.show_pix_chart = False
    with col4:
        if st.button("Total de Pagamento - Pix"):
            st.session_state.show_pix_chart = not st.session_state.show_pix_chart
            st.session_state.show_tarifas_chart = False
    
    # Display chart based on button clicks
    if st.session_state.show_tarifas_chart:
        st.write("## Valor Total de 'Tarifas - Pagamento'")
        st.write("### Gráfico de 'Tarifas - Pagamento'")

        # Prepare data for the histogram
        tarifas_data = df.loc[tarifas_mask, ['Data', 'Valor']]
        tarifas_data['Data'] = tarifas_data['Data'].dt.strftime('%d-%m-%Y')
        tarifas_data_grouped = tarifas_data.groupby('Data').sum().reset_index()

        # Create the Altair chart
        chart = alt.Chart(tarifas_data_grouped).mark_bar(color='red').encode(
            x=alt.X('Data:O', axis=alt.Axis(title='Date', labelAngle=-45)),
            y=alt.Y('Valor:Q', axis=alt.Axis(title='Amount', labelExpr="datum.value < 0 ? '(' + format(-datum.value, ',.2f') + ')' : format(datum.value, ',.2f')")),
            tooltip=[alt.Tooltip('Data:O', title='Date'), alt.Tooltip('Valor:Q', title='Amount')]
        ).properties(
            width=600,
            height=400
        ).configure_axis(
            labelFontSize=12,
            titleFontSize=14
        ).configure_title(
            fontSize=16
        )

        st.altair_chart(chart, use_container_width=True)

    if st.session_state.show_pix_chart:
        st.write("## Valor Total de 'Pagamento - Pix'")
        st.write("### Gráfico de 'Pagamento - Pix'")

        # Prepare data for the histogram
        pix_data = df.loc[pix_mask, ['Data', 'Valor']]
        pix_data['Data'] = pix_data['Data'].dt.strftime('%d-%m-%Y')
        pix_data_grouped = pix_data.groupby('Data').sum().reset_index()

        # Create the Altair chart
        chart = alt.Chart(pix_data_grouped).mark_bar(color='blue').encode(
            x=alt.X('Data:O', axis=alt.Axis(title='Date', labelAngle=-45)),
            y=alt.Y('Valor:Q', axis=alt.Axis(title='Amount', labelExpr="datum.value < 0 ? '(' + format(-datum.value, ',.2f') + ')' : format(datum.value, ',.2f')")),
            tooltip=[alt.Tooltip('Data:O', title='Date'), alt.Tooltip('Valor:Q', title='Amount')]
        ).properties(
            width=600,
            height=400
        ).configure_axis(
            labelFontSize=12,
            titleFontSize=14
        ).configure_title(
            fontSize=16
        )

        st.altair_chart(chart, use_container_width=True)
else:
    st.write("Please upload an Excel or CSV file to proceed.")
