import yahoo_news as yn
code = "2330.TW"
news_data = yn.get_yahoo_news(f"{code}")
print(news_data)
news_data.to_csv(f'/Users/tseng/Desktop/程式交易/stock_news_{code}.csv')