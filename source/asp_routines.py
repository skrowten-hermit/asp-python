##########################################################################################################################################
##########################################################################################################################################
## File              :: asp_routines.py
## Description       :: Audio, speech verification routines/functions using essentia.
## Developer         :: Sreekanth S
## Version           :: v1.0
## Release Date      :: 28/03/2019
## Changes made      :: Created a class based API.
## Changes made Date :: 23/08/2018
## Changes made by   :: Sreekanth S
##########################################################################################################################################
##########################################################################################################################################



from essentia.standard import *


class AudioPrism:
    def __init__(self, cmp, inp_file, out_file, op_fold, debug):
        self.compare = cmp          # Speech/audio comparison switch.
        self.srcWav = inp_file      # The source file which was played.
        self.recWav = out_file      # The output file that was recorded.
        self.outPath = op_fold      # The path where all the output files are to be stored.
        self.debug = debug          # Debug switch.
        self.prismAnalysisStruct = {

                                    }

# Loading audio from file in mono setting - single channel.

    def audio_loader(self, file):
        loader = MonoLoader(filename=file)()
        return loader

# Detect any clicks if present in the recorded file.

    def click_detector(self, file):
        print "Click detection"
        ClickDetector(file)

# Detect any burst of noise if present in the recorded file.

    def noiseburst_detector(self):
        print "Noise bursts detection"

# Detect any gaps/discontinuities if present in the recorded file.

    def gapsbreaks_detector(self):
        print "Broken audio detection"

# Detect any white-noise if present in the recorded file.

    def whitenoise_detector(self):
        print "White-noise in background detection"

# Detect any sine tone if present in the recorded file.

    def sinetone_detector(self):
        print "Sine tone in background detection"

# Check if the speech in the recorded file is metallic in nature.

    def metallicaudio_detector(self):
        print "Metallic audio detection"

# Check if the speech in the recorded file has any of the defects/problems mentioned in the functions above.

    def faultyaudio_detector(self):
        print "Check if the recorded audio has faults like clicks, breaks, background noise (white and tone), metallic audio"

# Check if the speech in the recorded file has higher gain level(s) compared to the source file.

    def highgain_detector(self):
        print "High gain (w.r.t source) detection"

# Check if the speech in the recorded file has lower gain level(s) compared to the source file.

    def lowgain_detector(self):
        print "Low gain (w.r.t source) detection"

# Check if the speech in the recorded file has higher or lower gain level(s) compared to the source file.

    def gain_detector(self):
        print "Check if the audio gain of recorded file has changed (increased or decreased)"

# Calculate the SNR of a given audio file.

    def snr_calculator(self):
        print "Calculate the Signal-To-Noise Ratio (SNR)"

# Compare and analyze speech.

    def speech_analysis(self):
        print "Comparing recorded speech to the input speech file"

