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
P3-1: Sinusoidal tracking using sinusoidal model

This program implements additive synthesis using sinusoidal model.

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

inputFile = stpath + '/sounds/oboe-A4.wav'
window_type = 'hamming'
M = 501
N = 1024
t = -90 # Threshold for peak detection
minSineDur = 0.1 # Min. duration of a sine track
maxnSines = 20 # Max. no of sines that will be allowed simultaneously
freqDevOffset = 10 # Allowed deviation from one frame to the next of a given track in Hz, it means that in the lowest frequency it allows a peak to change frequency by 'freqDevOffset' Hz from one frame to the next and still be part of the same track
freqDevSlope = 0.001 # A way to allow the deviation to increase for higher frequencies as in higher frequencies this deviation may be higher - higher the frequency, bigger the slope and bigger the deviation/change
H = 200

# Here, we use sineModelAnal() even though we have a complete function sineModel() because even
# though the latter implements the complete analysis-synthesis, it does not include the tracking
# aspect that we need - i.e., it cannot show sinusoidal tracks, it is meant to be used in real-time
# application while the former just performs the analysis part and is able to do sinusoidal
# tracking as it allows all the tracks in one place and do some post-processing on these tracks.

(fs, x) = UF.wavread(inputFile)
w = get_window(window_type, M)
tfreq, tmag, tphase = SM.sineModelAnal(x, fs, w, N, H, t, maxnSines, minSineDur, freqDevOffset, freqDevSlope)

numFrames = int(tfreq[:, 0].size)
frmTime = H * np.arange(numFrames)/float(fs)
tfreq[tfreq <= 0] = np.nan

# The tracks are plotted in different colours, not just for lines at different frequencies, but
# also in the same line there are different colours visible. This means that a particular track
# was alive for some time and then it disappeared and a new track started from there. This gives
# the idea that tracks can appear and disappear. Most of these tracks correspond to the harmonics
# of the sound, but some do not. Especially in the higher frequencies we can see that the tracks
# may be short-lived and may be tracks of some noise component(s) or some side lobe of the analysis
# which is part of the sinusoidal model and nothing much can be done about it. We can control the
# length of these tracks using the variable 'minSineDur' which when kept to an optimal value can
# help cleaning up the track and avoid unnecessary tracks that correspond to fragments of little
# sounds, noises or side lobes or things like that which we can call artifacts.

plt.plot(frmTime, tfreq)
plt.show()
