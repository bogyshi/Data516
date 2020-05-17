import pandas as pd
import numpy as np

def sigmoid(x):
    '''
    returns the sigmoid transformation of the inputData

    >>>sigmoid(0)
    0.5
    >>>sigmoid(100)<0.1
    '''
    return 1/(1+np.exp(-x))

if __name__ == "__main__":
    import doctest
    doctest.testmod()
