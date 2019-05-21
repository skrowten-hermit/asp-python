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
P2-1: Detection of fundamental frequency f0

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
import sineModel as SM
import harmonicModel as HM

inputFile = stpath + '/sounds/vignesh.wav'
window_type = 'blackman'
M = 1201
N = 2048
t = -90
minSineDur = 0.1
nH = 50
minf0 = 130
maxf0 = 300
f0et = 5
harmDevSlope = 0.1
Ns = 512
H = 128

fs, x = UF.wavread(inputFile)
w = get_window(window_type, M)

hfreq, hmag, hphase = HM.harmonicModelAnal(x, fs, w, N, H, t, nH, minf0, maxf0, f0et, harmDevSlope, minSineDur)

numFrames = int(hfreq[:, 0].size)
frmTime = H * np.arange(numFrames) / float(fs)
hfreq[hfreq <= 0] = np.nan

plt.plot(frmTime, hfreq)
plt.show()
