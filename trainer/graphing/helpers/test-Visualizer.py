import pandas as pd
import Visualizer
import DataAnalyzer


dataFile = pd.read_csv("../../data/testing-leftright-qsMbpdsd6zQTqlrKAADi-1-72BPM.csv", header=0)
#normal data

visualizer = Visualizer.Visualizer(dataFile)
visualizer.visualizeStream(dataFile.gamma,correlated=True)
