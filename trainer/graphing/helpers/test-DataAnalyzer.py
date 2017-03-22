import DataAnalyzer
import pandas as pd
import matplotlib.pyplot as plt
import Visualizer



dataFile = pd.read_csv("../../data/testing-leftright-qsMbpdsd6zQTqlrKAADi-1-72BPM.csv", header=0)
dataFile2 = pd.read_csv("../../data/training-leftright-avkfxrmpauHdDpeaAAAa-3.csv", header=0)
dataFile3 = pd.read_csv("../../data/training-updown-avkfxrmpauHdDpeaAAAa-1.csv", header=0)
dataFile4 = pd.read_csv("../../data/training-rotateclockwise-avkfxrmpauHdDpeaAAAa-6.csv", header=0)

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

analyzer = DataAnalyzer.DataAnalyzer()

dataFile = analyzer.normalize(dataFile)
print(dataFile)
#dataFile2 = analyzer.normalize(dataFile2)
#dataFile3 = analyzer.normalize(dataFile3)
#dataFile4 = analyzer.normalize(dataFile4)



#print("smallest:\t", analyzer.DTWSimilarity(dataFile, dataFile2))
#print("medium:\t\t", analyzer.DTWSimilarity(dataFile2, dataFile3))
#print("large:\t\t", analyzer.DTWSimilarity(dataFile2, dataFile4))

#print(analyzer.autoCorrelate(dataFile2))


