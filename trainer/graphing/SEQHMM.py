import docopt
import sklearn
import numpy as np
import pandas as pd
import matplotlib.pylab as plt

import os #filesystem reads

#for supervised hmm shit
from seqlearn.hmm import MultinomialHMM

import helpers #custom modules, yay!


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

model = MultinomialHMM(decode='viterbi', alpha=0.01)

# -- training --

training_data = []
training_labels = []
training_data_length = []

files = getDataFileNames("training")
for trainingFile in files:
  dataFile = pd.read_csv(DATA_FOLDER + trainingFile, header = 0)
  data = [dataFile['accX'][:199], dataFile['accY'][:199], dataFile['accZ'][:199]]
  #data = [dataFile['alpha'], dataFile['beta'], dataFile['gamma'], dataFile['accX'], dataFile['accY'], dataFile['accZ']]
  
  length = len(dataFile['accX'])
  training_data_length.append([length, length, length]) # 3 items because X, Y, Z data
  
  training_data.append(data)
  if "updown" in trainingFile:
    training_labels.append("updown")
  elif "leftright" in trainingFile:
    training_labels.append("leftright")
  elif "rotateclock" in trainingFile:
    training_labels.append("rotateclockwise")

print("label size:", len(training_data))
print("data size:", len(training_labels))

model.fit(training_data, training_labels, training_data_length)

#----- testing -------

test_data = []
test_labels = []
test_data_length = []


files = getDataFileNames("test")
for trainingFile in files:
  dataFile = pd.read_csv(DATA_FOLDER + trainingFile, header = 0)
  data = [dataFile['accX'], dataFile['accY'], dataFile['accZ']]
  #data = [dataFile['alpha'], dataFile['beta'], dataFile['gamma'], dataFile['accX'], dataFile['accY'], dataFile['accZ']]
  length = len(dataFile['accX'])
  test_data_length.append([length, length, length])
  
  test_data.append(data)
  if "updown" in trainingFile:
    test_labels.append("updown")
  elif "leftright" in trainingFile:
    test_labels.append("leftright")
  elif "rotateclock" in trainingFile:
    test_labels.append("rotateclockwise")



print("label size:", len(test_data))
print("data size:", len(test_labels))




for index, t in enumerate(test_data):
  print("HMM prediction for " + str(test_labels[index]) + " = " + str(model.predict(t)))

