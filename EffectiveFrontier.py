import numpy as np
import matplotlib as plt
import math
import sys  






"""
read_data: reads data from files and returns the data.
file_name: list of file names. must be greater than 2
"""
def read_data(file_name_list):
    closed_price = np.genfromtxt(file_name_list, delimiter=',')[1:,4]
    return closed_price

"""
calc_expected_retrun: calculates expected return.
coins_prices: np array of the prices of a stock or 
a cryptocoin usually at closed price.
"""
def calc_expected_retrun(coins_prices):
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

    return_percentages  = calc_expected_retrun(coins_prices_matrix)
    mean, variance, std_deviation, correlation = calc_mean_variance_stddev(
                                                            return_percentages)
    
    for i in range(0,100,10):
        calc_porftolio_return(mean,np.array([i,100-i]))
        calc_porftolio_volatility(std_deviation, np.array([i,100-i]), correlation)  