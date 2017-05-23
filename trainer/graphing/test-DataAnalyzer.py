import helpers
from helpers import DataAnalyzer, Visualizer, Socket
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import itertools
import scipy.stats as stats
from sklearn.preprocessing import normalize
from scipy import signal


from sklearn import svm
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.decomposition import PCA
from sklearn.model_selection import GridSearchCV





samplingRate = 1000/50



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






#cnf_matrix = confusion_matrix(test_plot_labels, predict_labels)
class_names = ['updown', 'leftright', 'rotateclockwise', 'rest']

cnf_matrix = np.array([[662,0,42,34],[0,332,0,0],[ 22,10,532,298],[ 23,20,181,544]])
np.set_printoptions(precision=2)

# Plot non-normalized confusion matrix
plt.figure()
plot_confusion_matrix(cnf_matrix, classes=class_names,
                      title='Confusion matrix. 100 iterations, test ratio: 0.3')

# Plot normalized confusion matrix


plt.figure()

normedMatrix = normalize(cnf_matrix, axis=1, norm='l1')
normedMatrix = np.around(normedMatrix, decimals=2)


plot_confusion_matrix(normedMatrix, classes=class_names,
                      title='Confusion matrix. 100 iterations, test ratio: 0.3')
plt.show()



#dataFile = pd.read_csv("../data/CLASSIFY-sequences/updown-77.4193548387-1495458620208.csv", header=0)
#dataFile2 = pd.read_csv("../data/testing-leftright-qsMbpdsd6zQTqlrKAADi-1-72BPM.csv")


#aa = DataAnalyzer.AutoAnalyzer(dataFile)
#data = aa.getPeriods(2, startIndex=1)['data']


#dataFile2 = pd.read_csv("../data/training-leftright-avkfxrmpauHdDpeaAAAa-3.csv", header=0)
#dataFile3 = pd.read_csv("../data/training-updown-avkfxrmpauHdDpeaAAAa-1.csv", header=0)
#dataFile4 = pd.read_csv("../data/training-rotateclockwise-avkfxrmpauHdDpeaAAAa-6.csv", header=0)

#d = DataAnalyzer.DataAnalyzer()

#dataFile = d.normalize(dataFile)
#dataFile = d.autoCorrelate(dataFile)


#v = Visualizer.Visualizer(dataFile)

#aa = DataAnalyzer.AutoAnalyzer(dataFile)

#out = aa.getLastPeakTime()
#print(out)


#v.visualizeSequence(dataFile)




'''

totaldata = []
totallabels = []




data = []
for index,item in enumerate(dataFile['accX'][:5]):
  data.append([dataFile['accX'][index], dataFile['accY'][index], dataFile['accZ'][index]])


#data.append([dataFile['accX'], dataFile['accY'], dataFile['accZ']])
data = np.array(data)
pca = PCA(n_components=3, whiten=True)
transformed_dataset = PCA.fit_transform(pca, data)
transformed_dataset = transformed_dataset.reshape(-1,1)[0]
print(transformed_dataset)

totaldata.append(transformed_dataset)
totallabels.append("updown")

totaldata.append(transformed_dataset)
totallabels.append("left-right")


print(totaldata)



model = svm.SVC()
parameters = {'kernel':('linear', 'rbf'), 'C':[1, 10]}

#estimators = [('reduce_dim', PCA()), ('clf', svm.SVC())]


clf = GridSearchCV(model, parameters, verbose=True )

model.fit(totaldata, totallabels)

'''


'''

length = int(samplingRate / (bpm[0]/60))
startIndex = length * 2  # <-- Start extracting the peak from the 2nd period
rates = np.array([70,80,90,100,110,120,130,140])/60 #BPMs to test

piece = dataFile['accZ'][startIndex: startIndex+length*2]

peak = signal.find_peaks_cwt(piece, samplingRate/rates/2)
print(peak)

'''
#visualizer.visualizeStream(piece, vLine=peak[0])
#continue next time with this

''''
streams = ['accX', 'accY', 'accZ', 'alpha', 'beta', 'gamma']
for stream in streams:
  print(dataFile[stream][1:4])

'''

'''
print(analyzer.getBPM(autocorrelated=True, printAll=True))
print(analyzer.getBPM(autocorrelated=False, printAll=True))
'''



'''
dataRaw = []
dataRaw.extend(dataFile['accX'].values)
dataRaw.extend(dataFile['accY'].values)
dataRaw.extend(dataFile['accZ'].values)

currIter = 0
dataX = dataRaw[:len(dataFile['accX'].values)]
currIter = len(dataFile['accX'].values);
dataY = dataRaw[currIter:currIter + len(dataFile['accY'].values)]
currIter += len(dataFile['accY'].values)
dataZ = dataRaw[currIter:currIter + len(dataFile['accZ'].values)]

#tests:
print(dataFile['accX'].values == dataX)
print(dataFile['accY'].values == dataY)
print(dataFile['accZ'].values == dataZ)
'''


'''

normalizeAlpha = skNorm([dataFile['beta']])[0]
out = analyzer.normalize(dataFile)

visualizer.visualizeStream(normalizeAlpha)
visualizer.visualizeStream(out['alpha'])

'''

'''
output = analyzer.getPeriodInfo()
print('Normal: ', output['detectedBPM'])
fft = analyzer.getFFTData()
X = np.abs(fft['fft'][:fft['positive_freqs'].size])
print(stats.normaltest(X))
visualizer = Visualizer.Visualizer(dataFile)
visualizer.visualizeStream(dataAlpha)
visualizer.visualizeFFT(fft['fft'], fft['positive_freqs'], title='FFT Normal Data')




analyzer2 = DataAnalyzer.StreamDataAnalyzer(analyzer.getAutocorrelation())
output2 = analyzer2.getPeriodInfo()
print('Autocorrelated: ', output2['detectedBPM'])

fft2 = analyzer2.getFFTData()
X = np.abs(fft2['fft'][:fft2['positive_freqs'].size])
print(stats.normaltest(X))
visualizer.visualizeFFT(fft2['fft'], fft2['positive_freqs'], title='FFT Autocorrelated Data')

'''



'''

#-----------------------
#detecting normality of FFT data:
analyzer = DataAnalyzer.StreamDataAnalyzer(dataAlpha)
fft = analyzer.getFFTData()
visualizer.visualizeFFT(fft['fft'], fft['positive_freqs'], title='FFT Normal Data')
X = np.abs(fft['fft'][:fft['positive_freqs'].size])
stats.normaltest(X)
visualizer.visualizeStream(X)
#-----------------------------



'''