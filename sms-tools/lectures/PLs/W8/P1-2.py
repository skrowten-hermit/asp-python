import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as pltx
import matplotlib.pyplot as pltmX
import matplotlib.pyplot as pltpX
import matplotlib.pyplot as pltB
import matplotlib.pyplot as pltmBX
import matplotlib.pyplot as pltpBX
from scipy.signal import get_window, resample
from scipy.fftpack import fft
import sys, os, math

"""
P1-2: STFT transformations - morphing two sounds

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
import dftModel as DFT
import harmonicModel as HM

M = N = 512
inputFile1 = stpath + '/sounds/rain.wav'
inputFile2 = stpath + '/sounds/soprano-E4.wav'
fs1, x1 = UF.wavread(inputFile1)
fs2, x2 = UF.wavread(inputFile2)
window_type = 'hanning'
w = get_window(window_type, M)
x1w = x1[10000:10000 + M] * w
x2w = x2[10000:10000 + M] * w

mX1, pX1 = DFT.dftAnal(x1w, w, N)
mX2, pX2 = DFT.dftAnal(x2w, w, N)

smoothf = 0.2
mX2smooth1 = resample(np.maximum(-200, mX2), mX2.size * smoothf)
mX2smooth2 = resample(mX2smooth1, N / 2)

balancef = 0.7
mY = balancef * mX2smooth2 + (1 - balancef) * mX1

y = DFT.dftSynth(mY, pX1, N)
