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

This program implements analysis of a sinusoid with a window function using DFT.

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

fs = 44100
f = 5000.0
M = 101
x = np.cos(2 * np.pi * f * np.arange(M) / float(fs))
N = 512
w = get_window('hanning', M)
mX, pX = DFT.dftAnal(x, w, N)

plt.plot(np.arange(0, fs / 2, fs / float(N), mX - max(mX)))
plt.show()
