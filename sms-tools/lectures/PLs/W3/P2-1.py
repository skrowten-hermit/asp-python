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

inputFile = stpath + '/sounds/piano.wav'
# Returns a frequency and an array of floating point values (from wave file)
(fs, x) = UF.wavread(inputFile)
print fs, x

# Calculates the time array corresponding to the samples (for plotting)
# tx = np.arange(len(x)/float(fs)) # For plotting with the sample numbers at x-axis
nsamplesx = len(x)/float(fs)
tx = np.linspace(0, nsamplesx, len(x))

M = 501
w = get_window('hamming', M) # Generates a smoothing window

# To convert to samples, we start at 'time' second(s) and multiply time with sampling rate 'fs'
# to get the sample at the start of 'time' second(s). Then we select the next 'M" samples to
# get the input signal.
start_time = 0.2
start_sample = start_time * fs
stop_sample = (start_time * fs) + M
x1 = x[int(start_sample):int(stop_sample)]
stop_time = float(stop_sample/fs)
tx1 = np.linspace(start_time, stop_time, M)

# The fragment of sound with the FFT size and the smoothing window is passed to the functions in
# DFT - first to 'dftAnal', the outputs of which is passed to 'dftSynth' to get back the new
# synthesized sound. Note that the ouput of 'dftSynth' is normalized using a normalization factor
# 'sum(w)'. This may not look so intuitive but we need ro apply this particular normalization
# factor in this scenario.
N = 1024
mX1, pX1 = DFT.dftAnal(x1, w, N)
y = DFT.dftSynth(mX1, pX1, w.size) * sum(w)


# plt.plot(x) # Plots the amplitude-sample graph of x[n]
# plt.plot(tx, x) # Plots the amplitude-time graph of x[n] with time in seconds
plt.plot(tx1, x1) # Plots the amplitude-time graph of x1[n] with time in seconds
# plt.axis([start_time, stop_time, min(x1), max(x1)]) # Makes a tight plot of x1[n]
# plt.plot(w) # Plots the amplitude-sample graph of smoothing window 'w'
# plt.plot(mX1) # Plots the magnitude spectrum of x1[n] (in dB), this plots only the positive side
# plt.show()    # of the spectrum, going from (half of sampling rate) 0 to N/2 (half of FFT size).
# plt.plot(pX1) # Plots the phase spectrum of x1[n], with phase unwrap applied.
# plt.axis([-0.2, 0.9, -0.8, 0.8])
# plt.xlabel("time")
# plt.ylabel("amplitude")
plt.show()
