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
P1-1: STFT Analysis of a sound file

This program implements STFT analysis of a sound file.

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
import stft as STFT

inputFile = stpath + '/sounds/piano.wav'
window_type = 'hamming'
M = 801
N = 1024
H = 400

# Returns a frequency and an array of floating point values (from wave file)
(fs, x) = UF.wavread(stpath + '/sounds/piano.wav')
print fs, x

w = get_window(window_type, M)
mX, pX = STFT.stftAnal(x, fs, w, N, H)

plt.plot(np.arange(0, fs / 2, fs / float(N), mX - max(mX)))
plt.show()
