import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as pltx
import matplotlib.pyplot as pltmX
import matplotlib.pyplot as pltpX
import matplotlib.pyplot as pltB
import matplotlib.pyplot as pltmBX
import matplotlib.pyplot as pltpBX
from scipy.signal import get_window
from scipy.signal import blackmanharris, triang
from scipy.fftpack import fft, ifft
import sys, os, math

"""
P2-4: Sinusoidal analysis and synthesis using genspeclines

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


inputFile = stpath + '/sounds/piano.wav'

# Returns a frequency and an array of floating point values (from wave file)
(fs, x) = UF.wavread(inputFile)
print fs, x

Ns = 512
hNs = Ns / 2
H = Ns / 4
M = 511
t = -70
window_type = 'hamming'
w = get_window(window_type, M)
x1 = x[.8 * fs:(.8 * fs) + M]
mX1, pX1 = DFT.dftAnal(x1, w, N)
ploc = UF.peakDetection(mX1, t)
pmag = mX1[ploc]
iploc, ipmag, ipphase = UF.peakInterp(mX1, pX1, ploc)
ipfreq = fs * iploc / float(Ns)
Y = UF.genSpecSines_p(ipfreq, ipmag, ipphase, Ns, fs)
y = np.real(ifft(Y))

sw = np.zeros(Ns)
ow = triang(Ns/2)
sw[hNs - H:hNs + H] = ow
bh = blackmanharris(Ns)
bh = bh / sum(bh)
sw[hNs - H:hNs + H] = sw[hNs - H:hNs + H] / bh[hNs - H:hNs + H]

yw = np.zeros(Ns)
yw[:hNs - 1] = y[hNs + 1:]
yw[hNs - 1:] = y[:hNs + 1]
yw *= sw

freqaxis = fs * np.arange(((Ns/2) + 1)/(float(Ns)))
plt.plot(freqaxis, mX1)
plt.plot(fs * iploc / Ns, ipmag, marker = 'x', linestyle = '')
plt.show()
