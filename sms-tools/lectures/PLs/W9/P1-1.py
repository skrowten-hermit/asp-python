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
import essentia.standard as ess

"""
P1-1: Essentia - mfcc.py

This program implements analysis of a window function using DFT.

"""



cwd = os.getcwd()
dtree = cwd.split('/')
ltree = len(dtree)
lroot = ltree - 3
stpath = ""
stpath = '/'.join(dtree[:lroot])
modpath = stpath + '/software/models/'
sys.path.append(modpath)

M = 1024 # Window length/size.
N = 1024
H = 512
fs = 44100
inputFile = stpath + '/sounds/speech-female.wav'

spectrum = ess.Spectrum(size=N)
window = ess.Windowing(size=M, type='hann')
mfcc = ess.MFCC(numberCoefficients=12, inputSize=(N/2)+1)
x = ess.MonoLoader(filename=inputFile, sampleRate=fs)()
mfccs = []

for frame in ess.FrameGenerator(x, frameSize=M, hopSize=H, startFromZero=True):
    mX = spectrum(window(frame))
    mfcc_bands, mfcc_coeffs = mfcc(mX)
    mfccs.append(mfcc_coeffs)

mfccs = np.array(mfccs)
