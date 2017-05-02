import docopt
from sklearn.cluster import AffinityPropagation
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import itertools

import os #filesystem reads

#for supervised hmm shit

from helpers import DataAnalyzer

DATA_FOLDER = "../data/"
CLASSIFY_FOLDER = "C:/Users/Ruben/Dropbox/Coding/GIT/Thesis/trainer/data/CLASSIFY"


# Helper functions:


# get all the data files from the directory
def getDataFileNames(dataType, movement = "", dataFolder = DATA_FOLDER):
  files = os.listdir(dataFolder);
  output = []
  for file in files:
    if dataType in file and movement in file:
      output.append(file)
  return output



# ------------------- MAIN ------------------------------------

analyzer = DataAnalyzer.DataAnalyzer()

# -- training --

training_data = []
training_labels = []
training_data_length = []

files = getDataFileNames("training")
for trainingFile in files:
  dataFile = pd.read_csv(DATA_FOLDER + trainingFile, header = 0)
  #data = [dataFile['alpha'], dataFile['beta'], dataFile['gamma'], dataFile['accX'], dataFile['accY'], dataFile['accZ']]
  dataFile = analyzer.normalize(dataFile)
  dataFile = analyzer.autoCorrelate(dataFile)
  
  training_data.append(dataFile)
  if "updown" in trainingFile:
    training_labels.append("updown")
  elif "leftright" in trainingFile:
    training_labels.append("leftright")
  elif "rotateclock" in trainingFile:
    training_labels.append("rotateclockwise")

print("label size:", len(training_data))
print("data size:", len(training_labels))


training_matrix = np.zeros((len(training_data),len(training_data)))

'''
for data in training_data:
  row = []
  for secondData in training_data:
    row.append(analyzer.DTWSimilarity(data, secondData))
  training_matrix.append(row)
'''

#Enhanced method for creating the  DTW Similarity matrix. Now only computes the first half of the matrix
for n in itertools.combinations(np.arange(len(training_data)), 2):
  calculation = analyzer.DTWSimilarity(training_data[n[0]], training_data[n[1]])
  training_matrix[n[0], n[1]] = calculation
  training_matrix[n[1], n[0]] = calculation

model = KNeighborsClassifier()
#model = AffinityPropagation()
model.fit(training_matrix, training_labels)




#----- testing -------

test_data = []
test_labels = []
test_data_length = []


files = getDataFileNames("test")
for trainingFile in files:
  dataObject = pd.read_csv(DATA_FOLDER + trainingFile, header = 0)
  #data = [dataFile['accX'], dataFile['accY'], dataFile['accZ']]
  #data = [dataFile['alpha'], dataFile['beta'], dataFile['gamma'], dataFile['accX'], dataFile['accY'], dataFile['accZ']]
  dataObject = analyzer.normalize(dataObject)
  dataObject = analyzer.autoCorrelate(dataObject)

  test_data.append(dataObject)
  if "updown" in trainingFile:
    test_labels.append("updown")
  elif "leftright" in trainingFile:
    test_labels.append("leftright")
  elif "rotateclock" in trainingFile:
    test_labels.append("rotateclockwise")

  autoanalyzer = DataAnalyzer.AutoAnalyzer(dataObject)
  print("BPM: " + str(autoanalyzer.getBPM(autocorrelated=True)))


print("label size:", len(test_data))
print("data size:", len(test_labels))


for index, data in enumerate(test_data):
    row = []
    for secondData in training_data:
      row.append(analyzer.DTWSimilarity(data, secondData))

    print("AffinityProp prediction for " + str(test_labels[index]) + " = " + str(model.predict([row])))


'''

for index, t in enumerate(test_data):

  test_matrix = []

  for data in t:
    row = []
    for secondData in t:
      row.append(analyzer.DTWSimilarity(data, secondData))
    test_matrix.append(row)

  print("AffinityProp prediction for " + str(test_labels[index]) + " = " + str(model.predict(test_matrix)))

'''