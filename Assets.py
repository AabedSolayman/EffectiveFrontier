
from time import time

import numpy as np

import requests
import yfinance as yf  



class Assets():

    def __init__(self,nr_of_assets,nr_interval_in_year):
        self.nr_of_assets = nr_of_assets
        self.nr_interval_in_year = nr_interval_in_year


    def fetch_asset(self, asset_name, interval, years):
        raise NotImplementedError() #virtual function


    def calc_annual_portfolio_return(self, portfolio_return):
        temp =  (np.array(portfolio_return)+1)**self.nr_interval_in_year - 1
        print(temp[0])
        return temp

    def calc_annual_volatility_return(self, portfolio_return):
        return np.sqrt(self.nr_interval_in_year) * np.array(portfolio_return)


class Stocks(Assets):

    def __init__(self,nr_of_assets):
        self.nr_interval_in_year = 12
        super().__init__(nr_of_assets,self.nr_interval_in_year)

    def fetch_asset(self, asset_name, interval = "1mo" , period = 10):
        y = str(period) + 'y'
        
        data = yf.download(asset_name, period = y, interval=interval)
        
        prices = np.array(data.loc[:,"Close"])

        prices = prices[~np.isnan(prices)]

        return prices


class Crypto(Assets):

    def __init__(self,nr_of_assets):
        self.nr_interval_in_year = 365
        super().__init__(nr_of_assets,self.nr_interval_in_year)


    def fetch_asset(self,asset_name, interval = "86400", days = 2380 ): #interval = 1d
        base_url = "https://poloniex.com/"
                #sec  min  hour days
        days_delta = 60 * 60 * 24 * days
        now_is = int(time())    
        start_At = now_is - days_delta
        price_url = f"public?command=returnChartData&currencyPair={asset_name}&start={start_At}&end={now_is}&period={interval}"
        price_list = []
        prices      = requests.get(base_url+price_url).json()

        for i in range(0,np.shape(prices)[0], 1):
            price_list.append(prices[i]['close'])
    
        return np.array(price_list)
