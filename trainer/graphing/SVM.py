import docopt
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import itertools
from sklearn import svm

from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.decomposition import PCA
from sklearn.model_selection import GridSearchCV

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


  
  training_data.append([dataFile['accX'][:150], dataFile['accY'][:150]])
  if "updown" in trainingFile:
    training_labels.append("updown")
  elif "leftright" in trainingFile:
    training_labels.append("leftright")
  elif "rotateclock" in trainingFile:
    training_labels.append("rotateclockwise")
  elif "rest" in trainingFile:
    training_labels.append("rest")

print("label size:", len(training_data))
print("data size:", len(training_labels))


model = svm.SVC()
parameters = {'kernel':('linear', 'rbf'), 'C':[1, 10]}

#estimators = [('reduce_dim', PCA()), ('clf', svm.SVC())]


clf = GridSearchCV(model, parameters, verbose=True )

clf.fit(training_data, training_labels)


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

  test_data.append([dataObject['accX'][:150], dataObject['accY'][:150]])
  if "updown" in trainingFile:
    test_labels.append("updown")
  elif "leftright" in trainingFile:
    test_labels.append("leftright")
  elif "rotateclock" in trainingFile:
    test_labels.append("rotateclockwise")
  elif "rest" in trainingFile:
    test_labels.append("rest")



print("label size:", len(test_data))
print("data size:", len(test_labels))


for index, data in enumerate(test_data):
    print("SVC prediction for " + str(test_labels[index]) + " = " + str(clf.predict([data])))


