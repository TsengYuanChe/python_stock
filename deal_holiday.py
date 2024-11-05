import pandas as pd
import datetime
today = datetime.date.today()
convert_today = today.strftime('%Y')
x = pd.read_csv("/Users/tseng/Desktop/python/holidaySchedule_113.csv", encoding='big5')
d = []
for i in range(1,x.size):
    y = str(x.index[i]).split('(')[1]
    z = y.find('月')
    a = y.find('日')
    if y[z-2]=='1':
        d.append(y[z-2:a+1])
    else:
        d.append(y[z-1:a+1])
df = pd.DataFrame(d)
df.columns = ['日期']

df['日期'] = df['日期'].apply(lambda x:convert_today+'年'+x)
df['日期'] = df['日期'].apply(lambda x:x.replace('年','/'))
df['日期'] = df['日期'].apply(lambda x:x.replace('月','/'))
df['日期'] = df['日期'].apply(lambda x:x.replace('日',''))
print(df['日期'])
df['日期'].to_csv('/Users/tseng/Desktop/程式交易/holiday.csv')

