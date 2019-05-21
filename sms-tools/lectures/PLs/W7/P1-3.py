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
P1-3: Analysis and synthesis of sound using stochastic model

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
import stochasticModel as STM

inputFile = stpath + '/sounds/ocean.wav'
fs, x = UF.wavread(inputFile)
H = 128
stocf = 0.2

stocEnv = STM.stochasticModelAnal(x, H, H * 2, stocf)
