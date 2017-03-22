import pandas as pd
import numpy as np
from seqlearn.hmm import MultinomialHMM


model = MultinomialHMM(decode='viterbi', alpha=0.01)

# -- training --

training_data = []
training_labels = []
training_data_length = []



dataFile = pd.read_csv("../data/training-leftright-avkfxrmpauHdDpeaAAAa-3.csv", header = 0)
data = [dataFile['accX'][:5], dataFile['accY'][:5], dataFile['accZ'][:5]]
#data = [dataFile['alpha'], dataFile['beta'], dataFile['gamma'], dataFile['accX'], dataFile['accY'], dataFile['accZ']]

length = len(dataFile['accX'][:5])
training_data_length.append([length, length, length]) # 3 items because X, Y, Z data

training_data.append(data)
training_labels.append('leftright')




dataFile = pd.read_csv("../data/training-updown-avkfxrmpauHdDpeaAAAa-1.csv", header=0)
data = [dataFile['accX'][:5], dataFile['accY'][:5], dataFile['accZ'][:5]]
#data = [dataFile['alpha'], dataFile['beta'], dataFile['gamma'], dataFile['accX'], dataFile['accY'], dataFile['accZ']]

length = len(dataFile['accX'][:5])
training_data_length.append([length, length, length]) # 3 items because X, Y, Z data

training_data.append(data)
training_labels.append('updown')



model.fit(training_data[0], training_labels, training_data_length)
