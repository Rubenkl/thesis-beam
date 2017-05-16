import pandas as pd
from helpers import Visualizer
from helpers import DataAnalyzer

#dataFile = pd.read_csv("../../data/testing-leftright-qsMbpdsd6zQTqlrKAADi-1-72BPM.csv", header=0)
#dataFile = pd.read_csv("../../data/training-rotateclockwise-avkfxrmpauHdDpeaAAAa-6.csv", header=0)
#dataFile = pd.read_csv("../../data/training-updown-avkfxrmpauHdDpeaAAAa-1.csv", header=0)
#normal data

dataFile = pd.read_csv("../data/forvisualize/training-w-WvUVD6yGptP0OmsZAABi-3.csv", header=0)
da = DataAnalyzer.DataAnalyzer()

dataFile = da.normalize(dataFile)
dataFile = da.autoCorrelate(dataFile)

#das = DataAnalyzer.StreamDataAnalyzer(dataFile['accZ']) #<---- PLAY WITH THIS PARAMETER Z, X, Y
#output = das.getFFTData()


daa = DataAnalyzer.AutoAnalyzer(dataFile)

bpm, preferredStream = daa.getBPM()
print("BPM: ", bpm, ", Stream: ", preferredStream)

output = daa.getLastPeakTime(visualize=True, periods=6)
peakTime = output['index']

#graphData = das.getPeriods(4, startIndex=peakTime)[preferredStream]
