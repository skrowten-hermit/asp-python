import matplotlib.pyplot as plt
import numpy as np

"""
P1-1: DFT of a real sinusoid

Computing the DFT means computing X[k] i.e., to compute all the spectral values present in a given signal x[n].
So, we will be iterating over "k", which ranges from [0, N-1] and computing the sum. For the inverse DFT, we'll
iterating over all time and over all "n" and for each "n" we'll be computing the sum.

"""

# The input signal x[n] can be defined with the help of sample size "N" and the frequency "k0" (the frequency
# index) as a real sinusoid, a cosine function.

N = 64
k0 = 7
k0 = 7.5
n = np.arange(N)
v = np.arange(-N/2, N/2)
x = np.cos(2 * np.pi * k0 * n / N)

X = np.array([])

for k in v:
# arange creates time sample indexes 0 to N-1
    s = np.exp(1j * 2 * np.pi * k * n / N)
# The output spectrum is appended to existing spectrum whatever it was from the previous computation
# and we'll compute the sum of the multiplied by the conjugate of our complex exponential. This is the
# inner product discussed in the theory lectures.
    X = np.append(X, sum(x * np.conjugate(s)))

# If the following analysis plot shows 2 peaks value equal to "N/2" of "N" above for the frequency "k0", we can
# confirm that the input signal was indeed a real sinusoid because it has 2 complex exponential results as it
# is the sum of 2 complex exponentials. The x-axis values should be k0 and -k0, which is why we use "v" instead
# of "n", which goes from 0 to N-1. For non-integer values of frequency "k0", even though the peak is somewhere
# between the nearest integers on either side, the plot shows positive values for all complex exponentials.
plt.plot(v, abs(X))
plt.axis([-N/2, N/2-1, 0, N])
plt.show()