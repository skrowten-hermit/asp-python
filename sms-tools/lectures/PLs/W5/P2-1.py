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
P2-1: Peak detection

This program implements additive synthesis using sinusoidal model. That is how to synthesize a sinusoid
from the computed spectral peaks using additive synthesis in the frequency domain. We do this by 
synthesizing the main lobes of Blackman window first and then take the inverse DFT of that.
This program shows how to synthesize a lobe of blackman harris window.

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

f = 0.5

# The bins that have to be generated - since we want to generate only the main lobe, we only give eight
# centered points for 8 bins of Blackman-Harris window.
bins1 = np.array([-4, -3, -2, -1, 0, 1, 2, 3])
# The bins that have to be generated - since we want to generate only the main lobe, we only give eight
# centered points with wider main lobe with added shift/width to move the main lobe around the samples.
# This is how we generate main lobes corresponding to different frequencies.
bins2 = np.array([-4, -3, -2, -1, 0, 1, 2, 3]) + f
X1 = UF.genBhLobe(bins1) # Function to generate the main lobe
mX1 = 20 * np.log10(X1)
X2 = UF.genBhLobe(bins2) # Function to generate the main lobe
mX2 = 20 * np.log10(X2)

fig, (ax1, ax2) = plt.subplots(1, 2, sharex=False, sharey=False)
fig.suptitle('Comparing Blackman-Harris Lobes')
fig.subplots_adjust(hspace=0.4, wspace=0.4)
ax1.plot(mX1, 'tab:blue')
ax1.tick_params(axis='both', which='both', labelsize=7)
ax1.set_xlabel('sample/bin')
ax1.set_ylabel('amplitude (in dB)')
ax2.plot(mX2, 'tab:red')
ax2.tick_params(axis='both', which='both', labelsize=7)
ax2.set_xlabel('sample/bin')
ax2.set_ylabel('amplitude (in dB)')
plt.show()
