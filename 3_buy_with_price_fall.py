import sys
sys.path.append('/Users/tseng/Desktop/python')
import utility_f as uf
import pandas as pd
import yfinance as yf
import numpy as np
import datetime
import time
import traceback
try:
    data = pd.read_csv('/Users/tseng/Desktop/python/stocklist.csv')
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

    stock_store = []
    today_store = []
    today_fall = []
    count = 0
    for target in target_stock:
        count+=1
        time.sleep(1)
        stock = yf.Ticker(f'{target}.TW')
        df = stock.history(start=date_start, end=date_end)
        if len(df)>=5:
            today_price = df['Close'].values[-1]
            yes_price = df['Close'].values[-2]
            be_yes_price = df['Close'].values[-3]
            fall_today = ((today_price-yes_price)/yes_price)*100
            fall_yes = ((yes_price-be_yes_price)/be_yes_price)*100
            if fall_today<=-5 and fall_today<=-5:
                today_store.append(today_price)
                today_fall.append(fall_today)
                stock_store.append(target)
            print(f'Dealing Stock: {target} | All Stock: {len(target_stock)} | Now: {count}')
    control = 0
    for t in stock_store:
        time.sleep(1)
        if control==0:
            main_df = uf.get_yahoo_news(t)
            main_df['stock'] = len(main_df)*[t]
            control+=1
        else:
            merge_df = uf.get_yahoo_news(t)
            merge_df['stock'] = len(merge_df)*[t]
            main_df = pd.concat([main_df,merge_df],axis=0, ignore_index=True)
    main_df.to_csv(f'/Users/tseng/Desktop/python/fall_stock_news.csv', index=False)
    empty_dataframe = pd.DataFrame()
    empty_dataframe['股票代號'] = stock_store
    empty_dataframe['今價'] = today_store
    empty_dataframe['今日跌幅%'] = today_fall
    empty_dataframe = empty_dataframe.to_html(index=False)
    body = f'''<html>
                <font face="微軟正黑體"></font>
                <body>
                <h4>
                小幫手系列偵測下表股票為暴跌中股票 
                </h4>
                {empty_dataframe}
                <h5>投資理財有賺有賠，請謹慎評估風險</h5>
                </body>
                </html>'''
    mail_list = ['adam880614@gmail.com']
    subject = f'{today}  小幫手暴跌中股票偵測'
    uf.send_mail(mail_list, subject, body,'html', [f'/Users/tseng/Desktop/python/fall_stock_news.csv'], ['相關新聞表.csv'])
except SystemExit:
    print('Its OK')
except:
    today = datetime.date.today()
    mail_list = ['adam880614@gmail.com']
    subject = f'{today}  小幫手暴跌中股票異常'
    body = traceback.format_exc()
    uf.send_mail(mail_list, subject, body,'text', None, None)