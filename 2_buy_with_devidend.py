import yfinance as yf
import pandas as pd
import numpy as np
import time
import datetime
import traceback
import utility_f as uf
try:
    stock_list = pd.read_csv('/Users/tseng/Desktop/python/stocklist.csv')
    all_stock = stock_list['代號'].values
    dividend_store = []
    stock_store = []
    count = 0
    for i in all_stock:
        start = time.time()
        count+=1
        stock = yf.Ticker(f'{i}.TW')
        try:
            if stock.info['dividendYield'] != None:
                d_y = stock.info['dividendYield']
                if d_y!=None and d_y>=0.05:
                    stock_store.append(i)
                    dividend_store.append(d_y)
            else:
                d_y=None
            end = time.time()
            print(f'Dealing: {count} | All: {len(all_stock)} | Stock: {i}| DY: {d_y} | Cost Time: {end-start}s')
        except:
            print(f'Error Stock ! Dealing: {count} | All: {len(all_stock)} | Stock: {i}')
    data = pd.DataFrame()
    data['代號'] = stock_store
    data['殖利率'] = dividend_store
    data.to_csv('/Users/tseng/Desktop/python/dividend_list.csv')
except SystemError:
    print('Its OK')
except:
    today = datetime.date.today()
    mail_list = ['adam880614@gmail.com']
    subject = f'{today} 小幫手三大法人篩選異常'
    body = traceback.format_exc()
    uf.send_mail(mail_list, subject, body, 'text', None, None)