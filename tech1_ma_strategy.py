#%%
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
import yfinance as yf

# Import the backtrader platform
import backtrader as bt
import pandas as pd
import matplotlib.pyplot as plt
# Create a Stratey
class TestStrategy(bt.Strategy):
    params = (
        ('fast_period', 3),
        ('slow_period', 60)
    )

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # Add a MovingAverageSimple indicator
        self.sma1 = bt.indicators.SimpleMovingAverage(
            self.datas[0].close, period=self.params.fast_period)
        self.sma2 = bt.indicators.SimpleMovingAverage(
            self.datas[0].close, period=self.params.slow_period)
        self.crossover = bt.ind.CrossOver(self.sma1, self.sma2)

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
        if not self.position:

            # Not yet ... we MIGHT BUY if ...
            if self.crossover>0:
                print()

                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log('BUY CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()

        else:

            if self.crossover<0:
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('SELL CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()
    def stop(self):
        print(f'Fast MA: {self.params.fast_period} | Slow MA: {self.params.slow_period} | End Value: {self.broker.getvalue()}')
if __name__ == '__main__':
    cerebo = bt.Cerebro()
    cerebo.addstrategy(TestStrategy)
    # strats = cerebo.optstrategy(TestStrategy, fast_period=range(3,7),slow_period=range(40,70,10))
    data = bt.feeds.PandasData(dataname = yf.download('2330.TW','2014-01-01','2020-12-31'))
    cerebo.adddata(data)
    cerebo.broker.setcash(1000000.0)
    cerebo.addsizer(bt.sizers.SizerFix, stake=1000)
    cerebo.broker.setcommission(commission=0.0015)
    print('Starting Portfolio Value: %.2f' % cerebo.broker.getvalue())
    cerebo.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')
    results = cerebo.run(maxcpus=1)
    print('Final Portflio Value: %.2f' % cerebo.broker.getvalue())
    #  cerebo.plot(style = 'candlestick', barup = 'red', bardown = 'green')
    strat = results[0]
    pyfoliozer = strat.analyzers.getbyname('pyfolio')
    returns, positions, transactions, gross_lev = pyfoliozer.get_pf_items()
    
    import pyfolio as pf
    pf.create_full_tear_sheet(returns, positions=positions, transactions=transactions, live_start_date='2018-01-01')



    #%%