import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as pltx
import matplotlib.pyplot as pltmX
import matplotlib.pyplot as pltpX
import matplotlib.pyplot as pltB
import matplotlib.pyplot as pltmBX
import matplotlib.pyplot as pltpBX
from scipy.signal import triang
from scipy.fftpack import fft
import threading
import time

"""
P1-1: Fourier transform properties using Triangular Function

This program explores the DFT properties using a triangular function as the input signal, most 
importantly shifting property.

"""


def plotGraph(p, v, t, sub):
    p.plot(v)
    p.title(t)
    if sub == 0:
        p.show()
    time.sleep(1)


def plotGraphGrid():
    print "P"

n = 15
x = triang(n) # 'n' samples of triangular function is computed

# It's important to notice that even if the size of the samples is not a power of 2 (FFT requires the
# input sample size to be a power of 2), it will work because this particular implementation of FFT,
# scipy.fftpack.fft() would just implement the standard DFT when the sample size is not a power of 2.
# Thus, it won't be able to take advantage of FFT when the sample size is not a power of 2 but will
# work for any sample size.
X = fft(x)
mX = abs(X) # The magnitude spectrum
pX = np.angle(X) # The phase spectrum

# The following plot of x will show the triangular function going from t = 0 to t = n - 1.
# pltx.plot(x)
# pltx.show()

# The following plot of x will show the magnitude spectrum. A triangular function is a real function.
# Hence, the magnitude spectrum is symmetric. The symmetry is a little misleading. The symmetry is
# around zero. This has to be understood as a circular buffer in which the center is at zero, the
# first half of the array are from positive values (of 'n') and the second half of the array are
# negative values (of 'n'). So, the sample at 'n-1' is also the sample at '-1'. This keeps repeating.
# pltmX.plot(mX)
# pltmX.show()

# The following plot of x will show the phase spectrum. It shows a  complex function that's
# counter-intuitive to what we expect - a triangular function is even and the phase should be zero,
# which is one of the properties (symmetry) of DFT. Here, the phase is not zero because the time axis
# of the triangular function was not centered around zero, it had a shift operation with a shift of
# half of triangular function i.e., (n-1)/2(the peak was at (n-1)/2).
# pltpX.plot(pX)
# pltpX.show()

# The following changes to the triangular function, transforming it from 'x' to 'fftbuffer' will center
# it around zero. 'np.zeroes' creates an array of empty values. Then, we take the center point where
# the peak of the triangular function is located and copy the values from this point to the last value,
# the second half, to the first half (including the center) of the 'fftbuffer'. We also take the first
# half of 'x' and copy these values to the second half (excluding the center) of the 'fftbuffer'.
if n % 2 == 0:
    ctr = n/2
else:
    ctr = (n-1)/2
fftbuffer = np.zeros(n)
fftbuffer[:ctr + 1] = x[ctr:]
fftbuffer[ctr + 1:] = x[:ctr]

BX = fft(fftbuffer)
mBX = abs(BX)
pBX = np.angle(BX)

# The following plot of x will show the triangular function going from t = 0 to t = n - 1.
# t1 = threading.Thread(target=plotGraph, args=(pltx, x, 'plot of x[n]'))

# The following plot will show the magnitude spectrum of x. A triangular function is a real function.
# Hence, the magnitude spectrum is symmetric. The symmetry is a little misleading. The symmetry is
# around zero. This has to be understood as a circular buffer in which the center is at zero, the
# first half of the array are from positive values (of 'n') and the second half of the array are
# negative values (of 'n'). So, the sample at 'n-1' is also the sample at '-1'. This keeps repeating.
# t2 = threading.Thread(target=plotGraph, args=(pltmX, mX, 'magnitude spectrum of x[n]'))

# The following plot will show the phase spectrum of x. It shows a  complex function that's
# counter-intuitive to what we expect - a triangular function is even and the phase should be zero,
# which is one of the properties (symmetry) of DFT. Here, the phase is not zero because the time axis
# of the triangular function was not centered around zero, it had a shift operation with a shift of
# half of triangular function i.e., (n-1)/2(the peak was at (n-1)/2).
# t3 = threading.Thread(target=plotGraph, args=(pltpX, pX, 'phase spectrum of x[n]'))

# The following plot of 'fftbuffer' will show the triangular function being modified by copying the
# first half of 'x' to the end and by copying the second half to the beginning.
# t4 = threading.Thread(target=plotGraph, args=(pltB, fftbuffer, 'fftbuffer = x[n] centred around 0'))

# The following plot will show the  magnitude spectrum of the function 'fftbuffer', which is identical
# to that of the magnitude spectrum of 'x. This is because the magnitude doesn't change after a shift
# operation.
# t5 = threading.Thread(target=plotGraph, args=(pltmBX, mBX, 'magnitude spectrum of fftbuffer'))

# The following plot will show the phase spectrum of the function 'fftbuffer'. This should ideally be
# a 0 value along the x axis. But the plot here shows something different with a plot that shows odd
# symmetry. But if we take a look at the y-axis, we can see that the plot is in the scale of e^(-15),
# which means the y-axis values are actually "e^(-15)*y", which is negligible and is almost equal to
# 0. It's probably because of some numerical error. But this is essentially related a computer's
# computational precisional capability. It can be assumed to be 0.
# t6 = threading.Thread(target=plotGraph, args=(pltpBX, pBX, 'phase spectrum of fftbuffer'))
#
# t1.start()
# t2.start()
# t3.start()
# t4.start()
# t5.start()
# t6.start()
# t1.join()
# t2.join()
# t3.join()
# t4.join()
# t5.join()
# t6.join()

# pltB.plot(fftbuffer)
# pltB.show()

# pltmBX.plot(mBX)
# pltmBX.show()

# The following plot of x will show the triangular function going from t = 0 to t = n - 1.
# pltpBX.plot(pBX)
# pltpBX.show()


# To show as subplots,


fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, sharex=False, sharey=False)
fig.suptitle('Comparing non-shifted and shifted triangular signal')
fig.subplots_adjust(hspace=0.4, wspace=0.4)
ax1.plot(x, 'tab:blue')
ax1.tick_params(axis='both', which='both', labelsize=7)
ax1.set_xlabel('time')
ax1.set_ylabel('amplitude')
ax2.plot(fftbuffer, 'tab:red')
ax2.tick_params(axis='both', which='both', labelsize=7)
ax2.set_xlabel('time (shifted)')
ax2.set_ylabel('amplitude')
ax3.plot(mX, 'tab:blue')
ax3.tick_params(axis='both', which='both', labelsize=7)
ax3.set_xlabel('frequency')
ax3.set_ylabel('magnitude')
ax4.plot(mBX, 'tab:red')
ax4.tick_params(axis='both', which='both', labelsize=7)
ax4.set_xlabel('frequency')
ax4.set_ylabel('magnitude')
ax5.plot(pX, 'tab:blue')
ax5.tick_params(axis='both', which='both', labelsize=7)
ax5.set_xlabel('frequency')
ax5.set_ylabel('phase')
ax6.plot(pBX, 'tab:red')
ax6.tick_params(axis='both', which='both', labelsize=7)
ax6.set_xlabel('frequency')
ax6.set_ylabel('phase')

# sub_axes = [ax1, ax2, ax3, ax4, ax5, ax6]
# for axis in sub_axes:
#     for tick in axis.get_xticklabels():
#         tick.set_visible(True)
#     for tick in axis.get_yticklabels():
#         tick.set_visible(True)

# for ax in fig.get_axes():
#     ax.label_outer()

plt.show()