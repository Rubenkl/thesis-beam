import DataAnalyzer
import pandas as pd
import matplotlib.pyplot as plt
import Visualizer
import numpy as np
import itertools



dataFile = pd.read_csv("../../data/testing-leftright-qsMbpdsd6zQTqlrKAADi-1-72BPM.csv", header=0)
dataFile2 = pd.read_csv("../../data/training-leftright-avkfxrmpauHdDpeaAAAa-3.csv", header=0)
dataFile3 = pd.read_csv("../../data/training-updown-avkfxrmpauHdDpeaAAAa-1.csv", header=0)
dataFile4 = pd.read_csv("../../data/training-rotateclockwise-avkfxrmpauHdDpeaAAAa-6.csv", header=0)

analyzer = DataAnalyzer.DataAnalyzer()

'''
data = dataFile['gamma'].values

analyzer = DataAnalyzer.StreamDataAnalyzer(data)

output = analyzer.getPeriodInfo()
print(output['detectedBPM'])
fft = analyzer.getFFTData()
visualizer = Visualizer.Visualizer(dataFile)
visualizer.visualizeFFT(fft['fft'], fft['positive_freqs'], title='FFT Normal Data')


analyzer2 = DataAnalyzer.StreamDataAnalyzer(analyzer.getAutocorrelation())
fft2 = analyzer2.getFFTData()
visualizer.visualizeFFT(fft2['fft'], fft2['positive_freqs'], title='FFT Autocorrelated Data')


output2 = analyzer.getFFTDataFromStream(analyzer.getAutocorrelation())

print(output['detectedBPM'])

'''
#dataFile2 = analyzer.normalize(dataFile2)
#dataFile3 = analyzer.normalize(dataFile3)
#dataFile4 = analyzer.normalize(dataFile4)



#print("smallest:\t", analyzer.DTWSimilarity(dataFile, dataFile2))
#print("medium:\t\t", analyzer.DTWSimilarity(dataFile2, dataFile3))
#print("large:\t\t", analyzer.DTWSimilarity(dataFile2, dataFile4))

#print(analyzer.autoCorrelate(dataFile2))


training_data = [12,4,51,21,8]


dataFile = analyzer.normalize(dataFile)
training_matrix = []


for i,data in enumerate(training_data):
  row = []
  for j, secondData in enumerate(training_data):
    if (i==j):
      row.append(0)
    else:
      row.append(data * secondData)
  training_matrix.append(row)

print(training_matrix)


#second

test_matrix = np.zeros((len(training_data),len(training_data)))

for n in itertools.combinations(np.arange(len(training_data)), 2):

  test_matrix[n[0], n[1]] = training_data[n[0]] * training_data[n[1]]
  test_matrix[n[1], n[0]] = training_data[n[0]] * training_data[n[1]]

print(test_matrix)

print(training_matrix == test_matrix)

