


########################################################################################################################
########################################################################################################################
## File              :: lib/asp/audio/audioprism.py
## Description       :: VoIP Automation Common API : Audio, speech analysis functions for analysis and verification of
##                      audio.
## Developer         :: Sreekanth S
## Version           :: v2.0
## Release Date      :: 28/03/2019
## Changes made      :: Created a class based API.
## Changes made Date :: 23/08/2018
## Changes made by   :: Sreekanth S
########################################################################################################################
########################################################################################################################



import wave
import os
import string
import time
import gc
import essentia

import numpy
from math import sqrt
from numpy.fft import fft

from essentia.standard import *

from lib.generic.globalutils import *



class AudioPrism:
    def __init__(self, cmp, inp_file, out_file, op_fold, debug=0):
        self.source = ""
        self.sink = ""
        self.compare = cmp          # Speech/audio comparison switch.
        self.srcWav = inp_file      # The source file which was played.
        self.recWav = out_file      # The output file that was recorded.
        self.outPath = op_fold      # The path where all the output files are to be stored.
        self.sourceprops = {}
        self.sinkprops = {}
        self.AudioPrismAnalysisStruct = {

                                        }
        self.DEBUG = debug
#*----------------------------------------------------------------------------------------------------------------------

# Compare frequency.

    def frequencyCompare(self):
        # remove pylab functions and replace with pyplot
        data_size = 40000
        wav_file = wave.open(self.wav_file, 'r')
        data = wav_file.readframes(data_size)
        wav_file.close()
        data = struct.unpack('{n}h'.format(n=data_size), data)
        data = numpy.array(data)
        w = numpy.fft.fft(data)
        freqs = numpy.fft.fftfreq(len(w))
        # print "Min & Max=", freqs.min(), freqs.max()
        # Find the peak in the coefficients
        idx = numpy.argmax(numpy.abs(w))
        freq = freqs[idx]
        freq_in_hertz = abs(freq * self.rate)
        print"freq_in_hertz=", freq_in_hertz
#*----------------------------------------------------------------------------------------------------------------------

# Get the gain levels of the source and the sink.

    def inoutGainLevels(self):
        print "Getting the gain levels of input and output files...."

        # TODO: Use 'SoX' command sox <filename>.wav -n stats to get dB levels (most likely its 'Pk lev dB')
#*----------------------------------------------------------------------------------------------------------------------

# LOAD AUDIO : Loading audio from file in mono setting - single channel.

    def audioLoader(self, file):
        loader = MonoLoader(filename=file)()
        return loader
#*----------------------------------------------------------------------------------------------------------------------

# CLICKS DETECTOR : Detect any clicks if present in the recorded file.

    def clickDetector(self, file):
        print "Click detection"
        print ClickDetector(file)
#*----------------------------------------------------------------------------------------------------------------------

# NOISE BURST DETECTOR : Detect any burst of noise if present in the recorded file.

    def noiseburstDetector(self):
        print "Noise bursts detection"
#*----------------------------------------------------------------------------------------------------------------------

# BROKEN AUDIO DETECTOR : Detect any gaps/discontinuities if present in the recorded file.

    def gapsbreaksDetector(self):
        print "Broken audio detection"
#*----------------------------------------------------------------------------------------------------------------------

# BACKGROUND NOISE (WHITE) DETECTOR : Detect any white-noise if present in the recorded file.

    def whitenoiseDetector(self):
        print "White-noise in background detection"
#*----------------------------------------------------------------------------------------------------------------------

# BACKGROUND TONE (SINE) DETECTOR : Detect any sine tone if present in the recorded file.

    def sinetoneDetector(self):
        print "Sine tone in background detection"
#*----------------------------------------------------------------------------------------------------------------------

# METALLIC AUDIO VERIFIER : Check if the speech in the recorded file is metallic in nature.

    def metallicaudioDetector(self):
        print "Metallic audio detection"
#*----------------------------------------------------------------------------------------------------------------------

# CUMULATIVE DEFECT VERIFIER : Check if the speech in the recorded file has any of the defects/problems mentioned in the
# functions above.

    def faultyaudioDetector(self, file):
        print "Check if the recorded audio has faults like clicks, breaks, background noise (white and tone), " \
              "metallic audio"
#*----------------------------------------------------------------------------------------------------------------------

# HIGH-GAIN DETECTOR : Check if the speech in the recorded file has higher gain level(s) compared to the source file.

    def highgainDetector(self):
        print "High gain (w.r.t source) detection"
#*----------------------------------------------------------------------------------------------------------------------

# LOW-GAIN DETECTOR : Check if the speech in the recorded file has lower gain level(s) compared to the source file.

    def lowgainDetector(self):
        print "Low gain (w.r.t source) detection"
#*----------------------------------------------------------------------------------------------------------------------

# GAIN DETECTOR : Check if the speech in the recorded file has higher or lower gain level(s) compared to the source file
# (uses the two functions above).

    def gainDetector(self):
        print "Check if the audio gain of recorded file has changed (increased or decreased)"
#*----------------------------------------------------------------------------------------------------------------------

# SNR CALCULATOR : Calculate the SNR of a given audio file.

    def calculateSNR(self, file):
        print "Calculate the Signal-To-Noise Ratio (SNR)"
#*----------------------------------------------------------------------------------------------------------------------

# SPEECH ANALYSIS : Analyze speech.

    def speechAnalyser(self, source, recorded, file):
        print "Analysing the given file for any defects"
        self.faultyaudio_detector(file)
        if source == 0 and recorded == 1:
            self.gain_detector(file)
        self.snr_calculator(file)
#*----------------------------------------------------------------------------------------------------------------------

# SPEECH VERIFICATION : Compare speech after analysis.

    def speechVerifier(self):
        print "Comparing recorded speech to the input speech file"
        self.speech_analysis(1, 0, self.srcWav)
        self.speech_analysis(0, 1, self.recWav)
#*----------------------------------------------------------------------------------------------------------------------



'''
PowerSpectrum()
PitchSalience()
SpectrumCQ()
FadeDetection()
Larm()
Leq()
LevelExtractor()
Loudness()
LoudnessEBUR128()
DynamicComplexity()
CrossCorrelation()

ClickDetector()
DiscontinuityDetector()
GapsDetector()
NoiseBurstDetector()
SNR()
'''



if __name__ == '__main__':
    fn = '/home/sreekanth/Programs/input/Speech/male_8k_wclick.wav'
    tL = AudioPrism(0, fn, '', '', 0)
    audioSam = tL.audio_loader(fn)

    # from pylab import plot, show, figure, imshow
    # import matplotlib.pyplot as plt
    # plt.rcParams['figure.figsize'] = (15, 6)  # set plot sizes to something larger than default
    #
    # plot(audioSam[400:])
    # plt.title("This is how the 2nd second of this audio looks like:")
    # show()  # unnecessary if you started "ipython --pylab"

    tL.click_detector(audioSam)
