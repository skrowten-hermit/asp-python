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
P2-3: Sinusoidal synthesis using genspeclines

This program implements additive synthesis using sinusoidal model by genspeclines.

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
y = np.real(ifft(Y))

sw = np.zeros(Ns)
ow = triang(Ns/2)
sw[hNs - H:hNs + H] = ow
bh = blackmanharris(Ns)
bh = bh / sum(bh)
sw[hNs - H:hNs + H] = sw[hNs - H:hNs + H] / bh[hNs - H:hNs + H]

yw = np.zeros(Ns)
yw[:hNs - 1] = y[hNs + 1:]
yw[hNs - 1:] = y[:hNs + 1]
yw *= sw

# freqaxis = fs * np.arange(((Ns/2) + 1)/(float(Ns)))
# plt.plot(freqaxis, 20 * np.log10(absY))
# plt.show()
