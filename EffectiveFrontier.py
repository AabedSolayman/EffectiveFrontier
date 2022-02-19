import sys
import math

import yfinance as yf  
import requests


import numpy as np
import matplotlib.pyplot as plt

"""
read_data: reads data from files and returns the data.
file_name: list of file names. must be greater than 2
"""
def read_data(file_name_list):
    closed_price = np.genfromtxt(file_name_list, delimiter=',')[1:,4]
    return closed_price


"""
calc_history_retrun: calculates expected return.
coins_prices: np array of the prices of a stock or 
a cryptocoin usually at closed price.
"""
def calc_history_retrun(coins_prices):
    #coins_prices_incremented is an np array that contains 
    # the coin prices but starts from index 1 instead of 0.
    coins_prices_incremented = np.empty_like(coins_prices)
    return_percentage        = np.empty_like(coins_prices)

    for i in range(nr_of_assets):
        coins_prices_incremented[i]     = coins_prices[i][1:]
        return_percentage[i]            = coins_prices_incremented[i]/coins_prices[i][:-1]-1 
      
    return return_percentage


"""
calc_mean_variance_stddev: calculates mean, variance,
standard deviation and correlation .
return_percentage: np array of the prices of a stock or
a cryptocoin usually at closed price.
"""
def calc_mean_variance_stddev(return_percentage):
    mean           =   np.empty_like(return_percentage)
    variance       =   np.empty_like(return_percentage)
    std_deviation  =   np.empty_like(return_percentage)

    for i in range(nr_of_assets): 
        mean[i]             =   np.mean( return_percentages[i] )
        variance[i]         =   np.var ( return_percentages[i] )
        std_deviation[i]    =   np.std ( return_percentages[i] )
    
    correlation = np.cov(return_percentages[0],
                               return_percentages[1])


    return mean, variance, std_deviation, correlation



"""
calc_porftolio_return: calculates the portfolio expected return.
portfolio_return:
"""
def calc_porftolio_return(mean, ratio):
    portfolio_return = np.sum(mean * ratio)
    portfolio_return = (1+portfolio_return)**250 - 1
    return (portfolio_return)
    
    
    
"""
calc_porftolio_volatility: calculates the portfolio volatility using standart deviation.
portfolio_volatility:
"""
def calc_porftolio_volatility(std_dev, ratio, correl):
        
    portfolio_volatility = math.sqrt(np.sum((std_dev*ratio)**2) + 2 * np.prod( std_dev * ratio ) * correl[0][1])
    # portfolio_volatility = np.sqrt(12) * portfolio_volatility
    portfolio_volatility = np.sqrt(250) * portfolio_volatility

    return portfolio_volatility


def fetch_data_crypto(coin_pair, frequency, days ):
    
    base_url = "https://poloniex.com/"
            #sec  min  hour days
    days_delta = 60 * 60 * 24 * days
    now_is = int(time())    
    start_At = now_is - days_delta
    price_url = f"public?command=returnChartData&currencyPair={coin_pair}&start={start_At}&end={now_is}&period={frequency}"
    price_list = []
    prices      = requests.get(base_url+price_url).json()

#    for item in prices:
    for i in range(0,np.shape(prices)[0], 1):
        price_list.append(prices[i]['close'])
    
    return np.array(price_list)


def fetch_data_stocks(stock_name,years):
    y = str(years) + 'y'
    data = yf.download(stock_name, period = y,interval="1d")
    
    # data = yf.download(stock_name,start="2012-01-01",end="2022-01-01",interval="1mo")

    prices = np.array(data.loc[:,"Close"])

    prices = prices[~np.isnan(prices)]

    return prices




if __name__ == "__main__":
    
    global nr_of_assets      #number of different coins or stocks in a portfolio
    nr_of_assets = len(sys.argv)-1
    risk_free   = 0.00       # value in % that should be subtracted from the risk
    
    
    coins_prices_matrix = np.array([0] * nr_of_assets, dtype=object)        


    frequency = "86400" #1Day
    days = 2382 #period
       
    for i in range(nr_of_assets):
        #coins_prices_matrix[i] = fetch_data_crypto(sys.argv[i+1],frequency,days)
        coins_prices_matrix [i] = fetch_data_stocks(stock_name = sys.argv[i+1],years = 10)
        #coins_prices_matrix[i] = read_data(sys.argv[i+1])
        
    return_percentages  = calc_history_retrun(coins_prices_matrix)

    mean, variance, std_deviation, correlation = calc_mean_variance_stddev(
                                                            return_percentages)
        
    portfolio_return       = []
    portfolio_volatilities = []
    weight_array           = []
    
    max_iterations = 100000


# For several stocks/coins
    for i in range(0,max_iterations):
        weights      = np.random.rand(nr_of_assets)
        random_sum   = np.sum(weights)
        weights      = np.round((weights / random_sum),3)
        weight_array.append(weights)
        
        temp = calc_porftolio_return(mean,weights)
        portfolio_return.append(temp*100)
        temp = calc_porftolio_volatility(std_deviation, weights, correlation)
        portfolio_volatilities.append(temp*100)
    
    sharpe_ratio = (np.array(portfolio_return) - risk_free)/ np.array(portfolio_volatilities)
    max_sharp_value = sharpe_ratio.argmax()
    max_sharpe_ratio = weight_array[max_sharp_value]
    max_sharp_volatility = portfolio_volatilities[max_sharp_value]
    max_sharp_return     = portfolio_return[max_sharp_value]
    

    for i in range(len(max_sharpe_ratio)):
        print(sys.argv[i+1]+ ":" + "%.2f" % round(max_sharpe_ratio[i]*100, 2)  + "%")
  #"%.2f" % round(max_sharpe_ratio[i]*100, 2)
    
    #plot volatiliy, return, and sharp ratio
    plt.figure(figsize=(9,12))
    plt.scatter(portfolio_volatilities,portfolio_return,c=sharpe_ratio,cmap='plasma')
    plt.colorbar(label='Sharpe Ratio')
    plt.xlabel('Volatility')
    plt.ylabel('Return')# Add red dot for max sharp ratio
    plt.scatter(max_sharp_volatility,max_sharp_return,c='red',s=50,edgecolors='black')
    plt.tight_layout()
    plt.show()





"""
    print(return_percentages)
    return_percentages[1][1] = 0.07
    return_percentages[1][6] = 0.05
    return_percentages[1][7] = 0.05
    return_percentages[1][8] = 0.12
"""