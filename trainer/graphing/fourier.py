import docopt
import sklearn
import numpy as np
import pandas as pd
from scipy.spatial.distance import euclidean
#import matplotlib.pylab as plt
import matplotlib.pyplot as plt
import math #for math.ceil

from scipy import fftpack


def estimated_autocorrelation(x):
    n = len(x)
    variance = x.var()
    x = x-x.mean()
    r = np.correlate(x, x, mode = 'full')[-n:]
    #assert N.allclose(r, N.array([(x[:n-k]*x[-(n-k):]).sum() for k in range(n)]))
    result = r/(variance*(np.arange(n, 0, -1)))
    return result


#original_headers = list(dataFile.columns.values)

#dataFile = pd.read_csv("../data/training-updown-avkfxrmpauHdDpeaAAAa-1.csv", header=0)
dataFile = pd.read_csv("../data/testing-leftright-qsMbpdsd6zQTqlrKAADi-1-72BPM.csv", header=0)
data = dataFile['gamma'].values
dataCorrelated = estimated_autocorrelation(data)

time = np.linspace(0,10, data.shape[0])

N = dataFile.shape[0]

# from: https://raw.githubusercontent.com/markdregan/K-Nearest-Neighbors-with-Dynamic-Time-Warping/master/K_Nearest_Neighbor_Dynamic_Time_Warping.ipynb


fig = plt.figure(1, figsize=(12,4))
_ = plt.plot(time, data, label='Raw')
_ = plt.plot(time, dataCorrelated, label='Autocorrelated')
_ = plt.title('Data and correlated data')
_ = plt.ylabel('Amplitude')
_ = plt.xlabel('Time')
_ = plt.legend()




#fourier transformation below:

Fs=1000 / 50 # equals 20hz
T = 1.0 / 50.0

X = fftpack.fft(data)
freqs = fftpack.fftfreq(len(data)) * Fs
positive_freqs = freqs[np.where(freqs >= 0)]
magnitudes = X[np.where(freqs > 0)]
peakIndex = np.argmax(magnitudes)
BPM = positive_freqs[peakIndex] * 60

print("[Data] Peak: %s Hz, BPM: %s" % (positive_freqs[peakIndex], BPM))

fig, ax = plt.subplots()



ax.stem(positive_freqs, np.abs(X[:positive_freqs.size])) # was: X[:N//2]
ax.set_xlabel('Frequency in Hertz [Hz]')
ax.set_ylabel('Frequency Domain (Spectrum) Magnitude')
ax.set_xlim(0, Fs / 2)


'''
class data:
  def __init__(self):

'''


# Second stuff for the correlated data:

#fourier transformation below:

Fs=1000 / 50 # equals 20hz
T = 1.0 / 50.0

XC = fftpack.fft(dataCorrelated)
freqsC = fftpack.fftfreq(len(dataCorrelated)) * Fs
positive_freqsC = freqsC[np.where(freqsC >= 0)]
magnitudesC = XC[np.where(freqsC > 0)]
peakIndexC = np.argmax(magnitudesC)
BPMC = positive_freqsC[peakIndexC] * 60

print("[Correlated] Peak: %s Hz, BPM: %s" % (positive_freqsC[peakIndexC], BPMC))

'''
fig, ax = plt.subplots()

ax.stem(positive_freqs, np.abs(X[:N//2]))
ax.set_xlabel('Frequency in Hertz [Hz]')
ax.set_ylabel('Frequency Domain (Spectrum) Magnitude')
ax.set_xlim(0, Fs / 2)
ax.set_ylim(0, 110)

plt.show()
'''

# Graphing a whole period:

detectedFreq = positive_freqs[peakIndex]
samplingRate = 20

dataPointsLength = int(samplingRate / detectedFreq)

time = np.linspace(0,(1/detectedFreq)*4, dataPointsLength*4) # 4 times a period (dataPointsLength)
dataPointsCorrelated = dataCorrelated[0:dataPointsLength*4] # same
dataPoints = data[0:dataPointsLength*4] # same



fig = plt.figure(3, figsize=(12,4))

_ = plt.subplot(211)
_ = plt.plot(time, dataPoints)
_ = plt.title('Raw')
_ = plt.ylabel('Amplitude')
_ = plt.xlabel('Time')
#new additions for second subplot:
_ = plt.subplot(212)
_ = plt.plot(time, dataPointsCorrelated)
_ = plt.title('Correlated')
_ = plt.ylabel('Amplitude')
_ = plt.xlabel('Time')



fig.tight_layout() # tight layout to prevent overlapping of axis labels
plt.show()