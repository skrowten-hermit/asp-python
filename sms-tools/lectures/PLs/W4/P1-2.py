import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as pltx
import matplotlib.pyplot as pltmX
import matplotlib.pyplot as pltpX
import matplotlib.pyplot as pltB
import matplotlib.pyplot as pltmBX
import matplotlib.pyplot as pltpBX
from scipy.signal import get_window
from scipy.fftpack import fft
import sys, os, math

"""
P1-1: Sinusoid Analysis with a window function

This program implements analysis of a sinusoid with a window function (i.e., a sinusoid that has 
been windowed) using DFT.

"""



cwd = os.getcwd()
dtree = cwd.split('/')
ltree = len(dtree)
lroot = ltree - 3
stpath =""
stpath = '/'.join(dtree[:lroot])
modpath = stpath + '/software/models/'
sys.path.append(modpath)


import dftModel as DFT

# Here we pass the parameters to the 'dftAnal' function - the input signal, the window function
# and the FFT size and it automatically does all the operations and returns the magnitude and
# phase spectrums. Here, we generate a sine wave with a given frequency 'f' as the input signal
# x[n]. Here, we are going to use 'M' as the sample size of the input the window as well as the
# window size.
fs = 44100
f = 5000.0
M = 101
x = np.cos(2 * np.pi * f * np.arange(M) / float(fs))
N = 512
window_type = 'hamming'
w = get_window(window_type, M)
mX, pX = DFT.dftAnal(x, w, N)

# print mX - max(mX)
# print np.arange(0, (fs/2) + 1, fs/float(N))
# print len(mX)
# print len(mX - max(mX))
# print len(np.arange(0, (fs/2) + 1, fs/float(N)))
# sys.exit()

# The 'dftAnal' function only computes the positive part of the spectrum. The following displays
# the plot with frequency in hertz. In the resulting plot, the central lobe that is visible is
# that of the window used. 'xHz' displays the frequency values in Hz and 'mX_0' is a normalized
# variation of 'mX' so that the peak is 0 dB. The important thing to notice and understand is
# that during the analysis of a sine wave multiplied by a given window, the resultant spectrum
# shows that the transform of the window (the peak or the main lobe) always points to the
# frequency of the sinusoid.
xHz = np.arange(0, (fs/2) + 1, fs/float(N))
mX_0 = mX - max(mX)
plt.plot(xHz, mX_0)
plt.show()
