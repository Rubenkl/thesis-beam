import docopt
import sklearn
import numpy as np
import pandas as pd
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean
import matplotlib.pylab as plt

import scipy.fftpack










#original_headers = list(dataFile.columns.values)
N = 198

time = np.linspace(0,20, 198)

dataFile = pd.read_csv("../data/training-updown-RbWE5pRKUdnyeTTAAAI-1.csv", header =0)
dataA = dataFile['beta'].values

dataFileB = pd.read_csv("../data/training-updown-RbWE5pRKUdnyeTTAAAI-2.csv", header=0)
dataB = dataFileB['beta'].values

dataFileC = pd.read_csv("../data/training-leftright-RbWE5pRKUdnyeTTAAAI-3.csv", header=0)
dataC = dataFileC['beta'].values

dataFileD = pd.read_csv("../data/training-updown-RbWE5pRKUdnyeTTAAAI-7.csv", header=0)
dataD = dataFileD['beta'].values

fdataD = scipy.fftpack.fft(dataA)

distance, path = fastdtw(dataA, dataD)

print(distance)


# from: https://raw.githubusercontent.com/markdregan/K-Nearest-Neighbors-with-Dynamic-Time-Warping/master/K_Nearest_Neighbor_Dynamic_Time_Warping.ipynb

'''
fig = plt.figure(figsize=(12,4))
_ = plt.plot(time, dataA, label='A')
_ = plt.plot(time, dataD, label='D')
_ = plt.title('DTW distance between A and C is %.2f' % distance)
_ = plt.ylabel('Amplitude')
_ = plt.xlabel('Time')
_ = plt.legend()
plt.show()
'''

# 1 second divided by 50ms to get the measures per second
Fs=1000 / 50.
t = [i*1./Fs for i in range(198)]

fourier = scipy.fftpack.fft(dataD)
frequencies = scipy.fftpack.fftfreq(len(dataD)) * Fs  
positive_frequencies = frequencies[np.where(frequencies > 0)]  
magnitudes = abs(fourier[np.where(frequencies > 0)])  # magnitude spectrum

peak_frequency = np.argmax(magnitudes)
print(peak_frequency)


T = 1.0 / 50.0

#xf = np.linspace(0.0, 1.0/(2.0*T), N/2)
xf = np.linspace(0, 2, 99, endpoint=False)


fig, ax = plt.subplots()
ax.plot(xf, 2.0/N * np.abs(fdataD[:N//2]))
plt.show()





'''
class data:
  def __init__(self):

'''