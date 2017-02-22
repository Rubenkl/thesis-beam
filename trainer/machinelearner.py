import docopt
import sklearn
import numpy as np
import pandas as pd
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean

import matplotlib.pylab as plt








#original_headers = list(dataFile.columns.values)

time = np.linspace(0,20, 198)

dataFile = pd.read_csv("data/training-updown-RbWE5pRKUdnyeTTAAAI-1.csv", header =0)
dataA = dataFile['beta'].values

dataFileB = pd.read_csv("data/training-updown-RbWE5pRKUdnyeTTAAAI-2.csv", header=0)
dataB = dataFileB['beta'].values

dataFileC = pd.read_csv("data/training-leftright-RbWE5pRKUdnyeTTAAAI-3.csv", header=0)
dataC = dataFileC['beta'].values

dataFileD = pd.read_csv("data/training-updown-RbWE5pRKUdnyeTTAAAI-7.csv", header=0)
dataD = dataFileD['beta'].values

distance, path = fastdtw(dataA, dataD)

print(distance)


# from: https://raw.githubusercontent.com/markdregan/K-Nearest-Neighbors-with-Dynamic-Time-Warping/master/K_Nearest_Neighbor_Dynamic_Time_Warping.ipynb
fig = plt.figure(figsize=(12,4))
_ = plt.plot(time, dataA, label='A')
_ = plt.plot(time, dataD, label='D')
_ = plt.title('DTW distance between A and C is %.2f' % distance)
_ = plt.ylabel('Amplitude')
_ = plt.xlabel('Time')
_ = plt.legend()
plt.show()

'''
class data:
  def __init__(self):

'''