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
P2-1: HPS model

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

inputFile = stpath + '/sounds/oboe-A4.wav'
fs, x = UF.wavread(inputFile)
pin = 40000
M = 801
N = 2048
t = -80
minf0 = 300
maxf0 = 500
f0et = 5
nH = 60
harmDevSlope = 0.001
stocf = 0.4

window_type = 'blackman'
w = get_window(window_type, M)
hM1 = int(math.floor((M + 1) / 2))
hM2 = int(math.floor(M / 2))

x1 = x[pin - hM1:pin + hM2]
mX1, pX1 = DFT.dftAnal(x1, w, N)
ploc = UF.peakDetection(mX1, t)
iploc, ipmag, ipphase = UF.peakInterp(mX1, pX1, ploc)
ipfreq = fs * iploc / N
f0 = UF.f0Twm(ipfreq, ipmag, f0et, minf0, maxf0, 0)
hfreq, hmag, hphase = HM.harmonicDetection(ipfreq, ipmag, ipphase, f0, nH, [], fs, harmDevSlope)

Ns = 512
hNs = 256
Yh = UF.genspecSines(hfreq, hmag, Ns, fs)

wr = get_window('blackmanharris', Ns)
xw2 = x[pin - hNs -1: pin + hNs -1] * wr / sum(wr)
fftbuffer = np.zeros(Ns)
fftbuffer[:hNs] = xw2[hNs:]
fftbuffer[hNs:] = xw2[:hNs]
X2 = fft(fftbuffer)
Xr = X2 - Yh

mXr = 20 * np.log10(abs(Xr[:hNs]))
mXrenv = resample(np.maximum(-200, mXr), mXr.size * stocf)
stocEnv = resample(mXrenv, hNs)
