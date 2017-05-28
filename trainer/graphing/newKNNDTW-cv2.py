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
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import normalize



#--------------------------------------------------------

DATA_FOLDER = "../data/trainsequences/"
CLASSIFY_FOLDER = "C:/Users/Ruben/Dropbox/Coding/GIT/Thesis/trainer/data/CLASSIFY"
ADDITIONAL_TRAIN_FOLDER = "C:/Users/Ruben/Dropbox/Coding/GIT/Thesisclone/thesis-beam/trainer/data/FLAWED/ADDITIONAL-TRAINED/"
ADDITIONAL_TEST_FOLDER = "C:/Users/Ruben/Dropbox/Coding/GIT/Thesisclone/thesis-beam/trainer/data/FLAWED/ADDITIONAL-TESTED/"

ITERATIONS = 100
TEST_SIZE_PERCENT = 0.30

np.set_printoptions(precision=2)


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


#copyright: http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html
def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')



# ------------------- MAIN ------------------------------------

analyzer = DataAnalyzer.DataAnalyzer()

print("Doing " + str(ITERATIONS) + " iterations with a " + str(TEST_SIZE_PERCENT) + " test ratio")

# -- training --

data_data = []
data_labels = []
data_data_length = []

files = getDataFileNames("")
for trainingFile in files:
  dataFile = pd.read_csv(DATA_FOLDER + trainingFile, header = 0)
  #data = [dataFile['alpha'], dataFile['beta'], dataFile['gamma'], dataFile['accX'], dataFile['accY'], dataFile['accZ']]
  #dataFile = analyzer.normalize(dataFile)
  #dataFile = analyzer.autoCorrelate(dataFile)
  
  data_data.append(dataFile)
  if "updown" in trainingFile:
    data_labels.append("0")
  elif "leftright" in trainingFile:
    data_labels.append("1")
  elif "rotateclock" in trainingFile:
    data_labels.append("2")
  elif "rest" in trainingFile:
    data_labels.append("3")


#-- Additional training data:
additional_data = []
additional_labels = []

files = getDataFileNames("", dataFolder=ADDITIONAL_TRAIN_FOLDER)
for trainingFile in files:
  dataFile = pd.read_csv(ADDITIONAL_TRAIN_FOLDER + trainingFile, header = 0)
  #data = [dataFile['alpha'], dataFile['beta'], dataFile['gamma'], dataFile['accX'], dataFile['accY'], dataFile['accZ']]
  #dataFile = analyzer.normalize(dataFile)
  #dataFile = analyzer.autoCorrelate(dataFile)
  
  additional_data.append(dataFile)
  if "updown" in trainingFile:
    additional_labels.append("0")
  elif "leftright" in trainingFile:
    additional_labels.append("1")
  elif "rotateclock" in trainingFile:
    additional_labels.append("2")
  elif "rest" in trainingFile:
    additional_labels.append("3")





class_names = ['updown', 'leftright', 'rotateclockwise', 'rest']


test_plot_labels = []
predict_labels = []


print("label size:", len(data_data))
print("data size:", len(data_labels))
print("---------")




#all data files loaded, now separate as training & test:


#start the loop:
correct = []
for _ in range(ITERATIONS):

  training_data, test_data, training_labels, test_labels = train_test_split(data_data, data_labels, test_size=TEST_SIZE_PERCENT)


  #------------------- ADDITIONAL TRAINING FILES ---------------------


  for datapoint in additional_data:
    training_data.append(datapoint)
  for labelpoint in additional_labels:
    training_labels.append(labelpoint)


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
      predict_labels.append(model.predict([row]))
      test_plot_labels.append(test_labels[index])
      if test_labels[index] != model.predict([row]):
        test_error.append(test_labels[index])
        print("wrong prediction for " + str(test_labels[index]) + " = " + str(model.predict([row])))

  correct.append((len(test_data)-len(test_error))/len(test_data))
  print((len(test_data)-len(test_error))/len(test_data))



print(correct)
print("Mean: " + str(np.mean(correct)))


cnf_matrix = confusion_matrix(test_plot_labels, predict_labels)
np.set_printoptions(precision=2)

# Plot non-normalized confusion matrix
plt.figure()
plot_confusion_matrix(cnf_matrix, classes=class_names,
                      title='Confusion matrix. '+ str(ITERATIONS)+' iterations, test ratio: ' + str(TEST_SIZE_PERCENT))

# Plot normalized confusion matrix


plt.figure()

normedMatrix = normalize(cnf_matrix, axis=1, norm='l1')
normedMatrix = np.around(normedMatrix, decimals=2)


plot_confusion_matrix(normedMatrix, classes=class_names, title='Confusion matrix. '+ str(ITERATIONS)+' iterations, test ratio: ' + str(TEST_SIZE_PERCENT))
plt.show()
