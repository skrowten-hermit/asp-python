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
mX, pX = STFT.stftAnal(x, fs, w, N, H)

plt.plot(np.arange(0, fs / 2, fs / float(N), mX - max(mX)))
plt.show()
