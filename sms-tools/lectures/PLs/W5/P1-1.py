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
P1-1: Peak detection

This program implements detection of spectral peak.

"""




cwd = os.getcwd()
dtree = cwd.split('/')
ltree = len(dtree)
lroot = ltree - 3
stpath =""
stpath = '/'.join(dtree[:lroot])
modpath = stpath + '/software/models/'
sys.path.append(modpath)


import utilFunctions as UF
import dftModel as DFT
import stft as STFT

inputFile = stpath + '/sounds/piano.wav'

# Returns a frequency and an array of floating point values (from wave file)
(fs, x) = UF.wavread(stpath + '/sounds/piano.wav')
print fs, x

window_type = 'hamming'
M = 501
N = 512
t = -20
w = get_window(window_type, M)
x1 = x[.8 * fs:(.8 * fs) + M]
mX1, pX1 = DFT.dftAnal(x1, w, N)
ploc = UF.peakDetection(mX1, t)
pmag = mX1[ploc]

freqaxis = fs * np.arange(((N/2) + 1)/(float(N)))
plt.plot(freqaxis, mX1)
plt.plot(fs * ploc / float(N), pmag, marker = 'x', linestyle = '')
plt.show()
