import ta
import yfinance as yf
import pandas as pd
import mpl_finance as mpf
import matplotlib.pyplot as plt
stock = yf.Ticker('2330.TW')
df = stock.history(start="2017-01-01",end="2021-02-02")
indicator_bb = ta.volatility.BollingerBands(close=df["Close"],window=20,window_dev=2)
df['bbm'] = indicator_bb.bollinger_mavg()
df['bbh'] = indicator_bb.bollinger_hband()
df['bbl'] = indicator_bb.bollinger_lband()
fig = plt.figure(figsize=(24,8))
grid = plt.GridSpec(3,20)
ax = fig.add_subplot(grid[0:2,1:])
ax2 = fig.add_subplot(grid[2:,1:])
mpf.candlestick2_ochl(ax, df['Open'], df['Close'], df['High'], df['Low'], width=0.6, colorup='r', colordown='g', alpha=0.75)
mpf.volume_overlay(ax2, df['Open'], df['Close'], df['Volume'], colorup='r', colordown='g')
convert_date = pd.DataFrame(df.index[::30])['Date'].apply(lambda x: x.strftime('%Y-%m-%d'))
ax.plot(df['bbm'].values, color='b', label = 'bbm')
ax.plot(df['bbh'].values, color='g', label = 'bbh')
ax.plot(df['bbl'].values, color='r', label = 'bbl')
ax.set_xticks(range(0, len(df.index), 30))
ax.set_xticklabels(convert_date, rotation=90, fontsize=6)
ax2.set_xticks(range(0, len(df.index), 30))
ax2.set_xticklabels(convert_date, rotation=90, fontsize=6)
ax.set_title(f'2330 Stock Price')
ax.set_xlabel('Date')
ax.set_ylabel("Price")
fig.tight_layout()
ax.legend()
plt.savefig('/Users/tseng/Desktop/程式交易/test_fig.png')
plt.show()