import utility_f as uf
import pandas as pd
import yfinance as yf
import numpy as np
import datetime
import traceback
try:
    data = pd.read_csv('/Users/tseng/Desktop/python/dividend_list.csv')
    target_stock = data['代號'].tolist()
    today = datetime.date.today()
    if_trade = uf.is_open(today)
    if if_trade=='N':
        mail_list = ['adam880614@gmail.com']
        subject = f'{today} 小幫手高配息低股價，每日價格比對 - 今日休市'
        body = ''
        uf.send_mail(mail_list, subject, body, 'text', None, None)
        exit()

    date_start = today + datetime.timedelta(days=-365)
    date_start = date_start.strftime('%Y-%m-%d')
    date_end = today + datetime.timedelta(days=1)
    date_end = date_end.strftime('%Y-%m-%d')

    target_store = []
    highest_store = []
    now_price_store = []
    for target in target_stock:
        stock = yf.Ticker(f'{target}.TW')
        df = stock.history(start = date_start, end = date_end)
        highest = np.max(df['High'].values)
        now_price = df['Close'].values[-1]
        if now_price<highest*0.7:
            target_store.append(target)
            highest_store.append(highest)
            now_price_store.append(now_price)
            print(f'Stock: {target} | high 70%: {highest*0.7} | now: {now_price} | Status : Get!')
    all_stock_list = pd.read_csv('/Users/tseng/Desktop/python/stocklist.csv')
    stock_name_store = []
    for st in target_store:
        select_data = all_stock_list[(all_stock_list[u'代號']==st)]
        target = select_data['股票名稱'].values[0]
        stock_name_store.append(target)
    empty_df = pd.DataFrame()
    empty_df['日期'] = len(target_store)*[today]
    empty_df['股票代號'] = target_store
    empty_df['股票名稱'] = stock_name_store
    empty_df['最近收盤'] = now_price_store
    empty_df['一年內最高'] = highest_store
    empty_df = empty_df.to_html(index=False)
    body = f'''<html>
                <font face="微軟正黑體"></font>
                <body>
                <h4>
                小幫手系列偵測下表股票配後高且股價相對低
                </h4>
                {empty_df}
                <h5>投資理財有賺有賠，請謹慎評估風險</h5>
                </body>
                </html>'''
    mail_list = ['adam880614@gmail.com']
    subject = f'{today} 小幫手高配息低股價-每日比對價格'
    uf.send_mail(mail_list, subject, body, 'html', None, None)
except SystemExit:
    print('Its OK')
except:
    today = datetime.date.today()
    mail_list = ['adam880614@gmail.com']
    subject = f'{today}  小幫手高配息低股價-每日價格比對異常'
    body = traceback.format_exc()
    uf.send_mail(mail_list, subject, body,'text', None, None)