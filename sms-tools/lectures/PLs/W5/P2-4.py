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
P2-4: Sinusoidal analysis-synthesis of real sound using genspeclines

This program implements additive synthesis of a real sound using sinusoidal model using genspeclines.

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


inputFile = stpath + '/sounds/oboe-A4.wav'

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
n = int(0.8 * fs)
print n
x1 = x[n:n + M]
mX1, pX1 = DFT.dftAnal(x1, w, Ns) # DFT analysis
ploc = UF.peakDetection(mX1, t) # Peak detection
pmag = mX1[ploc]
iploc, ipmag, ipphase = UF.peakInterp(mX1, pX1, ploc) # Using interpolation to get more accurate value of the location of peaks in the sinusoid
ipfreq = fs * iploc / float(Ns)
Y = UF.genSpecSines_p(ipfreq, ipmag, ipphase, Ns, fs) # Synthesis in frequency domain
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

# Plots the spectrum with peaks detected. If there is no zero-padding and the size of FFT is small,
# the effect of parabolic interpolation will be significant and substantial and the peak detection
# may be wayward.
# freqaxis = fs * np.arange((Ns/2) + 1)/(float(Ns))
# plt.plot(freqaxis, mX1)
# plt.plot(fs * iploc / Ns, ipmag, marker = 'x', linestyle = '')

plt.plot(y)
# plt.plot(yw)
plt.show()
