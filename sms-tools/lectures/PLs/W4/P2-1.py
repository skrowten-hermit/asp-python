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
P1-1: STFT Analysis/Synthesis of a sound file

This program implements a whole STFT system for a sound file. We need to iterate over a sound x[n]
and computing at every frame 'l'. We'll be computing frames of the sound at each frame location and
multiplying the fragment of the sound with a window, 'w'. This way, we'll be having a sequence of 
spectra, more specifically in this case, a complex spectra. This whole process can be undone by 
using the inverse FFT. The inverse FFT gives us the output y[n] multiplied by window function w[n]
as yw[n]. Then, we'll use a technique called "Overlap-add strategy" to add together all the 
fragments together into a whole output signal y[n]. If we choose the window and hop size correctly,
y[n] would be identical to x[n].

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
import stft as STFT

inputFile = stpath + '/sounds/piano.wav'
window_type = 'hamming'
M = 801
N = 1024
H = 400

# Returns a frequency and an array of floating point values (from wave file)
(fs, x) = UF.wavread(inputFile)
print fs, x

w = get_window(window_type, M)

# The output array of magnitude spectrum, 'mX' and the output array of phase spectrum, 'pX' are
# very large variables/arrays. They're very big matrices of values. So, mX.shape or pX.shape will
# tell the actual dimensions of the array i.e., the number of frames and the number of samples in
# the spectrum in the format (x, y) where 'x' is the number of frames and 'y' is the number of
# samples. Here, each of the 'x' frames have 'y' samples. Since we use half of the FFT size, the
# array returns half of 'N' as the sample numbers. We can access any individual frame 'n' using the
# notation mX[n, :] or pX[n, :]. The function 'pcolormesh' plots the matrix as a 3D shape. The plot
# is a bit different from other plots because the vertical axis or the y-axis is the time and the
# horizontal axis or the x-axis is the frequency. So, we can transpose the matrix using 'transpose'
# function first to plot the time on x-axis and the frequency on y-axis.
mX, pX = STFT.stftAnal(x, fs, w, N, H)

plt.plot(x)
plt.show()
plt.plot(w)
plt.show()
plt.plot(mX[50, :])
plt.show()
plt.pcolormesh(mX)
plt.show()
plt.pcolormesh(np.transpose(mX))
plt.show()
