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
P2-1: DFT Model

This program implements analysis-synthesis using DFT i.e, it constructs a model where from a
fragment of sound x[n], performs the FFT algorithm and then generates magnitude and phase 
spectrum (analysis), which would again be used as the input to the inverse FFT algorithm and
returns another fragment of sound as the output which is identical to the input fragment of 
sound x[n].

"""

# wdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../software/models/')
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


(fs, x) = UF.wavread(stpath + '/sounds/piano.wav')
print fs, x

M = 501
w = get_window('hamming', M)

time = 0.2
x1 = x[int(time*fs):int(time*fs)+M]


N = 1024
mX, pX = DFT.dftAnal(x1, w, N)
y = DFT.dftSynth(mX, pX, w.size) * sum(w)