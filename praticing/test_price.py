import yahoo_price as yp
stock_list = ['2330.TW','2317.TW','2324.TW']
for x in stock_list:
    price = yp.stock_price(x)
    print('股票:',x,'| 價格:', price)