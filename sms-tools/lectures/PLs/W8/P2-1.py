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
P2-1: Analysis and synthesis using sine transformations

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
import sineTransformations as ST

inputFile = stpath + '/sounds/piano.wav'
window_type = 'hamming'
M = 1001
N = 2048
t = -100
minSineDur = 0.01
maxnSines = 150
freqDevOffset = 30
freqDevSlope = 0.02
H = 200
Ns = 512

fs, x = UF.wavread(inputFile)
w = get_window(window_type, M)

tfreq, tmag, tphase = SM.sineModelAnal(x, fs, w, N, H, t, maxnSines, minSineDur, freqDevOffset, freqDevSlope)
y = SM.sineModelSynth(tfreq, tmag, np.array([]), Ns, H, fs)
UF.wavwrite(y, fs, 'output.wav')
