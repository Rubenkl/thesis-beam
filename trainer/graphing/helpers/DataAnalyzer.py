import numpy as np
from scipy import fftpack


  
class DataAnalyzer(object):
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
    return {'positive_freqs': self.positive_freqs, 'magnitudes': self.magnitudes}


  def getPeriods(self, amount, startIndex = 0):
    '''Returns the specified data of an amount of periods regarding to the calculated dominating FFT frequency
      Arguments:
        amount: how many periods should be returned
        startIndex: period number that is being started from. (should probably be a fixed number)
    '''

    dataPointsLength = int(self.samplingRate / self.detectedFreq)
    startIndex = dataPointsLength * startIndex

    time = np.linspace(0,(1/self.detectedFreq) * amount, dataPointsLength * amount) # [AMOUNT] times a period (dataPointsLength)
    dataPoints = self.data[startIndex: startIndex + dataPointsLength * amount] # same

    return {'time': time, 'data': dataPoints}
