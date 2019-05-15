import matplotlib.pyplot as plt
import numpy as np

"""
P1-1: DFT of a complex sinusoid

Computing the DFT means computing X[k] i.e., to compute all the spectral values present in a given signal x[n].
So, we will be iterating over "k", which ranges from [0, N-1] and computing the sum. For the inverse DFT, we'll
iterating over all time and over all "n" and for each "n" we'll be computing the sum.

"""

# The input signal x[n] can be defined with the help of sample size "N" and the frequency "k0" (the frequency
# index) as a complex sinusoid.

N = 64
k0 = 7
n = np.arange(N)
x = np.exp(1j * 2 * np.pi * k0 * n / N)

X = np.array([])

for k in n:
# arange creates time sample indexes 0 to N-1
    s = np.exp(1j * 2 * np.pi * k / N * np.arange(N))
# The output spectrum is appended to existing spectrum whatever it was from the previous computation
# and we'll compute the sum of the multiplied by the conjugate of our complex exponential. This is the
# inner product discussed in the theory lectures
    X = np.append(X, sum(x * np.conjugate(s)))

# If the following analysis plot shows a peak value defined in "N" above for the frequency "k0", we can
# confirm that the input signal was indeed a complex sinusoid
plt.plot(np.arange(N), abs(X))
plt.axis([0, N-1, 0, N])
plt.show()