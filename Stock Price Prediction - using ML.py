import streamlit as st, pandas as pd, numpy as np, yfinance as yf 
import plotly.express as px
import datetime 
import ptvsd

st.title('Stock Dashboard')
ticker = st.sidebar.text_input('Ticker')
start_date = st.sidebar.date_input('Start Date')
end_date = st.sidebar.date_input('End Date')


data = yf.download(ticker, start=start_date, end=end_date)

fig = px.line(data, x = data.index, y = data['Adj Close'], title = ticker)
st.plotly_chart(fig)

pricing_data, fundamental_data, news = st.tabs(["Pricing data","Fundamental data","Top 10 news"])

with pricing_data:
    st.write('Price movement')
    st.write('Ticker: {ticker}')
    data2 = data
    data2['% Change'] = data['Adj Close'] / data['Adj Close'].shift(1) -1
    data2.dropna(inplace= True)
    st.write(data2)
    annual_return = data2['% Change'].mean()*252*100
    st.write('Annual Return is ',annual_return,'%')
    stdev = np.std(data2['% Change'])*np.sqrt(252)
    st.write('Standard Deviation is ',stdev*100,'%')
    st.write('Rick Ajl. Retrun is ',annual_return/(stdev*100))
    st.write(data)






from stocknews import StockNews
with news:
    st.header(f'News of {ticker}')
    sn = StockNews(ticker, save_news=False)
    df_news = sn.read_rss()
    for i in range(10):
        st.subheader(f'News of{i+1}')
        st.write(df_news['published'][i])
        st.write(df_news['title'][i])
        st.write(df_news['summary'][i])
        title_sentiment = df_news['sentiment_title'][i]
        st.write(f'Title Sentiment {title_sentiment}')
        news_sentiment = df_news['sentiment_summary'][i]
        st.write(f'News Seniment {news_sentiment}')

    st.write('News')






from alpha_vantage.fundamentaldata import FundamentalData 
with fundamental_data:
    key = 'OW1639L63B5UCYYL'
    fd = FundamentalData(key,output_format = 'pandas')
    st.subheader('Balance Sheet')
    balance_sheet = fd.get_balance_sheet_annual(ticker)[0]
    bs = balance_sheet.T[2:]
    bs.columns = list(balance_sheet.T.iloc[0])
    st.write(bs)
    st.subheader('Income Statement')
    income_statement = fd.get_income_statement_annual(ticker)[0]
    is1 = income_statement.T[2:]
    is1.columns = list(income_statement.T.iloc[0])
    st.write(is1)
    st.subheader('Cash Flow Statement')
    cash_flow = fd.get_cash_flow_annual(ticker[0])
    cf = cash_flow[0].T[2:]
    cf.columns = list(cash_flow[0].T.iloc[0])
    st.write(cf)

    st.write('Fundamental')

