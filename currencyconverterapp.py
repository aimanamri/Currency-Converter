import streamlit as st
from PIL import Image
import pandas as pd
import requests

st.set_page_config(layout="wide")
image = Image.open('img2.png')
st.image(image,width=300)

st.title('Currency Converter App')
st.markdown('''
This app converts the value of foreign currencies.
''')
st.beta_container()
# Sidebar + Main Panel
st.sidebar.header('Input Options')

# Sidebar - Currency price unit
currencyList = ['JPY','IDR','MYR','USD','SGD','KRW','CNY']
amount = st.sidebar.number_input('Enter some amount')
rates =1.2

base_price_unit = st.sidebar.selectbox('Select base currency',currencyList)
symbols_price_unit =st.sidebar.selectbox('Select target currency to convert to',currencyList)

# Retrieving currency data from ratesapi.io
@st.cache
def load_data(): # Not finish yet, trying to get the API token key from the wwebsite
    url = ''.join(['https://api.ratesapi.io/api/latest?base=',base_price_unit,'&symbols=',symbols_price_unit])
    response = requests.get(url)
    data = response.json()
    base_currency = pd.Series(data['base'],name='base_currency')
    rates_df = pd.DataFrame.from_dict(data['rates'].items())
    rates_df.columns = ['converted_currency','price']
    conversion_date = pd.Series(data['date'],name='date')
    df = pd.concat([base_currency,rates_df,conversion_date],axis=1)
    pass
df = load_data
st.header('Currency conversion')
st.write(df)
st.write(f'{base_price_unit} {amount}     ⇒     {symbols_price_unit} {round(amount*rates,2)}')

st.subheader('Idea ↓')
image = Image.open('img.jpg')
st.image(image,width=900)

# About
footer = st.beta_expander('About')
footer.markdown('''
- **Python libraries: ** streamlit, pandas
- **Data source: ** [ratesapi.io](https://www.ratesapi.io)
''')