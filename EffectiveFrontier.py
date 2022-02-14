import numpy as np
import matplotlib as plt

import sys  

def read_data(file_name):
    closed_price = np.genfromtxt(file_name, delimiter=',')[1:,4]
    return closed_price


if __name__ == "__main__":
    closed_prices = np.array([0,0], dtype=object)
    for i in range(len(sys.argv)-1):
        closed_prices[i] = read_data(sys.argv[i+1])
        print(sys.argv[i+1])

    print(closed_prices)