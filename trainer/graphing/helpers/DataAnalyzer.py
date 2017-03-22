import numpy as np
from scipy import fftpack
from fastdtw import fastdtw
from sklearn.preprocessing import normalize as skNorm


  
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


  '''
  # old code:
  def estimated_autocorrelation(self, x):
    n = len(x)
    variance = x.var()
    x = x-x.mean()
    r = np.correlate(x, x, mode = 'full')[-n:]
    #assert N.allclose(r, N.array([(x[:n-k]*x[-(n-k):]).sum() for k in range(n)]))
    result = r/(variance*(np.arange(n, 0, -1)))
    return result
  '''

  def getAutocorrelation(self):
    '''Returns the auttocorrelation data of the stream'''
    n = len(self.data)
    variance = self.data.var()
    x = self.data-self.data.mean()
    r = np.correlate(x, x, mode = 'full')[-n:]
    #assert N.allclose(r, N.array([(x[:n-k]*x[-(n-k):]).sum() for k in range(n)]))
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
        amount: how many periods should be returned
        startIndex: period number that is being started from. (should probably be a fixed number)
      Returns:
        time: x-values for graphing
        data: data points (y-values)
    '''

    dataPointsLength = int(self.samplingRate / self.detectedFreq)
    startIndex = dataPointsLength * startIndex

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

  def DTWSimilarity(self, dataX, dataY):
    '''
    Provide the loaded dataFiles, then this function will extract the accX, accY & accZ for you. Possible extension will be to calculate the alpha, beta and gamma aswell, but disabled due to speed
    Arguments:
      dataX: First data object
      dataY: Second data object
    '''
    self.dataX = dataX
    self.dataY = dataY

    X, path = fastdtw(dataX['accX'], dataY['accX'])
    Y, path = fastdtw(dataX['accY'], dataY['accY'])
    Z, path = fastdtw(dataX['accZ'], dataY['accZ'])

    '''
    Calculate similarity function as written in paper:
    ([11] Akl, A., Feng, C., & Valaee, S. (2011). A novel accelerometer-based gesture recognition system. IEEE Transactions on Signal Processing, 59(12), 6197-6205.
    ISO 690)
    '''
    return -1 * ((X**2) + (Y**2) + (Z**2))
    
  def normalize(self, dataObject):
    '''
    Normalizes the data using SciKit methods. (sklearn.preprocessing.normalize)
    Arguments:
      data: data object to be normalized (will return a deep copy)
    '''
    data = dataObject.copy() #make sure to create a copy, otherwise the same object will just be altered!!
    data['accX'] = skNorm([data['accX']])[0] #took me hours to figure out why indexes weren't correct. Never forget the [0]
    data['accX'] = skNorm([data['accX']])[0]
    data['accY'] = skNorm([data['accY']])[0]
    data['accZ'] = skNorm([data['accZ']])[0]
    data['alpha'] = skNorm([data['alpha']])[0]
    data['beta'] = skNorm([data['beta']])[0]
    data['gamma'] = skNorm([data['gamma']])[0]
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
