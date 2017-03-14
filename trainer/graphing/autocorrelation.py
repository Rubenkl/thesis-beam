import docopt
import sklearn
import numpy as np
import pandas as pd
from scipy.spatial.distance import euclidean
import matplotlib.pylab as plt
from sklearn.preprocessing import normalize as skNormalize

from scipy import fftpack #for fourier analysis


#original_headers = list(dataFile.columns.values)
N = 198

time = np.linspace(0,20, 200)
time = time.reshape(1,-1)

#dataFile = pd.read_csv("../data/training-leftright-avkfxrmpauHdDpeaAAAa-3.csv", header=0)
dataFile = pd.read_csv("../data/testing-leftright-qsMbpdsd6zQTqlrKAADi-1-72BPM.csv", header=0)
dataA = dataFile['gamma'].values
dataA = dataA.reshape(1, -1)
dataB = skNormalize(dataA)



def estimated_autocorrelation(x):
    n = len(x)
    variance = x.var()
    x = x-x.mean()
    r = np.correlate(x, x, mode = 'full')[-n:]
    #assert N.allclose(r, N.array([(x[:n-k]*x[-(n-k):]).sum() for k in range(n)]))
    result = r/(variance*(np.arange(n, 0, -1)))
    return result



#plot raw data and autocorrelation:
fig = plt.figure(figsize=(12,4))
_ = plt.plot(time[0], dataA[0], label='A')
_ = plt.plot(time[0], estimated_autocorrelation(dataA[0]), label='Correlated')
_ = plt.title('Datafile A')
_ = plt.ylabel('Amplitude')
_ = plt.xlabel('Time')
_ = plt.legend()
plt.show()



#fourier transformation below:

Fs=1000 / 50 # equals 20hz
T = 1.0 / 50.0

X = fftpack.fft(estimated_autocorrelation(dataA[0]))
freqs = fftpack.fftfreq(len(dataA[0])) * Fs
positive_freqs = freqs[np.where(freqs > 0)]
magnitudes = X[np.where(freqs >= 0)]
peak = np.argmax(magnitudes)

print("Peak: %d" % peak)

fig, ax = plt.subplots()
indices = np.where(X == X.max())

ax.stem(positive_freqs, np.abs(X[:N//2]))
ax.set_xlabel('Frequency in Hertz [Hz]')
ax.set_ylabel('Frequency Domain (Spectrum) Magnitude')
ax.set_xlim(0, Fs / 2)
ax.set_ylim(0, 30)
plt.show()


#from internet, fix the implementation here:

ps = np.abs(np.fft.fft(data))**2

time_step = 1 / 50
freqs = np.fft.fftfreq(data.size, time_step)
idx = np.argsort(freqs)

plt.plot(freqs[idx], ps[idx])