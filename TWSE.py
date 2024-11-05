#selectType 產業別 in url
import requests 
import json
import pandas as pd
def twes_data(r_date:str):
    data = requests.get(f"https://www.twse.com.tw/rwd/zh/fund/T86?date={r_date}&selectType=ALLBUT0999&response=json&_=1711790204370")
    data_json = json.loads(data.text)
    data_store = pd.DataFrame(data_json['data'],columns=data_json['fields'])
    return data_store
