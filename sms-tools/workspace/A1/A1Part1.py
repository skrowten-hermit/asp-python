import sys
import os
import numpy as np
sys.path.append('../../software/models/')
from utilFunctions import wavread

"""
A1-Part-1: Reading an audio file

Write a function that reads an audio file and returns 10 consecutive samples of the file starting from 
the 50001th sample. This means that the output should exactly contain the 50001th sample to the 50010th 
sample (10 samples). 

The input to the function is the file name (including the path) and the output should be a numpy array 
containing 10 samples.

If you use the wavread function from the utilFunctions module the input samples will be automatically 
converted to floating point numbers with a range from -1 to 1, which is what we want. 

Remember that in python, the index of the first sample of an array is 0 and not 1.

If you run your code using piano.wav as the input, the function should return the following 10 samples:  
array([-0.06213569, -0.04541154, -0.02734458, -0.0093997 ,  0.00769066,	0.02319407,  0.03503525, 
0.04309214, 0.04626606,  0.0441908], dtype=float32)

[-0.34058657 -0.34437087 -0.32557145 -0.2929777  -0.25586718 -0.21692556
 -0.17041536 -0.11499374 -0.06384473]
"""


def readAudio(inputFile):
    """
    Input:
        inputFile: the path to the wav file      
    Output:
        The function should return a numpy array that contains 10 samples of the audio.
    """
    ## Your code here

    # out_samples = numpy.empty(1)
    print "Input : ", inputFile
    type, samples = wavread(inputFile)
    np_samples = np.array(samples)
    print "samples = ", samples
    print "np samples = ", np_samples
    print "type = ", type
    print "len(samples) = ", len(samples)
    print "len(np samples) = ", len(np_samples)

    out_samples = np.array(samples[5000:5009])

    print "out samples", out_samples


# print "Path = ", sys.path

in_wav = '../../sounds/piano.wav'

print in_wav

readAudio(in_wav)