import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as pltx
import matplotlib.pyplot as pltmX
import matplotlib.pyplot as pltpX
import matplotlib.pyplot as pltB
import matplotlib.pyplot as pltmBX
import matplotlib.pyplot as pltpBX
from scipy.signal import get_window, resample
from scipy.fftpack import fft, ifft
import sys, os, math

"""
P1-2: Analysis of sound using stochastic model

This program implements analysis of a window function using DFT.

"""



cwd = os.getcwd()
dtree = cwd.split('/')
ltree = len(dtree)
lroot = ltree - 3
stpath = ""
stpath = '/'.join(dtree[:lroot])
modpath = stpath + '/software/models/'
sys.path.append(modpath)


import utilFunctions as UF

inputFile = stpath + '/sounds/ocean.wav'
fs, x = UF.wavread(inputFile)
M = N = 256
stocf = 0.2
window_type = 'hamming'
w = get_window(window_type, M)
xw = x[10000:10000 + M]
X = fft(xw)
mX = 20 * np.log10(abs(X[:N/2]))
mXenv = resample(np.maximum(-200, mX), mX.size * stocf)

mY = resample(mXenv, N/2)
pY = 2 * np.pi * np.random.rand(N/2)
Y = np.zeros(N, dtype=complex)
Y[:N/2] = 10 ** (mY/20) * np.exp(-1j * pY[:0:-1])
y = np.real(ifft(Y))
