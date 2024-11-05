import pandas as pd
import datetime
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
today = datetime.date.today()
test = is_open(today)
print(today,test)
