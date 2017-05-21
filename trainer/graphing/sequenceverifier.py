import pandas as pd
from helpers import Visualizer
from helpers import DataAnalyzer

#dataFile = pd.read_csv("../../data/testing-leftright-qsMbpdsd6zQTqlrKAADi-1-72BPM.csv", header=0)
#dataFile = pd.read_csv("../../data/training-rotateclockwise-avkfxrmpauHdDpeaAAAa-6.csv", header=0)
#dataFile = pd.read_csv("../../data/training-updown-avkfxrmpauHdDpeaAAAa-1.csv", header=0)
#normal data

PERIODS = 5
STARTING_PERIOD = 2
DATAFILE = "../data/training-square-ZirZIvZtcyHkJHlJAAEM-2.csv"

SAVE_LOCATION = "../data/trainsequences/"

#------------------------------------ 

dataFile = pd.read_csv(DATAFILE, header=0)
da = DataAnalyzer.DataAnalyzer()

dataFile = da.normalize(dataFile)
#dataFile = da.autoCorrelate(dataFile)
#FOR REPORT, UNCOMMENT AUTOCORRELATE AND SEE WHAT AUTOCORRELATE DOES!

#FFT:
'''
streamer = DataAnalyzer.StreamDataAnalyzer(dataFile['accZ'])
fft = streamer.getFFTData()
v = Visualizer.Visualizer(dataFile)
v.visualizeFFT(fft['fft'], fft['positive_freqs'])
'''



daa = DataAnalyzer.AutoAnalyzer(dataFile)

bpm, preferredStream = daa.getBPM()
print("BPM: ", bpm, ", Stream: ", preferredStream)

output = daa.getLastPeakTime(visualize=False, periods=PERIODS, startingPeriod=STARTING_PERIOD)
peakIndex = output['index']
endPeriodIndex = output['endPeriodIndex']
print("start: ", str(peakIndex), ", end: ", str(endPeriodIndex))



v = Visualizer.Visualizer(dataFile[peakIndex:endPeriodIndex])
v.visualizeAllAcc()
#v.visualizeSequence(dataFile[peakIndex:endPeriodIndex])

'''
graphData = daa.getPeriodsFromDataIndex(PERIODS, peakIndex)['data']
print("Startindex: ", peakIndex)
#graphData = daa.getPeriods(2, startIndexPeriod=2)['data']
v.visualizeSequence(graphData)
'''

def saveToFile(data):
  pd.to_csv(SAVE_LOCATION + data + ".csv") #no idea about this yet