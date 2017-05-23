import pandas as pd
from helpers import Visualizer
from helpers import DataAnalyzer

import matplotlib.pyplot as plt
import numpy as np


from sklearn.preprocessing import normalize as skNorm


#dataFile = pd.read_csv("../../data/testing-leftright-qsMbpdsd6zQTqlrKAADi-1-72BPM.csv", header=0)
#dataFile = pd.read_csv("../../data/training-rotateclockwise-avkfxrmpauHdDpeaAAAa-6.csv", header=0)
#dataFile = pd.read_csv("../../data/training-updown-avkfxrmpauHdDpeaAAAa-1.csv", header=0)
#normal data

dataFile = pd.read_csv("../data/training-leftright-pausing-3.csv", header=0)
da = DataAnalyzer.DataAnalyzer()


#Normalize each stream individually:
'''
dataNorm = dataFile.copy()
dataNorm['accX'] = skNorm(dataNorm['accX'])[0]
dataNorm['accY'] = skNorm(dataNorm['accY'])[0]
dataNorm['accZ'] = skNorm(dataNorm['accZ'])[0]
'''



dataFile = da.normalize(dataFile)
dataFile = da.autoCorrelate(dataFile)



daa = DataAnalyzer.AutoAnalyzer(dataFile)

visualizer = Visualizer.Visualizer(dataFile)
#visualizer = Visualizer.Visualizer(dataFile[90:120])

'''
time = np.linspace(0,dataFile[10:110].shape[0], dataFile[10:110].shape[0])
fig = plt.figure(figsize=(12,4))
_ = plt.plot(time, dataFile[10:110]['accZ'], label='Normalized')
_ = plt.plot(time, dataFileCorrelated[10:110]['accZ'], label='Autocorrelated')
#_ = plt.title('DTW distance betw')
_ = plt.ylabel('Amplitude')
_ = plt.xlabel('Time')
_ = plt.legend()
plt.show()

'''


#visualizer.visualizeStream(dataFile[10:110]['accX'])
visualizer.visualizeAllAcc(correlated=False)
