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
import sys, os, math, functools, time

"""
P1-1: Detection of fundamental frequency f0

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
import dftModel as DFT


def TWM_Errors(pfreq, pmag, f0c):
    p = 0.5 # Weighting by frequency value
    q = 1.4 # Weighting related to the magnitude of peaks
    r = 0.5 # Scaling related to the magnitude of peaks
    rho = 0.33 # Weighting of MP error
    Amax = max(pmag) # Maximum peak magnitude
    maxnpeaks = 10 # Maximum number of peaks used
    harmonic = np.matrix(f0c)
    ErrorPM = np.zeros(harmonic.size) # Initializing PM Errors
    MaxNPM = min(maxnpeaks, pfreq.size)

    for i in range(0, MaxNPM): # Predicted to measured mismatch error
        difmatrixPM = harmonic.T * np.ones(pfreq.size)
        difmatrixPM = abs(difmatrixPM - np.ones((harmonic.size, 1)) * pfreq)
        FreqDistance = np.amin(difmatrixPM, axis=1) # Minimum along rows
        peakloc = np.argmin(difmatrixPM, axis=1)
        Ponddif = np.array(FreqDistance) * (np.array(harmonic.T) ** (-p))
        PeakMag = pmag[peakloc]
        MagFactor = 10 ** ((PeakMag - Amax) / 20)
        ErrorPM = ErrorPM + (Ponddif + MagFactor * (q * Ponddif - r)).T
        harmonic = harmonic + f0c

    ErrorMP = np.zeros(harmonic.size) # Initializing MP errors
    MaxNMP = min(maxnpeaks, pfreq.size)

    for i in range(0, f0c.size): # Measured to predicted mismatch error
        nharm = np.round(pfreq[:MaxNMP] / f0c[i])
        nharm = (nharm >= 1) * nharm + (nharm < 1)
        FreqDistance = abs(pfreq[:MaxNMP] - nharm * f0c[i])
        Ponddif = FreqDistance * (pfreq[:MaxNMP] ** (-p))
        PeakMag = pmag[:MaxNMP]
        MagFactor = 10 ** ((PeakMag - Amax) / 20)
        ErrorMP[i] = sum(MagFactor * (Ponddif + MagFactor * (q * Ponddif - r)))

    Error = (ErrorPM[0] / MaxNPM) + (rho * ErrorMP / MaxNMP) # Total error

    return Error


inputFile = stpath + '/sounds/sawtooth-440.wav'
fs, x = UF.wavread(inputFile)
N = 1024
M = 601
t = -60
minf0 = 50
maxf0 = 2000

hN = N/2
hM = (M+1)/2

window_type = 'hamming'
w = get_window(window_type, M)
start = 0.8 * fs

x1 = x[start:start+M]
mX1, pX1 = DFT.dftAnal(x1, w, N)
ploc = UF.peakDetection(mX1, t)
iploc, ipmag, ipphase = UF.peakInterp(mX1, pX1, ploc)
ipfreq = fs * iploc / N
f0c = np.argwhere((ipfreq > minf0) & (ipfreq < maxf0))[:, 0]
f0cf = ipfreq[f0c]
f0Errors = TWM_Errors(ipfreq, ipmag, f0cf)

freqaxis = fs * np.arange(((N/2) + 1)/(float(N)))
plt.plot(freqaxis, mX1)
plt.plot(ipfreq, ipmag, marker = 'x', linestyle = '')
plt.show()
