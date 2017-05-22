import pandas as pd
from helpers import Visualizer
from helpers import DataAnalyzer

#dataFile = pd.read_csv("../../data/testing-leftright-qsMbpdsd6zQTqlrKAADi-1-72BPM.csv", header=0)
#dataFile = pd.read_csv("../../data/training-rotateclockwise-avkfxrmpauHdDpeaAAAa-6.csv", header=0)
#dataFile = pd.read_csv("../../data/training-updown-avkfxrmpauHdDpeaAAAa-1.csv", header=0)
#normal data

PERIODS = 4
STARTING_PERIOD = 10
WRITE = True
DATAFILE_NUMBER = 1
DATAFILE = "../data/good-backup-10seconds/training-rotateclockwise-8654johJQMBPknNOAAE3-1.csv"
DATAID = "8654johJQMBPknNOAAE3-1"

SAVE_LOCATION = "../data/trainsequences/"

#------------------------------------ 

dataFile = pd.read_csv(DATAFILE, header=0)
da = DataAnalyzer.DataAnalyzer()

dataFile = da.normalize(dataFile)
dataFile = da.autoCorrelate(dataFile)
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

output = daa.getLastPeakTime(visualize=True, periods=PERIODS, startingPeriod=STARTING_PERIOD)
peakIndex = output['index']
endPeriodIndex = output['endPeriodIndex']
print("start: ", str(peakIndex), ", end: ", str(endPeriodIndex))


#temp this for speeding up gathering datasets:
v = Visualizer.Visualizer(dataFile[peakIndex:endPeriodIndex])
v.visualizeAllAcc()


if WRITE:
  savePath = SAVE_LOCATION +"/"+ dataFile['movement'][1] + "-" + str(peakIndex) + "-" + str(endPeriodIndex) + "-" + DATAID + "_" + str(DATAFILE_NUMBER) + ".csv"
  print(savePath)
  dataFile[peakIndex:endPeriodIndex].to_csv(savePath, sep=',') #no idea about this yet


#v.visualizeSequence(dataFile[peakIndex:endPeriodIndex])

'''
graphData = daa.getPeriodsFromDataIndex(PERIODS, peakIndex)['data']
print("Startindex: ", peakIndex)
#graphData = daa.getPeriods(2, startIndexPeriod=2)['data']
v.visualizeSequence(graphData)
'''

def saveToFile(data):
  data.to_csv(SAVE_LOCATION + data['movement'] + "-" + peakIndex + "-" + endPeriodIndex + "_" + DATAFILE_NUMBER + ".csv") #no idea about this yet