import numpy as np
from scipy import fftpack
import pandas as pd
import matplotlib.pyplot as plt
import helpers.DataAnalyzer


  
class Visualizer(object):
  def __init__(self, dataObject):
    self.data = dataObject



  def visualizeAll(self, correlated = False):
    '''
    Visualizes all datastreams
    Arguments:
      correlated: set correlated to True if you want to autocorrelate the data before graphing.
    '''
    time = np.linspace(0,10, self.data.shape[0]) # from 0 to 10 seconds with [amount of datapoints] steps

    f, (ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots(6, sharex=True, sharey=True)

    ax1.plot(time, self.data.alpha)
    ax1.set_title('Alpha', y=0.65, size='smaller')
    ax2.plot(time, self.data.beta)
    ax2.set_title('Beta', y=0.65, size='smaller')
    ax3.plot(time, self.data.gamma)
    ax3.set_title('Gamma', y=0.65, size='smaller')
    ax4.plot(time, self.data.accX)
    ax4.set_title("accX", y=0.65, size='smaller')
    ax5.plot(time, self.data.accY)
    ax5.set_title("accY", y=0.65, size='smaller')
    ax6.plot(time, self.data.accZ)
    ax6.set_title("accZ", y=0.65, size='smaller')

    if correlated:
      analyzer = DataAnalyzer.DataAnalyzer(self.data.alpha)
      ax1.plot(time, analyzer.getAutocorrelation())
      analyzer = DataAnalyzer.DataAnalyzer(self.data.beta)
      ax2.plot(time, analyzer.getAutocorrelation())
      analyzer = DataAnalyzer.DataAnalyzer(self.data.gamma)
      ax3.plot(time, analyzer.getAutocorrelation())
      analyzer = DataAnalyzer.DataAnalyzer(self.data.accX)
      ax4.plot(time, analyzer.getAutocorrelation())
      analyzer = DataAnalyzer.DataAnalyzer(self.data.accY)
      ax5.plot(time, analyzer.getAutocorrelation())
      analyzer = DataAnalyzer.DataAnalyzer(self.data.accZ)
      ax6.plot(time, analyzer.getAutocorrelation())

    # Fine-tune figure; make subplots close to each other and hide x ticks for
    # all but bottom plot.
    f.subplots_adjust(hspace=0)
    plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)

    plt.show()


  def visualizeStream(self, dataStream, correlated=False, title='Data', vLine = None):
    '''Visualizes a particular datastream
      Arguments
        data: single datastream
        title: [optional]
    '''

    time = np.linspace(0,10,dataStream.shape[0])
    f, ax1 = plt.subplots(1)
    ax1.plot(time, dataStream)
    ax1.set_title(title)
    if correlated:
      analyzer = DataAnalyzer.DataAnalyzer(dataStream)
      ax1.plot(time, analyzer.getAutocorrelation())

    if (vLine):
      plt.axvline(vLine)
    plt.show()

  def visualizeFFT(self, fft, positive_freqs, title = 'FFT', Fs = 1000/50):
    '''
    Visualizes the Fourier transformed data.

    Arguments:
      fft: fourier transformed data. ex: fftdata.fft(data)
      positive_freqs: positive frequencies that were derived
      Fs: Sampling rate. Default = 20Hz (1000/50)
    '''
    fig, ax = plt.subplots()
    ax.set_title(title)
    ax.stem(positive_freqs, np.abs(fft[:positive_freqs.size])) # was: X[:N//2]
    ax.set_xlabel('Frequency in Hertz [Hz]')
    ax.set_ylabel('Frequency Domain (Spectrum) Magnitude')
    ax.set_xlim(0, Fs / 2)
    plt.show()