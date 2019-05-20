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
P1-3: Detection of fundamental frequency f0

This program implements analysis of a window function using DFT.

"""



M = 63 # Window length/size.
# Generates a smoothing window of type 'hanning', a raised cosine function.
window = get_window('hanning', M)
# plt.plot(window)
# plt.show()

# The following variables store the middle of the window information, irrespective of whether
# the window size is an even or odd number.
hM1 = int(math.floor((M + 1)) / 2)
hM2 = int(math.floor(M / 2))

# The following section prepares the window for computing the FFT. In order to do that, we
# need to do zero-phase windowing - place the window at the zeroth location (shift and plot in
# a way that it's centred around zero). So, we create a buffer 'fftbuffer' of the size of the
# FFT and we place the window around the zeroth sample by splitting the samples into two halves
# and shifting the second half to the left side (the beginning of the new buffer) and the first
# half to the right side (the end of the new buffer). The spectrum is calculated on the data of
# this resulting buffer called 'fftbuffer'.
N = 512
hN = N / 2 # 'hN' version 1.0
# hN = (N / 2) + 1 # 'hN' version 2.0
fftbuffer = np.zeros(N)
fftbuffer[:hM1] = window[hM2:]
fftbuffer[N - hM2:] = window[:hM2]
# plt.plot(fftbuffer)
# plt.show()

# To plot the magnitude spectrum in 'dB', we need to make sure that there are no zeroes in the
# absolute value of the result of FFT operation on 'fftbuffer'. This is because for calculating
# the magnitude in 'dB', we take the logarithm and 'log(0)' is "UNDEFINED". This is done by
# checking if the absolute value is less than epsilon value, the minimum representable value in
# python, which has to be zero (magnitude is always positive) or thereabouts and if any such
# value is found, proceed by replacing it with epsilon value. This way undefined values can be
# avoided. It is to be noted that the first part of magnitude spectrum will have +ve frequency
# values and the second part will have negative frequency values.
X = fft(fftbuffer)
absX = abs(X)
# plt.plot(absX)
# plt.show()
absX[absX < np.finfo(float).eps] = np.finfo(float).eps
# plt.plot(absX)
# plt.show()
mX = 20 * np.log10(absX)
plt.plot(mX)
plt.show()
pX = np.angle(X)
plt.plot(pX)
plt.show()

# The following part nullifies/reverses/undo's the zero-phase windowing operation done earlier in
# 'fftbuffer' in order to make the data easier to visualize. This 'mX1' is a better way display
# (by moving the main lobe to the center) the magnitude spectrum. In the phase spectrum, the most
# important observation is the phases in the middle. Though we have (2 * pi) discontinuities, it
# can be deduced as having a value zero at every point.
mX1 = np.zeros(N)
pX1 = np.zeros(N)
mX1[:hN] = mX[hN:] # For 'hN' version 1.0
mX1[hN:] = mX[:hN] # For 'hN' version 1.0
# mX1[:hN] = mX[N - hN:] # For 'hN' version 2.0
# mX1[N - hN:] = mX[:hN] # For 'hN' version 2.0
plt.plot(mX1)
plt.show()
pX1[:hN] = pX[hN:] # For 'hN' version 1.0
pX1[hN:] = pX[:hN] # For 'hN' version 1.0
# pX1[:hN] = pX[N - hN:] # For 'hN' version 2.0
# pX1[N - hN:] = pX[:hN] # For 'hN' version 2.0
plt.plot(pX1)
plt.show()

# The following allow us to visualize the x-axis of the magnitude spectrum better. Basically, we
# have normalized the horizontal axis (x-axis) by dividing by N and multiplying by M so that we
# actually see the samples with respect to the window. Also, the magnitude is normalized so that
# the maximum value is 0 dB.
plt.plot(np.arange(-hN, hN) / float(N) * M, mX1 - max(mX1))
plt.axis([-20, 20, -80, 0])
plt.show()

# plt.plot(x) # Plots the amplitude-sample graph of x[n]
# plt.plot(tx, x) # Plots the amplitude-time graph of x[n] with time in seconds
# plt.plot(tx1, x1) # Plots the amplitude-time graph of x1[n] with time in seconds
# plt.axis([start_time, stop_time, min(x1), max(x1)]) # Makes a tight plot of x1[n]
# plt.plot(w) # Plots the amplitude-sample graph of smoothing window 'w'
# plt.plot(mX1) # Plots the magnitude spectrum of x1[n] (in dB), this plots only the positive side
# plt.show()    # of the spectrum, going from (half of sampling rate) 0 to N/2 (half of FFT size).
# plt.plot(pX1) # Plots the phase spectrum of x1[n], with phase unwrap applied.
# plt.axis([-0.2, 0.9, -0.8, 0.8])
# plt.xlabel("time")
# plt.ylabel("amplitude")
# plt.show()
