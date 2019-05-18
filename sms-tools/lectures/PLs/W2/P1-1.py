import matplotlib.pyplot as plt
import numpy as np

"""
P1-1: Plotting a real sinusoid

Real sinewave is a sequence of real numbers that can be computed by using the formula:
x[n] = A * cos(2*pi*f*n*T + phi)
So, the arguments are - the constant "pi", the (fundamental) frequency "f", the discrete time index
"n", the sampling period "T" and the initial phase "phi".

"""


A = 0.8
f0 = 1000
phi = np.pi/2
# Sampling rate 'fs' is needed because we need to compute the sampling period or we need to display
# real sine wave in time.
fs = 44100

# We use arange to define an array of floating point numbers going from -0.002 to 0.002 in steps or
# increments of 1.0/fs.
t = np.arange(-0.002, 0.002, 1.0/fs)
x = A * np.cos(2 * np.pi * f0 * t + phi)

# The following will plot a sinusoid, which will have time (in secs) on x-axis, the horizontal axis
# where the time t=0 is in the center and the amplitude is on the y-axis, the vertical axis. This 
# plot will have 4 periods in the sinewave.
plt.plot(t, x)
plt.axis([-0.002, 0.002, -0.8, 0.8])
plt.xlabel("time")
plt.ylabel("amplitude")
plt.show()
