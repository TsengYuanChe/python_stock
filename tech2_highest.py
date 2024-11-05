#%%
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
# Create a Stratey
class Highest_high(bt.Strategy):
    params = (
        ('highest', 6),
        ('in_amount', 4),
        ('stoploss', 0.1),
        ('takeprofit', 0.2)
    )

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.datahigh = self.datas[0].high
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # Add a MovingAverageSimple indicator
        self.the_highest_high = bt.ind.Highest(self.datahigh, period = self.params.highest)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if self.position.size < self.params.in_amount*1000:

            # Not yet ... we MIGHT BUY if ...
            if self.datahigh > self.the_highest_high[-1]:

                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log('BUY CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()
        if self.position.size != 0:
            costs = self.position.price
            if self.dataclose[0] > costs + (costs*self.params.takeprofit):
                self.close()
                self.log('Take Profit, %.2f' % self.dataclose[0])
            elif self.dataclose[0] < costs - (costs*self.params.stoploss):
                self.close()
                self.log('Stop Loss, %.2f' % self.dataclose[0])
        

if __name__ == '__main__':
    cerebo = bt.Cerebro()
    #cerebo.addstrategy(Highest_high)
    cerebo.optstrategy(
        Highest_high,
        highest = range(5,9),
        in_amount = range(1,5),
        stoploss = np.arange(0.1, 0.5, 0.1),
        takeprofit = np.arange(0.1, 0.5, 0.1)
        )
    data = bt.feeds.PandasData(dataname = yf.download('2317.TW','2014-01-01','2020-12-31'))
    cerebo.adddata(data)
    cerebo.broker.setcash(1000000.0)
    cerebo.addsizer(bt.sizers.SizerFix, stake=1000)
    cerebo.broker.setcommission(commission=0.0015)
    #print('Starting Portfolio Value: %.2f' % cerebo.broker.getvalue())
    # cerebo.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')
    cerebo.addanalyzer(bt.analyzers.SharpeRatio)
    cerebo.addanalyzer(bt.analyzers.Returns)
    cerebo.addanalyzer(bt.analyzers.DrawDown)
    results = cerebo.run(maxcpus=1)
    #print('Final Portflio Value: %.2f' % cerebo.broker.getvalue())
    #cerebo.plot(style = 'candlestick', barup = 'red', bardown = 'green')
    par1, par2, par3, par4, ret, down, sharpe_r = [], [], [], [], [], [], []
    for strat in results:
        strat = strat[0]
        a_return = strat.analyzers.returns.get_analysis()
        drawDown = strat.analyzers.drawdown.get_analysis()
        sharpe = strat.analyzers.sharperatio.get_analysis()
        par1.append(strat.params.highest)
        par2.append(strat.params.in_amount)
        par3.append(strat.params.stoploss)
        par4.append(strat.params.takeprofit)
        ret.append(a_return['rtot'])
        down.append(drawDown['max']['drawdown'])
        sharpe_r.append(sharpe['sharperatio'])
    result_df = pd.DataFrame()
    result_df['Hightest'] = par1
    result_df['in_amount'] = par2
    result_df['stoploss'] = par3
    result_df['takeprofit'] = par4
    result_df['total profit'] = ret
    result_df['Max Drawdown'] = down
    result_df['Sharpe Ratio'] = sharpe_r
    result_df = result_df.sort_values(by = ['total profit'], ascending=False)
    print(result_df)
    #strat = results[0]
    #pyfoliozer = strat.analyzers.getbyname('pyfolio')
    #returns, positions, transactions, gross_lev = pyfoliozer.get_pf_items()
    
    #import pyfolio as pf
    #pf.create_full_tear_sheet(returns, positions=positions, transactions=transactions, live_start_date='2018-01-01')



    #%%