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

# LOAD AUDIO : Loading audio from file in mono setting - single channel.

    def audio_loader(self, file):
        loader = MonoLoader(filename=file)()
        return loader

# CLICKS DETECTOR : Detect any clicks if present in the recorded file.

    def click_detector(self, file):
        print "Click detection"
        print ClickDetector(file)

# NOISE BURST DETECTOR : Detect any burst of noise if present in the recorded file.

    def noiseburst_detector(self):
        print "Noise bursts detection"

# BROKEN AUDIO DETECTOR : Detect any gaps/discontinuities if present in the recorded file.

    def gapsbreaks_detector(self):
        print "Broken audio detection"

# BACKGROUND NOISE (WHITE) DETECTOR : Detect any white-noise if present in the recorded file.

    def whitenoise_detector(self):
        print "White-noise in background detection"

# BACKGROUND TONE (SINE) DETECTOR : Detect any sine tone if present in the recorded file.

    def sinetone_detector(self):
        print "Sine tone in background detection"

# METALLIC AUDIO VERIFIER : Check if the speech in the recorded file is metallic in nature.

    def metallicaudio_detector(self):
        print "Metallic audio detection"

# CUMULATIVE DEFECT VERIFIER : Check if the speech in the recorded file has any of the defects/problems mentioned in the
# functions above.

    def faultyaudio_detector(self, file):
        print "Check if the recorded audio has faults like clicks, breaks, background noise (white and tone), metallic audio"

# HIGH-GAIN DETECTOR : Check if the speech in the recorded file has higher gain level(s) compared to the source file.

    def highgain_detector(self):
        print "High gain (w.r.t source) detection"

# LOW-GAIN DETECTOR : Check if the speech in the recorded file has lower gain level(s) compared to the source file.

    def lowgain_detector(self):
        print "Low gain (w.r.t source) detection"

# GAIN DETECTOR : Check if the speech in the recorded file has higher or lower gain level(s) compared to the source file
# (uses the two functions above).

    def gain_detector(self):
        print "Check if the audio gain of recorded file has changed (increased or decreased)"

# SNR CALCULATOR : Calculate the SNR of a given audio file.

    def snr_calculator(self, file):
        print "Calculate the Signal-To-Noise Ratio (SNR)"

# SPEECH ANALYSIS : Analyze speech.

    def speech_analysis(self, source, recorded, file):
        print "Analysing the given file for any defects"
        self.faultyaudio_detector(file)
        if source == 0 and recorded == 1:
            self.gain_detector(file)
        self.snr_calculator(file)

# SPEECH VERIFICATION : Compare speech after analysis.

    def speech_verification(self):
        print "Comparing recorded speech to the input speech file"
        self.speech_analysis(1, 0, self.srcWav)
        self.speech_analysis(0, 1, self.recWav)


fn = '/home/skrowten_hermit/Programs/asp-python/Input/Speech/male_8k_wclick.wav'
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