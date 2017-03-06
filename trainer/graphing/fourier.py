import docopt
import sklearn
import numpy as np
import pandas as pd
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean
import matplotlib.pylab as plt

from scipy import fftpack










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

dataFileQuick = pd.read_csv("../data/training-updown-mg8f0Om0lSmaYI9AAAP-1-QUICK.csv", header=0)
dataQuick = dataFileD['beta'].values

fdataD = fftpack.fft(dataA)

distance, path = fastdtw(dataA, dataQuick)

print(distance)


# from: https://raw.githubusercontent.com/markdregan/K-Nearest-Neighbors-with-Dynamic-Time-Warping/master/K_Nearest_Neighbor_Dynamic_Time_Warping.ipynb


fig = plt.figure(figsize=(12,4))
_ = plt.plot(time, dataA, label='A')
_ = plt.plot(time, dataQuick, label='Quick')
_ = plt.title('DTW distance between A and Quick is %.2f' % distance)
_ = plt.ylabel('Amplitude')
_ = plt.xlabel('Time')
_ = plt.legend()
plt.show()


# 1 second divided by 50ms to get the measures per second
Fs=1000 / 50.


T = 1.0 / 50.0

#xf = np.linspace(0.0, 1.0/(2.0*T), N/2)


#fig, ax = plt.subplots()
#ax.plot(xf, 2.0/N * np.abs(fdataD[:N//2]))
#plt.show()


X = fftpack.fft(dataQuick)
freqs = fftpack.fftfreq(len(dataQuick)) * Fs
positive_freqs = freqs[np.where(freqs >= 0)]
magnitudes = abs(X[np.where(freqs >= 0)])
peak = np.argmax(magnitudes)
print(peak)

fig, ax = plt.subplots()

print(np.argmax(X[np.where(freqs>=0)]))

indices = np.where(X == X.max())
print(indices)

ax.stem(positive_freqs, np.abs(X[:N//2]))
ax.set_xlabel('Frequency in Hertz [Hz]')
ax.set_ylabel('Frequency Domain (Spectrum) Magnitude')
ax.set_xlim(0, Fs / 2)
ax.set_ylim(0, 510)

plt.show()

'''
class data:
  def __init__(self):

'''