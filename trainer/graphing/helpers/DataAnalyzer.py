import numpy as np
from scipy import fftpack
from scipy import signal
from fastdtw import fastdtw
from sklearn.preprocessing import normalize as skNorm
import scipy.stats as stats

from helpers.detect_peaks import detect_peaks #peak detection module from: https://github.com/demotu/BMC/blob/master/functions/detect_peaks.py (Marcos Duarte)
#remove 'helpers.' if you want to import it from the same folder, as it cannot find its own module




class StreamDataAnalyzer(object):
  '''Analyzes data: FFT, Autocorrelation, BPM & Freq detection'''
  def __init__(self, data, samplingRate = 1000/50):
    '''
    Arguments
      data: a single datastream (ex: datastream of alpha values) 
    '''
    self.data = data
    self.samplingRate = samplingRate

    #calculating FFT already:
    X = fftpack.fft(self.data)
    self.fft = X
    freqs = fftpack.fftfreq(len(self.data)) * self.samplingRate
    self.positive_freqs = freqs[np.where(freqs >= 0)]
    self.magnitudes = X[np.where(freqs > 0)]
    self.peakIndex = np.argmax(self.magnitudes)
    self.detectedFreq = self.positive_freqs[self.peakIndex]
    self.BPM = self.positive_freqs[self.peakIndex] * 60



    
  def getAutocorrelation(self):
    '''Returns the auttocorrelation data of the stream
    Copyright: http://stackoverflow.com/questions/14297012/estimate-autocorrelation-using-python
    '''
    n = len(self.data)
    variance = self.data.var()
    x = self.data-self.data.mean()
    r = np.correlate(x, x, mode = 'full')[-n:]
    result = r/(variance*(np.arange(n, 0, -1))) 
    return result

  def getPeriodInfo(self):
    '''returns detectedBPM and detectedFreq'''
    return {'detectedBPM': self.BPM, 'detectedFreq': self.detectedFreq }

  def getFFTData(self):
    """Returns the FFT data frequencies and magnitudes for plotting

    Returns:
      positive_freqs: which positive frequencies there are analyzed
      magnitudes: corresponding magnitudes of the frequencies
    """
    return {'fft': self.fft, 'positive_freqs': self.positive_freqs, 'magnitudes': self.magnitudes}



  def getPeriods(self, amount, startIndex = 0):
    '''Returns the specified data of an amount of periods regarding to the calculated dominating FFT frequency
      Arguments:
        amount: how many periods shouldf be returned
        startIndex: period number that is being started from. (should probably be a fixed number)
      Returns:
        time: x-values for graphing
        data: data points (y-values)
    '''

    dataPointsLength = int(self.samplingRate / self.detectedFreq)
    #startIndex = dataPointsLength * startIndex

    time = np.linspace(0,(1/self.detectedFreq) * amount, dataPointsLength * amount) # [AMOUNT] times a period (dataPointsLength)
    dataPoints = self.data[startIndex: startIndex + dataPointsLength * amount] # same

    return {'time': time, 'data': dataPoints}


  def getFFTDataFromStream(self, data, samplingRate = 1000/50):
    '''Deprecated'''
    X = fftpack.fft(data)
    freqs = fftpack.fftfreq(len(data)) * samplingRate
    positive_freqs = freqs[np.where(freqs >= 0)]
    magnitudes = X[np.where(freqs > 0)]
    peakIndex = np.argmax(magnitudes)
    detectedFreq = positive_freqs[peakIndex]
    BPM = positive_freqs[peakIndex] * 60

    return {'fft': X, 'positive_freqs': positive_freqs, 'magnitudes': magnitudes, 'detectedFreq': detectedFreq, 'detectedBPM': BPM }



class DataAnalyzer(object):
  def __init__(self):
    '''
    Class for analyzing the Object containing all the streams itself.
    '''
    #no init

  def DTWSimilarity(self, dataX, dataY, gyroscope=False):
    '''
    Provide the loaded dataFiles, then this function will extract the accX, accY & accZ for you. When gyroscope parameter is set to True, it will also calculate the alpha, beta and gamma aswell, but disabled due to speed
    Arguments:
      dataX: First data object
      dataY: Second data object
    '''
    self.dataX = dataX
    self.dataY = dataY

    X, path = fastdtw(dataX['accX'], dataY['accX'])
    Y, path = fastdtw(dataX['accY'], dataY['accY'])
    Z, path = fastdtw(dataX['accZ'], dataY['accZ'])
    if (gyroscope):
        alpha, path = fastdtw(dataX['alpha'], dataY['alpha'])
        beta, path = fastdtw(dataX['beta'], dataY['beta'])
        gamma, path = fastdtw(dataX['gamma'], dataY['gamma'])

    '''
    Calculate similarity function as written in paper:
    (Akl, A., Feng, C., & Valaee, S. (2011). A novel accelerometer-based gesture recognition system. IEEE Transactions on Signal Processing, 59(12), 6197-6205.
    ISO 690)
    '''
    if (gyroscope):
        return -1 * ((X**2) + (Y**2) + (Z**2) + (alpha**2) + (beta**2) + (gamma**2))
    else:
        return -1 * ((X**2) + (Y**2) + (Z**2))
    
  def normalize(self, dataObject):
    '''
    Normalizes the data using SciKit methods. (sklearn.preprocessing.normalize)
    Own extension: combined normalization, where the datastreams alpha, beta and gamma are grouped together (accX, accY, accZ responsibly)
    in order to not normalize each stream individually.
    Arguments:
      data: data object to be normalized (will return a deep copy)
    '''
    data = dataObject.copy() #make sure to create a copy, otherwise the same object will just be altered!!

    # COMBINED NORMALIZATION FOR ALPHA/BETA/GAMMA:
    dataRaw = []
    dataRaw.extend(dataObject['alpha'].values)
    dataRaw.extend(dataObject['beta'].values)
    dataRaw.extend(dataObject['gamma'].values)
    dataRaw = skNorm([dataRaw])[0] #weird to use as input, but for the scikit you should append a deeper dimension. Fix is to immediately escape out of it.

    #split the stacked array back into original parts:
    currIter = 0
    dataAlpha = dataRaw[:len(dataObject['alpha'].values)]
    currIter = len(dataObject['alpha'].values);
    dataBeta = dataRaw[currIter:currIter + len(dataObject['beta'].values)]
    currIter += len(dataObject['beta'].values)
    dataGamma = dataRaw[currIter:currIter + len(dataObject['gamma'].values)]

    # COMBINED NORMALIZATION FOR X/Y/Z:
    dataRaw = []
    dataRaw.extend(dataObject['accX'].values)
    dataRaw.extend(dataObject['accY'].values)
    dataRaw.extend(dataObject['accZ'].values)
    dataRaw = skNorm([dataRaw])[0] 

    #split the stacked array back into original parts:
    currIter = 0
    dataaccX = dataRaw[:len(dataObject['accX'].values)]
    currIter = len(dataObject['accX'].values);
    dataaccY = dataRaw[currIter:currIter + len(dataObject['accY'].values)]
    currIter += len(dataObject['accY'].values)
    dataaccZ = dataRaw[currIter:currIter + len(dataObject['accZ'].values)]

    #set the new calculated values:
    data['accX'] = dataaccX
    data['accY'] = dataaccY
    data['accZ'] = dataaccZ
    data['alpha'] = dataAlpha
    data['beta'] = dataBeta
    data['gamma'] = dataGamma
    #data['alpha'] = skNorm([data['alpha']])[0] #took me hours to figure out why indexes weren't correct. Never forget the [0]
    #data['beta'] = skNorm([data['beta']])[0]
    #data['gamma'] = skNorm([data['gamma']])[0]
    return data

  def autoCorrelate(self, dataObject):
    data = dataObject.copy()
    data['accX'] = StreamDataAnalyzer(data['accX']).getAutocorrelation()
    data['accY'] = StreamDataAnalyzer(data['accY']).getAutocorrelation()
    data['accZ'] = StreamDataAnalyzer(data['accZ']).getAutocorrelation()
    data['alpha'] = StreamDataAnalyzer(data['alpha']).getAutocorrelation()
    data['beta'] = StreamDataAnalyzer(data['beta']).getAutocorrelation()
    data['gamma'] = StreamDataAnalyzer(data['gamma']).getAutocorrelation()

    return data

class AutoAnalyzer(object):
  '''Uses the data Object which automatically detects the best stream to use
  Returns:
    BPM which it thinks it is the closest by. This is a result of the median of all the calculated BPMs.
  '''
  def __init__(self, dataObject):
    self.data = dataObject
    self.samplingRate = 1000/50

  def getBPM(self, autocorrelated = True, printAll = False):
    data = self.data.copy()
    analyzer = DataAnalyzer()
    if (autocorrelated):
      data = analyzer.autoCorrelate(data)

    detectedBPMs = []
    streams = ['accX', 'accY', 'accZ', 'alpha', 'beta', 'gamma']
    for stream in streams:
        detectedBPMs.append((stream, StreamDataAnalyzer(data[stream]).getPeriodInfo()['detectedBPM']))

    data = [y for x,y in detectedBPMs] # only the peaks (not streams)
    bpmIndex = np.argsort(data)[len(data)//2]
    #FINISH THIS!!

    if (printAll):
      print(data)
      print(np.median(data))


    #returns the median of all the BPMs, in order to get the most occuring one.
    self.BPM = np.median(data)
    self.preferredStreamFromBPM = streams[bpmIndex]
    return(self.BPM, streams[bpmIndex])
  

  def getLastPeakTime(self, visualize=False, periods=1, startingPeriod = 2):

    # Peak time cannot be calculated when there is no BPM yet:
    if not hasattr(self, 'BPM'):
        self.getBPM(autocorrelated=True)
    length = int(self.samplingRate / (self.BPM/60))
    startIndex = length * startingPeriod  # <-- Start extracting the peak from the 2nd period
    rates = np.array([70,80,90,100,110,130,140])/60 #BPMs to test


    # If we take the data from the preferred stream:
    '''
    piece = self.data[self.preferredStreamFromBPM][startIndex: startIndex+length*2*periods]
    peak = detect_peaks(piece)
    if len(peak) > 0:
        peakTimeIndex = startIndex + peak[0]
    '''

    # Get the first peak from the different streams
    possiblePeaks = []
    streams = ['accX', 'accY', 'accZ', 'alpha', 'beta', 'gamma']
    for stream in streams:
        piece = self.data[stream][startIndex: startIndex+length * periods] # get only 1 period, meaning 2 hertz cycles [2pi].
        # old peak function:
        #peak = signal.find_peaks_cwt(piece, samplingRate/rates/2)
        peak = detect_peaks(piece)
        if len(peak) > 0:
            possiblePeaks.append((stream, startIndex + peak[0]))
            #print("peak value: " + str(self.data[stream][startIndex + peak[0]]))
            #print("peak time index: " + str(startIndex + peak[0]))
            #print("peak system time: " + str(self.data['timestamp'][startIndex + peak[0]]))


    data = [y for x,y in possiblePeaks] # only the peak times (not streams) (this is not peak VALUE, but peak TIME)
    peakIndex = np.argsort(data)[len(data)//2] #gets the median of all the possible peaks, likely to be the middle one?


    #print("length: ", (startIndex+length*2 - startIndex))

    # CAN THROW OUT OF BOUNDS ERROR, WHEN CLASSIFYING FILE DOES NOT CONTAIN 2 PERIODS OF DATA

    peakStream = possiblePeaks[peakIndex][0]
    peakTimeIndex = possiblePeaks[peakIndex][1]

    if (visualize):
        print("Stream chosen by peak detection: " + str(peakStream))
        print("Shows the datastream of where the peak should be found, not the stream from the peak until end itself!")
        from helpers import Visualizer
        visualizer = Visualizer.Visualizer(self.data)

        #print("stream: ", peakStream)
        #visualizer.visualizeStream(self.data[self.preferredStreamFromBPM][startIndex : startIndex+length*periods], vLine=(peakTimeIndex-startIndex))
        #change self.preferredStreamFromBPM to peakStream if you want to visualize the chosen stream from the peak analyzer instead of BPM.
        visualizer.visualizeStream(self.data[self.preferredStreamFromBPM][startIndex : startIndex+length*periods] )


        '''
        vLine means a vertical line on the axis. Vertical line should be placed on the detected peak. Because the startIndex is already inside the possiblePeaks,
        you have to deduct it to get the right placement
        '''


    return {'time': self.data['timestamp'][peakTimeIndex], 'bpm': self.BPM, 'index': peakTimeIndex}
    

  def getPeriods(self, amount, startIndexPeriod = 0):
    '''Returns the specified data of an amount of periods regarding to the calculated dominating FFT frequency
      Arguments:
        amount: how many periods should be returned
        startIndex: period number that is being started from. (should probably be a fixed number)
      Returns:
        time: x-values for graphing
        data: data points (y-values)
    '''
    if not hasattr(self, 'BPM'):
        self.getBPM(autocorrelated=True)
    if self.BPM < 10:
        self.BPM = 1
    dataPointsLength = int(self.samplingRate / (self.BPM/60)) #self.bpm / 60 because you want to get the frequency.
    startIndexPeriod = dataPointsLength * startIndexPeriod # skip the amount of periods provided by startIndexPeriod

    time = np.linspace(0,(1/(self.BPM/60)) * amount, dataPointsLength * amount) # [AMOUNT] times a period (dataPointsLength)
    dataPoints = self.data[startIndexPeriod: startIndexPeriod + dataPointsLength * amount] # same

    return {'time': time, 'data': dataPoints}

  def getPeriodsFromDataIndex(self, amount, index):
    '''returns specified periods based on the index of the datafile. This index could be a peak of the data,
    and start extracting a specified amount of periods from there
    '''
    if not hasattr(self, 'BPM'):
        self.getBPM(autocorrelated=True)
    dataPointsLength = int(self.samplingRate / (self.BPM/60)) #self/bpm / 60 because you want to get the frequency.

    time = np.linspace(0,(1/(self.BPM/60)) * amount, dataPointsLength * amount) # [AMOUNT] times a period (dataPointsLength)
    dataPoints = self.data[index: index + dataPointsLength * amount] # same

    return {'time': time, 'data': dataPoints}
