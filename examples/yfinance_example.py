import yfinance as yf
stock = yf.Ticker('2330.TW')
df = stock.history(period='max')
print(df)