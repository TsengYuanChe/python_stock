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

class MACD_Sta(bt.Strategy):
    params = (
        ('period_me1', 12),
        ('period_me2', 26),
        ('period_signal', 9),
        ('period_sma1', 5),
        ('period_sma2', 20),
        ('period_sma3', 60),
        ('stoploss', 0.3),
        ('takeprofit', 0.1),
    )
    def __init__(self):
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.dataclose = self.datas[0].close
        self.datahigh = self.datas[0].high
        self.dataopen = self.datas[0].open
        self.histogram = bt.ind.MACDHisto(period_me1 = 12, period_me2 = 26, period_signal = 9)
        self.histo = self.histogram.histo
        self.sma1 = bt.indicators.SimpleMovingAverage(self.datas[0].close, period = self.params.period_sma1)
        self.sma2 = bt.indicators.SimpleMovingAverage(self.datas[0].close, period = self.params.period_sma2)
        self.sma3 = bt.indicators.SimpleMovingAverage(self.datas[0].close, period = self.params.period_sma3)

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:
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
        if self.order:
            return
        
        if self.position.size == 0:
            buy_condition1 = self.sma1[0]>self.sma1[-1] and self.sma2[0]>self.sma2[-1] and self.sma3[0]>self.sma3[-1]
            buy_condition2 = self.histo[-2] < 0 and self.histo[-1] < 0 and self.histo[0] >= 0
            if buy_condition1 and buy_condition2:
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.order = self.buy()
        else:
            sell_condition1 = self.datahigh[0] < self.datahigh[-1] and self.datahigh[-1] > self.datahigh[-2] and self.datahigh[-2] > self.datahigh[-3]
            sell_condition2 = self.dataopen[0] > self.dataclose[0] and self.dataclose[-1] > self.dataopen[-1] and self.dataclose[-2] > self.dataclose[-2]
            sell_condition3 = self.dataclose[0] > self.position.price*(1+self.params.takeprofit)
            sell_condition4 = self.dataclose[0] < self.position.price*(1-self.params.stoploss)
            if (sell_condition1 and sell_condition2 and sell_condition3):
                self.log('SELL Profit, %.2f' % self.dataclose[0])
                self.order = self.close()
            elif sell_condition4:
                self.log('SELL Profit, %.2f' % self.dataclose[0])
                self.order = self.close()