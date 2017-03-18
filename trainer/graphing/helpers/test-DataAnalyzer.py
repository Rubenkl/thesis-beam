import DataAnalyzer
import pandas as pd
import matplotlib.pyplot as plt


dataFile = pd.read_csv("../../data/testing-leftright-qsMbpdsd6zQTqlrKAADi-1-72BPM.csv", header=0)
data = dataFile['gamma'].values

analyzer = DataAnalyzer.DataAnalyzer(data)

output = analyzer.getPeriodInfo()
print(output['detectedBPM'])

print(analyzer.getAutocorrelation())

output = analyzer.getPeriods(3, 2)
