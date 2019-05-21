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
P1-2: Detection of fundamental frequency f0

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


import utilFunctions as UF
import dftModel as DFT
import stft as STFT
import sineModel as SM
import harmonicModel as HM

inputFile = stpath + '/sounds/sawtooth-440.wav'
fs, x = UF.wavread(inputFile)

window_type = 'blackman'
w = get_window(window_type, 1001)

N = 1024
t = -50
minf0 = 300
maxf0 = 500
f0et = 1

H = 1000

f0 = HM.f0Detection(x, fs, w, N, H, t, minf0, maxf0, f0et)
