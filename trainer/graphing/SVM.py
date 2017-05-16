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

#update below if you do not want to use PCA, and which stream to choose from.
preferredStream = 'accY'
noPCA = False;


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
  #dataFile = analyzer.autoCorrelate(dataFile)


  data = []
  for index,item in enumerate(dataFile['accX'][:75]): #<--- CHANGE THIS TO THE LENGTH OF DATASET, DIFFERENT FOR CLASSIFICATION
    data.append([dataFile['accX'][index], dataFile['accY'][index], dataFile['accZ'][index]])


  data = np.array(data)
  pca = PCA(n_components=3, copy=True, whiten=True)
  reduced_data = PCA.fit_transform(pca, data)
  pca_training_data = reduced_data.reshape(-1,1)[0]

  if noPCA:
    pca_training_data = dataFile[preferredStream][:100]
  
  training_data.append(pca_training_data)
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
Cs = np.linspace(1,3,400)
Cs = np.arange(94,120, 200)


#CONTINUE HERE: hyperparameter optimization, by adding more gamma and Cs
param_grid = [
  {'C': Cs, 'kernel': ['linear']},
  #{'C': Cs, 'gamma': [0.1], 'kernel': ['rbf']},
  
 ]

clf = GridSearchCV(model, param_grid)

clf.fit(training_data, training_labels)



print("Best parameters: ", clf.best_params_)
print("Score: ", clf.best_score_)


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
  #dataObject = analyzer.autoCorrelate(dataObject)


  data = []
  for index,item in enumerate(dataObject['accX'][:75]): #<--- CHANGE THIS TO THE LENGTH OF DATASET, DIFFERENT FOR CLASSIFICATION, was 150
    data.append([dataObject['accX'][index], dataObject['accY'][index], dataObject['accZ'][index]])


  data = np.array(data)
  pca = PCA(n_components=3, copy=True, whiten=True)
  reduced_data = PCA.fit_transform(pca, data)
  pca_test_data = reduced_data.reshape(-1,1)[0]

  if noPCA:
    pca_test_data = dataObject[preferredStream][:100]

  test_data.append(pca_test_data)
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


