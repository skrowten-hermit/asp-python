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
P3-1: Sinusoidal tracking using sinusoidal model

This program implements additive synthesis using sinusoidal model.

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
import sineModel as SM

inputFile = stpath + '/sounds/oboe-A4.wav'
window_type = 'hamming'
M = 501
N = 512
t = -20
minSineDur = 0.1
maxnSines = 20
freqDevOffset = 10
freqDevSlope = 0.001
H = 200

fs, x = UF.wavread(inputFile)
w = get_window(window_type, M)
tfreq, tmag, tphase = SM.sineModelAnal(x, fs, w, N, H, t, maxnSines, minSineDur, freqDevOffset, freqDevSlope)

numFrames = int(tfreq[:, 0].size)
frmTime = H * np.arange((numFrames)/float(fs))
tfreq[tfreq <= 0] = np.nan

plt.plot(frmTime, tfreq)
plt.show()
