import numpy as np 
import pandas as pd 

def sortSecond(val): 
    return val[1] 

def predict(fit, predictX): #dataframe with numerical and sorted index and 1d array as input
    res = fit['difficulty']
    df1 = fit.drop('difficulty', axis = 1)
    dist = []
    k = 5
    index = 0
    for item in df1.values:
        d1 = (item[0]-predictX[0])**2
        d2 = (item[1]-predictX[1])**2
        d3 = (item[2]-predictX[2])**2
        d4 = (item[3]-predictX[3])**2
        d5 = (item[4]-predictX[4])**2
        dist1 = np.sqrt([d1+d2+d3+d4+d5])
        dist.append([index, dist1[0]])
        index = index + 1
    dist.sort(key=sortSecond)
    nearestNeighborsIndex = [x[0] for x in dist[0:5]]
    res = res.iloc[nearestNeighborsIndex]
    difficulty = 0
    for item in res.values:
        difficulty = difficulty + item**3
    difficulty = np.cbrt([difficulty/k])[0]
    return round(difficulty)