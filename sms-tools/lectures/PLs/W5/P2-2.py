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
P2-2: Sinusoidal analysis using genspecsines

This program implements additive synthesis using sinusoidal model by genspeclines.

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

fs = 44100
Ns = 512 # FFT Size
ipfreq = np.array([4000.0]) # Sinewave at 4000 Hz
ipmag = np.array([0.0]) # Magnitude of 0 dB
ipphase = np.array([0.0]) # Phase 0
Y = UF.genSpecSines_p(ipfreq, ipmag, ipphase, Ns, fs) # Generates a spectrum according to the frequency, magnitude and phase
absY = abs(Y[:Ns/2])
absY[absY < np.finfo(float).eps] = np.finfo(float).eps

freqaxis = fs * np.arange(((Ns/2) + 1)/(float(Ns)))
plt.plot(freqaxis, 20 * np.log10(absY))
plt.show()
