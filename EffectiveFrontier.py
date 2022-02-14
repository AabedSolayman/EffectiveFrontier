import numpy as np
import matplotlib as plt
import copy
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
coins_prices: np array of the prices of a stock or a cryptocoin usually at closed price.
"""
def calc_expected_retrun(coins_prices):
    #coins_prices_incremented is an np array that contains 
    # the coin prices but starts from index 1 instead of 0.
    coins_prices_incremented = np.empty_like(coins_prices)
    return_percentage        = np.empty_like(coins_prices)
    nr_of_coins              = coins_prices.shape[0]

    for i in range(nr_of_coins):
        coins_prices_incremented[i]     = coins_prices[i][1:]
        return_percentage[i]            = coins_prices_incremented[i]/coins_prices[i][:-1]-1 
             
    return return_percentage



if __name__ == "__main__":
    coins_prices_matrix = np.array([0,0], dtype=object)        #TODO: Change the size of coins_prices_matrix to match the number of arguments 
    for i in range(len(sys.argv)-1):
        coins_prices_matrix[i] = read_data(sys.argv[i+1])

    print(coins_prices_matrix)
    calc_expected_retrun(coins_prices_matrix)