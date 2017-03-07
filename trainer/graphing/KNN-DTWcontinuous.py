import docopt
import sklearn
import numpy as np
import pandas as pd
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean
import matplotlib.pylab as plt

from scipy import fftpack

import os #filesystem reads

#for knn shit
from tinylearn import KnnDtwClassifier
from tinylearn import CommonClassifier

from helpers import FolderWatch #custom module, yay!


DATA_FOLDER = "../data/"
CLASSIFY_FOLDER = "../data/CLASSIFY/"


# Helper functions:


# get all the data files from the directory
def getDataFileNames(dataType, movement = "", dataFolder = DATA_FOLDER):
  files = os.listdir(dataFolder);
  output = []
  for file in files:
    if dataType in file and movement in file:
      output.append(file)
  return output


#FROM THE TINYLEARN.PY:
# Utility function for normalizing numpy arrays
def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


# ------------------- MAIN ------------------------------------


# -- training --

training_data = []
training_labels = []

files = getDataFileNames("training")
for trainingFile in files:
  dataFile = pd.read_csv(DATA_FOLDER + trainingFile, header = 0)
  data = [dataFile['accX'], dataFile['accY'], dataFile['accZ']]
  #data = [dataFile['alpha'], dataFile['beta'], dataFile['gamma'], dataFile['accX'], dataFile['accY'], dataFile['accZ']]
  
  #flatten all the data, don't really know why you want to separate all the contained data into a flat field.... (just ask this)
  data = normalize(np.ravel(data))

  training_data.append(data)
  if "updown" in trainingFile:
    training_labels.append("updown")
  elif "leftright" in trainingFile:
    training_labels.append("leftright")
  elif "rotateclock" in trainingFile:
    training_labels.append("rotateclockwise")

print("label size:", len(training_data))
print("data size:", len(training_labels))

clf1 = KnnDtwClassifier(1)
clf1.fit(training_data, training_labels)



# -- testing --
global previousFile
previousFile = "none"

def classify(classiFile):
  global previousFile
  if (previousFile == "none"):
    previousFile = classiFile
    FolderWatch.FolderWatch(CLASSIFY_FOLDER, classify)
  else:
    print("classifying: " + previousFile)

# CONTINUE WITH THE TESTINT SHIT ITSELF HERE!!


FolderWatch.FolderWatch(CLASSIFY_FOLDER, classify)


test_data =[]
test_labels =[]

'''

files = getDataFileNames("test")
for trainingFile in files:
  dataFile = pd.read_csv(DATA_FOLDER + trainingFile, header = 0)
  data = [dataFile['accX'], dataFile['accY'], dataFile['accZ']]
  #data = [dataFile['alpha'], dataFile['beta'], dataFile['gamma'], dataFile['accX'], dataFile['accY'], dataFile['accZ']]
  
  #same story here
  data = normalize(np.ravel(data))
  
  
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
  print("KNN-DTW prediction for " + str(test_labels[index]) + " = " + str(clf1.predict(t)))

'''