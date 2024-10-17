import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import datetime
import os
import yfinance as yf
import warnings
warnings.filterwarnings('ignore')

def load_market_data(symbol, start_date, end_date):
    data = yf.download(symbol, start=start_date, end=end_date)
    return data #OHLCV

class Backtesting:
    def __init__(self, data, stratergy):
        self.data = data
        self.stratergy = stratergy
        self.portfolio = {'cash': 1000000, 'position': {}}
        self.trades = []
        self.equity = []
    def backtest_update(self):
        risk_per_trade = 0.02 #2% of the total capital
        for index, row in self.data.iterrows():
            close_price = row['Close']
            signal = row['signal'] #buy or sell
            if signal == 'buy': #
                available_cash = self.portfolio['cash']
                position_size = available_cash * risk_per_trade / close_price
                self.execute_trade(symbol=self.data.name, quantity=position_size, price=close_price)
            elif signal == 'sell':
                position_size = self.portfolio['positions'].get(self.data.name, 0)
                if position_size > 0: #long position
                    self.execute_trade(symbol=self.data.name, quantity=-position_size, price=close_price)

