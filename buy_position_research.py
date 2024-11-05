from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
import yfinance as yf
import numpy as np

# Import the backtrader platform
import backtrader as bt
import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns

stock_df = pd.read_csv('stock_list.csv')
stock_code_list = []
stop_days = 1
for i in range(0,len(stock_df['代號'])):
    code = str(stock_df['代號'][i])
    stock_code_list.append(f'{code}.TW')
stock_code_list1 = stock_code_list[1:10]
result_per = []
result_list = []
for code in range(0,len(stock_code_list)):
    data = yf.Ticker(stock_code_list[code])
    data = data.history(start = '2020-01-01', end = '2023-12-31')
    count = 0
    index = 0
    for i in range(30,len(data)-stop_days):
        condition1 = data['High'][i-1] == max(data['High'])
        condition2 = data['Close'][i-2] > data['Close'][i-1] and data['Close'][i] > data['Close'][i-1] and data['Close'][i-3] < data['Close'][i-2]
        condition3 = data['High'][i] == data['Close'][i]
        if condition1 and condition2:
            if data['Close'][i+stop_days]-data['Close'][i] > 0:
                index += 1
                count += 1
            else:
                index += 0
                count += 1
    if count == 0:
        rat = 'None'
    else:
        rat = (index/count)*100
    print(code, stock_df['股票名稱'][code], count, index, rat)
    con_data = [stock_df['股票名稱'][code], count, index, rat]
    result_list.append(con_data)
df_col = ['Name', 'Times', 'Success','Ratio']
result_df = pd.DataFrame(result_list, columns = df_col)
result_df.to_csv('test.csv')
df = pd.read_csv('test.csv')
ratio = df['Ratio']
sns.displot(ratio, kind='kde')
mean = np.mean(ratio)
median = np.nanmedian(ratio)

plt.axvline(mean, color='red', linestyle='dashed', linewidth=2, label='Mean')
plt.axvline(median, color='green', linestyle='dashed', linewidth=2, label='Median')
plt.text(mean, plt.ylim()[1]*0.9, f'Mean: {mean:.2f}', color='red', ha='center')
plt.text(median, plt.ylim()[1]*0.8, f'Median: {median:.2f}', color='green', ha='center')

plt.legend()
plt.savefig(f'png/test_{stop_days}.png')
plt.show()

