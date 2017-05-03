import docopt
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import itertools
import os #filesystem reads
from helpers import DataAnalyzer

#Crossvalidation:
from sklearn.model_selection import train_test_split

#--------------------------------------------------------

DATA_FOLDER = "../data/"
CLASSIFY_FOLDER = "C:/Users/Ruben/Dropbox/Coding/GIT/Thesis/trainer/data/CLASSIFY"

ITERATIONS = 30
TEST_SIZE_PERCENT = 0.2

#--------------------------------------------------------


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

print("Doing " + str(ITERATIONS) + " iterations with a " + str(TEST_SIZE_PERCENT) + " test ratio")

# -- training --

data_data = []
data_labels = []
data_data_length = []

files = getDataFileNames("training")
for trainingFile in files:
  dataFile = pd.read_csv(DATA_FOLDER + trainingFile, header = 0)
  #data = [dataFile['alpha'], dataFile['beta'], dataFile['gamma'], dataFile['accX'], dataFile['accY'], dataFile['accZ']]
  dataFile = analyzer.normalize(dataFile)
  dataFile = analyzer.autoCorrelate(dataFile)
  
  data_data.append(dataFile)
  if "updown" in trainingFile:
    data_labels.append("updown")
  elif "leftright" in trainingFile:
    data_labels.append("leftright")
  elif "rotateclock" in trainingFile:
    data_labels.append("rotateclockwise")

print("label size:", len(data_data))
print("data size:", len(data_labels))
print("---------")

#all data files loaded, now separate as training & test:


#start the loop:
correct = []
for _ in range(ITERATIONS):

  training_data, test_data, training_labels, test_labels = train_test_split(data_data, data_labels, test_size=TEST_SIZE_PERCENT)




  #------------ TRAINING -----------------

  #print("train label size:", len(training_labels))
  #print("train data size:", len(training_data))

  training_matrix = np.zeros((len(training_data),len(training_data)))

  #Enhanced method for creating the  DTW Similarity matrix. Now only computes the first half of the matrix
  for n in itertools.combinations(np.arange(len(training_data)), 2):
    calculation = analyzer.DTWSimilarity(training_data[n[0]], training_data[n[1]])
    training_matrix[n[0], n[1]] = calculation
    training_matrix[n[1], n[0]] = calculation

  model = KNeighborsClassifier()

  model.fit(training_matrix, training_labels)




  #----------- TESTING -------------------

  #test_data = []
  #test_labels = []
  #test_data_length = []



  #print("test data size:", len(test_data))
  #print("test label size:", len(test_labels))

  test_error = []
  for index, data in enumerate(test_data):
      row = []
      for secondData in training_data:
        row.append(analyzer.DTWSimilarity(data, secondData))

      #print("AffinityProp prediction for " + str(test_labels[index]) + " = " + str(model.predict([row])))
      if test_labels[index] != model.predict([row]):
        test_error.append(test_labels[index])
        print("wrong prediction for " + str(test_labels[index]) + " = " + str(model.predict([row])))

  correct.append((len(test_data)-len(test_error))/len(test_data))
  print((len(test_data)-len(test_error))/len(test_data))

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
print(correct)
print("Mean: " + str(np.mean(correct)))