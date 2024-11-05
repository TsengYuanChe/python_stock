import sys
sys.path.append('/Users/tseng/Desktop/程式交易')
import utility_f as uf
import datetime
import os
import pandas as pd
import traceback
try:
    today = datetime.date.today()
    if_trade = uf.is_open(today)
    if if_trade=='N':
        mail_list = ['adam880614@gmail.com']
        subject = f'{today} 小幫手三大法人 - 今日休市'
        body = ''
        uf.send_mail(mail_list, subject, body, 'text', None, None)
        exit()
    control = 0
    for i in range(0,10):
        if control <= 2:
            date_target = today + datetime.timedelta(days = -int(1))
            if_trade = uf.is_open(date_target)
            if if_trade=='N':
                continue
            else:
                convert_date = date_target.strftime('%Y%m%d')
                data = uf.twes_data(convert_date)
                data.to_csv(f'{convert_date}_twse.csv')
                data = pd.read_csv(f'{convert_date}_twse.csv',thousands=',')
                os.remove(f'{convert_date}_twse.csv')
                d_s = data[(data[u'三大法人買賣超股數']>0)]
                d_s = d_s[:50]
                print(len(d_s))
                if control==0:
                    result = set(d_s[u'證券代號'].tolist())
                else:
                    result = result.intersection(set(d_s[u'證券代號'].tolist()))
                control+=1
        else:
            break
    mail_list = ['adam880614@gmail.com']
    result = ",".join(result)
    subject = f'{today} 小幫手三大法人篩選'
    body = f'目標股票{result} 連續三日法人買超'
    uf.send_mail(mail_list, subject, body, 'text', None, None)
except SystemExit:
    print('Its OK')
except:
    mail_list = ['adam880614@gmail.com']
    subject = f'{today} 小幫手三大法人篩選異常'
    body = traceback.format_exc()
    uf.send_mail(mail_list, subject, body, 'text', None, None)
    