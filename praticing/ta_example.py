import ta
import yfinance as yf
stock = yf.Ticker('2330.TW')
df = stock.history(start='2017-01-01',end='2021-02-02')
#data = ta.add_all_ta_features(df,"Open","High","Low","Close","Volume",fillna=True) #產生所有指標
#ma = ta.trend.SMAIndicator(df['Close'],10,fillna=True)
#ma = ma.sma_indicator() #移動平均
indicator_bb = ta.volatility.BollingerBands(close=df["Close"],window=20,window_dev=2)
bb_bbm = indicator_bb.bollinger_mavg() #中線
bb_bbh = indicator_bb.bollinger_hband() #上線
bb_bbl = indicator_bb.bollinger_lband() #下線
bb_bbhi = indicator_bb.bollinger_hband_indicator() #大於上軌返回1
bb_bbli = indicator_bb.bollinger_lband_indicator() #小於下軌返回1
bb_bbw = indicator_bb.bollinger_wband() #帶寬
bb_bbp = indicator_bb.bollinger_pband() #％b值
print('布林中線\n',bb_bbm)