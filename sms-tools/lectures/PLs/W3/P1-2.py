import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as pltx
import matplotlib.pyplot as pltmX
import matplotlib.pyplot as pltpX
import matplotlib.pyplot as pltB
import matplotlib.pyplot as pltmBX
import matplotlib.pyplot as pltpBX
from scipy.signal import triang
from scipy.fftpack import fft
import sys, os, math

"""
P1-2: DFT properties using a real-world signal like a sound file.

This program explores the concepts of symmetry, zero-phase windowing, zero padding, dB scale
and phase unwrapping using a fragment of a sound signal.

"""

# wdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../software/models/')
cwd = os.getcwd()
dtree = cwd.split('/')
ltree = len(dtree)
lroot = ltree - 3
stpath = ""
stpath = '/'.join(dtree[:lroot])
modpath = stpath + '/software/models/'
sys.path.append(modpath)

import utilFunctions as UF

M = 501
# 'math.floor' is used to split odd and even numbered sample size into 2 portions.
hM1 = int(math.floor((M + 1)/2))
hM2 = int(math.floor((M/2)))

inputFile = stpath + '/sounds/soprano-E4.wav'
print hM1, hM2
(fs, x) = UF.wavread(inputFile)
print fs, x

# We are going to take only a fragment of the wave file, equal to the window size M from the
# sound file, and apply a smoothing window. So, the resultant signal is a short signal of
# M samples. The plot of the original file, whose samples are stored in 'x' shows amplitude
# normalized to values between -1 and 1. We'll select a particular sample to select the
# window's starting position and from there we'll select consecutive 'M' samples. Then, we
# can multiply it with a smoothing window.
start_sample = 5000
x0 = x[start_sample:start_sample+M]
x1 = x[start_sample:start_sample+M] * np.hamming(M)


# fig, (ax1, ax2) = plt.subplots(2, 1, sharex=False, sharey=False)
# fig.suptitle('Comparing original sound signal with signal with applied smoothing window')
# fig.subplots_adjust(hspace=0.4, wspace=0.4)
# ax1.plot(x0, 'tab:blue')
# ax1.tick_params(axis='both', which='both', labelsize=7)
# ax1.set_xlabel('time')
# ax1.set_ylabel('amplitude (actual)')
# ax2.plot(x1, 'tab:red')
# ax2.tick_params(axis='both', which='both', labelsize=7)
# ax2.set_xlabel('time (shifted)')
# ax2.set_ylabel('amplitude (smoothed : hamming)')
#
# plt.show()

X0 = fft(x0)
mX0 = abs(X0)
pX0 = np.angle(X0)

X1 = fft(x1)
mX1 = abs(X1)
pX1 = np.angle(X1)

# N = 511
N = 1024

fftbuffer = np.zeros(N)
fftbuffer[:hM1] = x1[hM2:]
fftbuffer[N - hM2:] = x1[:hM2]

BX = fft(fftbuffer)
# mBX = abs(BX)
mBX = 20 * np.log10(abs(BX)) # magnitude spectrum in dB
mBX = mBX[0:512]
# pBX = np.angle(BX)
# pBX = np.unwrap(np.angle(BX))
pBX = np.unwrap(np.angle(BX))

# We have 3 plots - the original signal's window x0, the smoothed (from x0) window x1 and
# the shifted window (from x), 'fftbuffer'. All these signals have an amplitude normalized
# to a value between -1 and 1. In case of 'fftbuffer', it is the same as x1 but is shifted
# and plotted in a way that it's centred around zero, which means that the second half of
# the signal is in positive time (horizontal axis, x-axis) and the first half of the signal
# is in negative time (horizontal axis, x-axis). This is called zero-phase windowing.
# The magnitude spectrum shows the symmetry we have seen before with the positive part at
# the beginning and the negative part at the end. We need only half of the N samples because
# of the symmetry the other half is kind of redundant. The phase spectrum does look a
# bit noisy, it's anti-symmetric or shows odd symmetry because of which the first half is
# the negative values of the second half.
# In case of the FFT, the general rule is to take an integer that's a power of 2 (the FFT
# size N and the sample size M are independent of each other). If we raise the value of N
# to any nearest power of 2, such that N > M, we can see that the middle part of the plot
# of 'fftbuffer' is all zeroes - this is called zero padding, which adds zeroes to fill up
# the FFT size. Examining the magnitude spectrum of such a plot shows a similar plot but
# with more number of samples now. In order to get a clearer detailed information, we can
# plot the magnitude spectrum in dB (by using a logarithmic scale, 20 * log10(mX). This
# results in the vertical axis changing a lot giving a detailed information. Because of
# the presence of symmetry only half of the spectrum needs to be plotted. And if we take
# a look at the phase spectrum (it displays odd symmetry), in order to help visualize
# better, we'll use the phase 'unwrap' function, from numpy. After applying the unwrap
# function, the phase spectrum would reveal more details. Here too, because of anti-symmetry,
# we only need the first half of the spectrum. The 'unwrap' function does the pi-2pi
# unwrappingand makes the plot look smoother.
fig, ((ax1, ax2, ax3), (ax4, ax5, ax6), (ax7, ax8, ax9)) = plt.subplots(3, 3, sharex=False, sharey=False)
fig.suptitle('Comparing sound signal plots', fontsize=20)
fig.subplots_adjust(hspace=0.4, wspace=0.4)
ax1.plot(x0, 'tab:blue')
ax1.tick_params(axis='both', which='both', labelsize=7)
ax1.set_xlabel('sample number')
ax1.set_ylabel('amplitude')
ax1.set_title('x0 (soprano sample)', fontsize=14)
ax2.plot(x1, 'tab:red')
ax2.tick_params(axis='both', which='both', labelsize=7)
ax2.set_xlabel('sample number')
ax2.set_ylabel('amplitude')
ax2.set_title('x1 (smoothed x0)', fontsize=14)
ax3.plot(fftbuffer, 'tab:orange')
ax3.tick_params(axis='both', which='both', labelsize=7)
ax3.set_xlabel('sample number')
ax3.set_ylabel('amplitude')
ax3.set_title('fftbuffer (zero-phase windowed x1)', fontsize=14)
ax4.plot(mX0, 'tab:blue')
ax4.tick_params(axis='both', which='both', labelsize=7)
ax4.set_xlabel('frequency')
ax4.set_ylabel('magnitude')
ax5.plot(mX1, 'tab:red')
ax5.tick_params(axis='both', which='both', labelsize=7)
ax5.set_xlabel('frequency')
ax5.set_ylabel('magnitude')
ax6.plot(mBX, 'tab:orange')
ax6.tick_params(axis='both', which='both', labelsize=7)
ax6.set_xlabel('frequency')
ax6.set_ylabel('magnitude (in dB)')
ax7.plot(pX0, 'tab:blue')
ax7.tick_params(axis='both', which='both', labelsize=7)
ax7.set_xlabel('frequency')
ax7.set_ylabel('phase')
ax8.plot(pX1, 'tab:red')
ax8.tick_params(axis='both', which='both', labelsize=7)
ax8.set_xlabel('frequency')
ax8.set_ylabel('phase')
ax9.plot(pBX, 'tab:orange')
ax9.tick_params(axis='both', which='both', labelsize=7)
ax9.set_xlabel('frequency')
ax9.set_ylabel('phase')

mng = plt.get_current_fig_manager()
mng.resize(*mng.window.maxsize())
# print mng.window.maxsize()
plt.show()