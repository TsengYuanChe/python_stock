import requests 
import json
import pandas as pd
import sys
sys.path.append('/Users/tseng/Desktop/python')
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from AES_Encryption.encrype_process import *
import datetime
from bs4 import BeautifulSoup

#是否開盤用函數，返回字串Ｙ、Ｎ，Ｙ代表有開盤，Ｎ反之
'''
target_date = 傳入datetime格式日期，為需要判斷是否開盤的日期
'''
def is_open(target_date:datetime.date):
    hd = pd.read_csv(r"/Users/tseng/Desktop/程式交易/holiday.csv")
    hd_date = pd.to_datetime(hd['日期']).tolist()
    str_date = target_date.strftime('%Y%m%d')
    day = target_date.weekday()
    if day == 5 or day == 6:
        return 'N'
    for i in hd_date:
        i = i.strftime('%Y%m%d')
        if (i==str_date):
            return 'N'
    return 'Y'
#三大法人買賣超日報，返回一份dataframe
'''
r_date = 字串格式日期，為需要查詢三大法人買賣超日報的目標日期
'''
def twes_data(r_date:str):
    data = requests.get(f"https://www.twse.com.tw/rwd/zh/fund/T86?date={r_date}&selectType=ALLBUT0999&response=json&_=1711790204370")
    data_json = json.loads(data.text)
    data_store = pd.DataFrame(data_json['data'],columns=data_json['fields'])
    return data_store
#寄信函數
'''
mail_list = 列表，需要寄信的清單
subject = 字串，標題
body = 字串，內容
mode = 字串，支援text跟html兩種寄信模式
file_path = 列表，想要寄出的檔案位置
file_name = 列表，希望收件者看到的檔名
'''
def send_mail(mail_list:list, subject:str, body:str, mode:str, file_path:list, file_name:list):
    msg = MIMEMultipart()
    user_id = 'adam880501@gmail.com'
    password = 'xuei svsj vybf mtpp'
    msg['From'] = user_id
    msg['To'] = ",".join(mail_list)
    msg['Subject'] = subject
    if mode =='html':
        msg.attach(MIMEText(body, mode))
    else:
        msg.attach(MIMEText(body))
    if file_path==None:
        pass
    else:
        for x in range(len(file_path)):
            with open(file_path[x], 'rb') as opened:
                openedfile = opened.read()
            attachedfile = MIMEApplication(openedfile)
            attachedfile.add_header('content-disposition', 'attachment', filename= file_name[x])
            msg.attach(attachedfile)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(user_id, password)
    text = msg.as_string()
    server.sendmail(user_id, mail_list, text)
    server.quit()
#取得新聞
'''
stock = 字串，目標股票
target_page = 好像用不了
'''
def get_yahoo_news(stock: str):
    try:
        headers = {
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
        data = requests.get(f"https://tw.stock.yahoo.com/quote/{stock}/news",headers=headers)
        soup = BeautifulSoup(data.text,"html.parser")
        all_news = soup.find_all("h3",{"class":"Mt(0) Mb(8px)"})
        all_news_store = []
        for a in all_news:
            news_path = a.find("a")["href"]
            if news_path[-4:] == "html":
                all_news_store.append(news_path)

        date_store, title_store = [], []
        for new in all_news_store:
            each_data = requests.get(f"{new}", headers=headers)
            each_soup = BeautifulSoup(each_data.text,"html.parser")
            title = each_soup.find("h1",{"data-test-locator": "headline"}).text
            news_time = each_soup.find("div",{"class":"caas-attr-time-style"}).text
            news_time = news_time.split(" ")[0]
            news_time = news_time.replace("年","/")
            news_time = news_time.replace("月","/")
            news_time = news_time.replace("日","")
            title_store.append(title)
            date_store.append(news_time)
        result = pd.DataFrame()
        result["title"] = title_store
        result["date"] = date_store
        result["url"] = all_news_store
    except:
        result = pd.DataFrame()
        result['title'] = ['Error']
        result["url"] = ['Error']
        result["date"] = ['Error']
    return result
