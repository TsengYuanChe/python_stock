import pandas as pd
import yfinance as yf
stock = yf.Ticker('2330.TW')
df = stock.history(start="2017-01-01",end="2021-02-02")
O_C_high = df['High'].rolling(6).apply(lambda x : x[0]-x[-1])
df['OCHIGH'] = O_C_high
df.to_csv('/Users/tseng/Desktop/程式交易/pd_practice.csv')