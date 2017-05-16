from helpers import DataAnalyzer
import pandas as pd
import matplotlib.pyplot as plt
import Visualizer
import numpy as np
import itertools
import scipy.stats as stats
from sklearn.preprocessing import normalize as skNorm
from scipy import signal

samplingRate = 1000/50

dataFile = pd.read_csv("../../data/good-backup-10seconds/testing-leftright-JUxdyRarf6RVZv0WAABN-7.csv", header=0)
#dataFile2 = pd.read_csv("../../data/training-leftright-avkfxrmpauHdDpeaAAAa-3.csv", header=0)


dataAlpha = dataFile['alpha'].values
dataBeta = dataFile['beta'].values
dataGamma = dataFile['gamma'].values

analyzer = DataAnalyzer.AutoAnalyzer(dataFile)
visualizer = Visualizer.Visualizer(dataFile)


res = analyzer.getLastPeakTime(visualize=True)

print(res['time'])
print(res['bpm'])



'''

length = int(samplingRate / (bpm[0]/60))
startIndex = length * 2  # <-- Start extracting the peak from the 2nd period
rates = np.array([70,80,90,100,110,120,130,140])/60 #BPMs to test

piece = dataFile['accZ'][startIndex: startIndex+length*2]

peak = signal.find_peaks_cwt(piece, samplingRate/rates/2)
print(peak)

'''
#visualizer.visualizeStream(piece, vLine=peak[0])
#continue next time with this

''''
streams = ['accX', 'accY', 'accZ', 'alpha', 'beta', 'gamma']
for stream in streams:
  print(dataFile[stream][1:4])

'''

'''
print(analyzer.getBPM(autocorrelated=True, printAll=True))
print(analyzer.getBPM(autocorrelated=False, printAll=True))
'''



'''
dataRaw = []
dataRaw.extend(dataFile['accX'].values)
dataRaw.extend(dataFile['accY'].values)
dataRaw.extend(dataFile['accZ'].values)

currIter = 0
dataX = dataRaw[:len(dataFile['accX'].values)]
currIter = len(dataFile['accX'].values);
dataY = dataRaw[currIter:currIter + len(dataFile['accY'].values)]
currIter += len(dataFile['accY'].values)
dataZ = dataRaw[currIter:currIter + len(dataFile['accZ'].values)]

#tests:
print(dataFile['accX'].values == dataX)
print(dataFile['accY'].values == dataY)
print(dataFile['accZ'].values == dataZ)
'''


'''

normalizeAlpha = skNorm([dataFile['beta']])[0]
out = analyzer.normalize(dataFile)

visualizer.visualizeStream(normalizeAlpha)
visualizer.visualizeStream(out['alpha'])

'''

'''
output = analyzer.getPeriodInfo()
print('Normal: ', output['detectedBPM'])
fft = analyzer.getFFTData()
X = np.abs(fft['fft'][:fft['positive_freqs'].size])
print(stats.normaltest(X))
visualizer = Visualizer.Visualizer(dataFile)
visualizer.visualizeStream(dataAlpha)
visualizer.visualizeFFT(fft['fft'], fft['positive_freqs'], title='FFT Normal Data')




analyzer2 = DataAnalyzer.StreamDataAnalyzer(analyzer.getAutocorrelation())
output2 = analyzer2.getPeriodInfo()
print('Autocorrelated: ', output2['detectedBPM'])

fft2 = analyzer2.getFFTData()
X = np.abs(fft2['fft'][:fft2['positive_freqs'].size])
print(stats.normaltest(X))
visualizer.visualizeFFT(fft2['fft'], fft2['positive_freqs'], title='FFT Autocorrelated Data')

'''



'''

#-----------------------
#detecting normality of FFT data:
analyzer = DataAnalyzer.StreamDataAnalyzer(dataAlpha)
fft = analyzer.getFFTData()
visualizer.visualizeFFT(fft['fft'], fft['positive_freqs'], title='FFT Normal Data')
X = np.abs(fft['fft'][:fft['positive_freqs'].size])
stats.normaltest(X)
visualizer.visualizeStream(X)
#-----------------------------



'''