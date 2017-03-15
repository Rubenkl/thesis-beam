import numpy as np
from scipy import fftpack


  
class DataAnalyzer(object):

  def __init__(self, data, samplingRate = 1000/50):
    self.data = data
    self.samplingRate = samplingRate

  def estimated_autocorrelation(self, x):
    n = len(x)
    variance = x.var()
    x = x-x.mean()
    r = np.correlate(x, x, mode = 'full')[-n:]
    #assert N.allclose(r, N.array([(x[:n-k]*x[-(n-k):]).sum() for k in range(n)]))
    result = r/(variance*(np.arange(n, 0, -1)))
    return result

  def getPeriodInfo(self):
    X = fftpack.fft(self.data)
    freqs = fftpack.fftfreq(len(self.data)) * self.samplingRate
    positive_freqs = freqs[np.where(freqs >= 0)]
    magnitudes = X[np.where(freqs > 0)]
    peakIndex = np.argmax(magnitudes)
    BPM = positive_freqs[peakIndex] * 60

    print("[Correlated] Peak: %s Hz, BPM: %s" % (positive_freqs[peakIndex], BPM))
    return {'detectedBPM': BPM, 'detectedFreq': positive_freqs[peakIndex]}


