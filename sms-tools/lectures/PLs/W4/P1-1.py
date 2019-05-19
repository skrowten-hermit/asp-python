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
P1-1: Window Analysis

This program implements analysis of a window function using DFT.

"""



M = 63
window = get_window('hamming', M) # Generates a smoothing window
hM1 = int(math.floor((M + 1)) / 2)
hM2 = int(math.floor(M / 2))

N = 512
hN = N / 2
fftbuffer = np.zeros(N)
fftbuffer[:hM1] = window[hM2:]
fftbuffer[N - hM2:] = window[:hM2]

X = fft(fftbuffer)
absX = abs(X)
absX[absX < np.finfo(float).eps] = np.finfo(float).eps
mX = 20 * np.log10(absX)
pX = np.angle(X)

mX1 = np.zeros(N)
pX1 = np.zeros(N)
mX1[:hN] = mX[hN:]
mX1[N - hN:] = mX[:hN]
pX1[:hN] = pX[hN:]
pX1[N - hN:] = pX[:hN]




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
plt.show()
