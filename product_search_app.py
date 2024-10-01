import streamlit as st
import pandas as pd

# Load the product data
file_path = 'Data Base of product .xlsx'
data_df = pd.read_excel(file_path, sheet_name='Sheet1')

# Strip spaces from column names to avoid errors
data_df.columns = data_df.columns.str.strip()

# Streamlit app
st.title("Product Search App")

# User input for product name search
search_term = st.text_input("Enter product name to search:", key="product_search_input")

if search_term:
    # Filter the dataframe by product name
    results = data_df[data_df['Product Name'].str.contains(search_term, case=False, na=False)]
    
    if not results.empty:
        st.write("Search Results:")
        
        # Allow users to update "Months for Stock" values using an input widget
        for index in results.index:
            updated_value = st.number_input(
                f"Update 'Months for Stock' for {results.at[index, 'Product Name']}:",
                min_value=0, value=int(results.at[index, 'Months for Stock']), step=1, key=f"stock_{index}"
            )
            results.at[index, 'Months for Stock'] = updated_value
            
        # Recalculate "Stock for Months" using the correct formula: (1yr Stock / 12) * Months for Stock
        results['Stock for Months'] = ((results['1yr Stock'] / 12) * results['Months for Stock']).round(0)
        
        # Select the columns to display in the specified order
        st.dataframe(results[['item Number', 'Almacen', 'Product Name', 'Stock for Months', 'Months for Stock', '1yr Stock']])
    else:
        st.write("No products found with that name.")
