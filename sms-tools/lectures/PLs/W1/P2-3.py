import matplotlib.pyplot as plt
import numpy as np

"""
P1-1: Inverse DFT

We'll need to go over all samples of "N" and compute the inverse.

"""

# The input signal x[n] can be defined with the help of sample size "N" and the frequency "k0" (the frequency
# index) as a real sinusoid, a cosine function.

N = 64
k0 = 7
# k0 = 7.5
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

# The output signal "y" is computed as follows:
y = np.array([])

for l in v:
# The "s" here is the sum of all complex exponentials of all possible frequencies at a given sample.
    s = np.exp(1j * 2 * np.pi * l * v / N)
# The output signal "y" is nothing but the appended to existing samples whatever it was from the
# previous computation sum of the spectrum "X" by "s" multiplied by the normalization factor 1/N.
# This is the inner product discussed in the theory lectures.
    y = np.append(y, 1.0 / N * sum(X * s))

# The plot should have all the samples in "y". This plot would be a cosine function whic has "k0" periods
# which is same as the input signal that we have computed.
plt.plot(v, np.real(y))
plt.axis([-N/2, N/2-1, -1, 1])
plt.show()