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
P1-1: Peak detection

This program implements detection of spectral peak. We're considering sinusoids in the frequency domain
in the Sinusoidal Model. More specifically, we're considering that a sinusoid is a spectral peak from 
which we can measure the values of the sinusoid. This code exactly that using the equation of the peak
that was studied in theory to measure the frequency, amplitude and phase of a sinusoid using parabolic
interpolation.

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
import stft as STFT

inputFile = stpath + '/sounds/sine-440.wav'
# inputFile = stpath + '/sounds/piano.wav'

# Returns a frequency and an array of floating point values (from wave file)
(fs, x) = UF.wavread(inputFile)
print fs, x

# With this code, we can analyze a spectrum of a sound and identify the spectral peak locations that
# are within the spectrum. If the sound is more complex than a sine wave and has a lower threshold,
# it will find multiple peaks.

window_type = 'hamming'
M = 501 # Window size
N = 2048 # FFT size - greater the size, better the resolution. This affects the inter-sample spacing and the local maxima.
t = -10 # The magnitude threshold
w = get_window(window_type, M)
s1 = .8 * fs
s2 = (.8 * fs) + M
print s1, s2
x1 = x[int(0.8 * fs):int((0.8 * fs)) + M] # Reading the sound file to get M samples from somewhere middle in the sample space
# x1 = x[int(0.5 * fs):int((0.5 * fs)) + M]
mX1, pX1 = DFT.dftAnal(x1, w, N) # Computing the spectrum using the function from dftmodel
ploc = UF.peakDetection(mX1, t) # Computation of the peak using peakDetection() function in utility functions utilFunctions
pmag = mX1[ploc] # To get the magnitude of the location where peak exists
iploc, ipmag, ipphase = UF.peakInterp(mX1, pX1, ploc) # To get a more accurate peak location, magnitude and phase

# This part prepares for the plot by converting the x-axis to Hz, and combining the magnitude
# spectrum with the peak marked with a demarcation.

# freqaxis = fs * np.arange((N/2))/(float(N)) # This gets only an even number of x-axis values expressed in Hz for plotting
freqaxis = fs * np.arange(((N/2) + 1))/(float(N)) # This gets an odd number of x-axis values expressed in Hz for plotting
print freqaxis
plt.plot(freqaxis, mX1)
# plt.plot(freqaxis)
# plt.show()
# plt.plot(mX1)
# plt.show()
# plt.plot(fs * ploc / float(N), pmag, marker='x', linestyle='') # Adds a marker to the peak to demarcate using peakDetection() function
plt.plot(fs * iploc / float(N), ipmag, marker='x', linestyle='') # Adds a marker to the peak to demarcate using peakInterp() function
plt.show()
