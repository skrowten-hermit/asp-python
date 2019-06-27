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
P2-3: Sinusoidal analysis-synthesis of sinusoid using genspeclines

This program implements additive synthesis of a sinusoid using sinusoidal model by genspeclines.

"""



cwd = os.getcwd()
dtree = cwd.split('/')
ltree = len(dtree)
lroot = ltree - 3
stpath =""
stpath = '/'.join(dtree[:lroot])
modpath = stpath + '/software/models/'
sys.path.append(modpath)


import utilFunctions as UF

fs = 44100
Ns = 512
hNs = Ns / 2
H = Ns / 4
ipfreq = np.array([4000.0])
ipmag = np.array([0.0])
ipphase = np.array([0.0])
Y = UF.genSpecSines_p(ipfreq, ipmag, ipphase, Ns, fs)
y = np.real(ifft(Y)) # Apply the inverse FFT

# The following undoes the Blackman-Harris window and applies the triangular window instead
# because in order to have a good overlap (of about 25%) with a bigger hop size, we need to have
# a composite window with a triangular/Blackman-Harris (triangular divided by Blackman-Harris)
# window.
sw = np.zeros(Ns) # The synthesis window initialization
ow = triang(Ns/2) # The reduction of triangle window size to half the window size
sw[hNs - H:hNs + H] = ow
bh = blackmanharris(Ns)
bh = bh / sum(bh)
sw[hNs - H:hNs + H] = sw[hNs - H:hNs + H] / bh[hNs - H:hNs + H]  # The final synthesis window calculated as the triangular window function divided by Blackman-Harris window function

# The following multiplies the inverse FFT obtained above with the synthesis window.
yw = np.zeros(Ns)
yw[:hNs - 1] = y[hNs + 1:]
yw[hNs - 1:] = y[:hNs + 1]
yw *= sw

# Plot complex spectrum of the sinusoid (magnitude spectrum with both the +ve side and -ve side of the sinusoid).
# plt.plot(abs(Y))

# Plot the complex spectrum of the sinusoid with x-axis in Hz.
freqaxis = fs * np.arange(Ns)/(float(Ns))
# freqaxis = fs * np.arange(-Ns/2, Ns/2)/(float(Ns))
# plt.plot(freqaxis, abs(Y))

# mYdB = 20 * np.log10(abs(Y))
# freqaxis = fs * np.arange(((Ns/2) + 1)/(float(Ns)))
# plt.plot(freqaxis, mYdB)

# Plotting the Blackman-Harris window sinusoid in time-domain centred around 0 (second half of the
# window is in the beginning and the first half is in the end). Since the window size M and the FFT
# size Ns are the same, there is no zero padding done and there is no zero phase here.
# plt.plot(y)

# Plotting the synthesis window applied sinusoid (which we would like to use in the overlap step),
# where we have divided by the Blackman-Harris window and multiply by the half-length triangle
# window (original size was 512, it's now reduced to 256). We would be able to overlap to about
# half of this window size i.e, by 128 samples.
plt.plot(yw)
plt.show()
