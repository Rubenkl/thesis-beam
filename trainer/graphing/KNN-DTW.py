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


DATA_FOLDER = "../data/"


# Helper functions:

# get all the data files from the directory
def getDataFileNames(dataType, movement = ""):
  files = os.listdir(DATA_FOLDER);
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


training_data = []
training_labels = []

files = getDataFileNames("training")
for trainingFile in files:
  dataFile = pd.read_csv(DATA_FOLDER + trainingFile, header = 0)
  #data = [dataFile['accX'], dataFile['accY'], dataFile['accZ']]
  data = [dataFile['alpha'], dataFile['beta'], dataFile['gamma'], dataFile['accX'], dataFile['accY'], dataFile['accZ']]
  
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

test_data =[]
test_labels =[]

files = getDataFileNames("test")
for trainingFile in files:
  dataFile = pd.read_csv(DATA_FOLDER + trainingFile, header = 0)
  #data = [dataFile['accX'], dataFile['accY'], dataFile['accZ']]
  data = [dataFile['alpha'], dataFile['beta'], dataFile['gamma'], dataFile['accX'], dataFile['accY'], dataFile['accZ']]


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

'''

#original_headers = list(dataFile.columns.values)
N = 198

time = np.linspace(0,20, 198)


#importing data


dataFile = pd.read_csv("../data/training-updown-RbWE5pRKUdnyeTTAAAI-1.csv", header =0)
dataA = dataFile['beta'].values

dataFileB = pd.read_csv("../data/training-updown-RbWE5pRKUdnyeTTAAAI-2.csv", header=0)
dataB = dataFileB['beta'].values

dataFileC = pd.read_csv("../data/training-leftright-RbWE5pRKUdnyeTTAAAI-3.csv", header=0)
dataC = dataFileC['beta'].values

dataFileF = pd.read_csv("../data/training-leftright-RbWE5pRKUdnyeTTAAAI-4.csv", header=0)
dataF = dataFileF['beta'].values

dataFileD = pd.read_csv("../data/training-updown-RbWE5pRKUdnyeTTAAAI-7.csv", header=0)
dataD = dataFileD['beta'].values

dataFileE = pd.read_csv("../data/training-updown-RbWE5pRKUdnyeTTAAAI-6.csv", header=0)
dataUpdownTest = dataFileE['beta'].values

dataFileQuick = pd.read_csv("../data/training-updown-mg8f0Om0lSmaYI9AAAP-1-QUICK.csv", header=0)
dataQuick = dataFileQuick['beta'].values

dataTestLeftRight = pd.read_csv("../data/training-leftright-RbWE5pRKUdnyeTTAAAI-8.csv", header=0)
dataLeftrightTest = dataTestLeftRight['beta'].values


#adding data arrays to a new array for training
training_data = np.array([dataA, dataB, dataC, dataF, dataD, dataQuick])
training_labels = np.array(['updown', 'updown', 'leftright', 'leftright', 'updown', 'updown'])
test_data = [dataUpdownTest, dataLeftrightTest]
test_labels = ['updown', 'leftright']

'''


clf1 = KnnDtwClassifier(1)
clf1.fit(training_data, training_labels)


for index, t in enumerate(test_data):
  print("KNN-DTW prediction for " + str(test_labels[index]) + " = " + str(clf1.predict(t)))

#plotting:

for i in range (0, 35, 5):
    hist, bins = np.histogram(training_data[i], bins=20)
    width = 0.7 * (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2
    plt.title(training_labels[i])
    plt.bar(center, hist, align='center', width=width)
    plt.show()



#fdataD = fftpack.fft(dataA)

#distance, path = fastdtw(dataA, dataQuick)

#print(distance)



# from: https://raw.githubusercontent.com/markdregan/K-Nearest-Neighbors-with-Dynamic-Time-Warping/master/K_Nearest_Neighbor_Dynamic_Time_Warping.ipynb
'''
fig = plt.figure(figsize=(12,4))
_ = plt.plot(time, dataA, label='A')
_ = plt.plot(time, dataQuick, label='Quick')
_ = plt.title('DTW distance between A and Quick is %.2f' % distance)
_ = plt.ylabel('Amplitude')
_ = plt.xlabel('Time')
_ = plt.legend()
plt.show()
'''
