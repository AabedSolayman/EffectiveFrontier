import sys  
import math

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

    for i in range(nr_of_coins):
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

    for i in range(nr_of_coins): 
        mean[i]             =   np.mean( return_percentages[i] )
        variance[i]         =   np.var ( return_percentages[i] )
        std_deviation[i]    =   np.std ( return_percentages[i] )
    
    correlation = np.corrcoef(return_percentages[0],
                               return_percentages[1])[0][1]

    return mean, variance, std_deviation, correlation



"""
calc_porftolio_return: calculates the portfolio expected return.
portfolio_return:
"""
def calc_porftolio_return(mean, ratio):
    portfolio_return = np.sum(mean * ratio) / 100
    return portfolio_return
    
    
    
"""
calc_porftolio_volatility: calculates the portfolio volatility using standart deviation.
portfolio_volatility:
"""
def calc_porftolio_volatility(std_dev, ratio, correl):
    portfolio_volatility = math.sqrt(np.sum((std_dev*ratio)**2) + 
                                     np.sum(2 * std_dev * ratio* correl )) / 100
    return portfolio_volatility
    



if __name__ == "__main__":
    coins_prices_matrix = np.array([0,0], dtype=object)        
    
    global nr_of_coins      #number of different coins or stocks in a portfolio
    nr_of_coins = len(sys.argv)-1
    
    for i in range(nr_of_coins):
        coins_prices_matrix[i] = read_data(sys.argv[i+1])

    return_percentages  = calc_history_retrun(coins_prices_matrix)
    mean, variance, std_deviation, correlation = calc_mean_variance_stddev(
                                                            return_percentages)
    
    portfolio_return       = []
    portfolio_volatilities = []
    weight_array           = []
    

# For several stocks/coins
    for i in range(0,10000):
        weights = np.random.rand(nr_of_coins)
        random_sum   = np.sum(weights)
        weights = weights / random_sum
        weight_array.append(weights)
        

        temp = calc_porftolio_return(mean,weights)
        portfolio_return.append(temp)
        temp = calc_porftolio_volatility(std_deviation, weights *100, correlation)
        portfolio_volatilities.append(temp)
        
    sharpe_ratio = np.array(portfolio_return) / np.array(portfolio_volatilities)
    max_sharp_value = sharpe_ratio.argmax()
    max_sharpe_ratio = weight_array[max_sharp_value]

    print("MAXIMUM SHARPE RATIO AT:" + str(max_sharpe_ratio*100))
        
    plt.plot(portfolio_volatilities,portfolio_return,'ro')
    plt.plot(portfolio_volatilities[max_sharp_value],portfolio_return[max_sharp_value],'bo')

    plt.show()

