


########################################################################################################################
########################################################################################################################
## File              :: lib/asp/plot/stdaudioplots.py
## Description       :: VoIP Automation Common API : Plots graphs of the output speech files for analysis in a standard
##                      format (2x3).
## Developer         :: Sreekanth S
## Version           :: v1.0
## Release Date      :: 08/04/2019
## Changes made      :: Added function plot_graph to support DTMF, other improvements in graph presentation.
## Changes made Date :: 08/04/2019
## Changes made by   :: Sreekanth S
########################################################################################################################
########################################################################################################################



from scipy import fft, arange
from scipy.io.wavfile import read
from scipy.fftpack import fft, fftfreq, fftshift
from scipy.signal import get_window
from math import ceil, pi
import pylab
import matplotlib.pyplot as pl
from matplotlib import mlab
import numpy as np
import struct
from array import array
import random
import time
import gc
import sys
import os
from pylab import *
from numpy import arange
import signal
import string

from lib.generic.globalutils import *



"""
WavPlotStdCanvas contains functions to plot various types of standard analysis graphs, creating a canvas comprising of 
two or more sub-graphs created from various plots implemented in WavGraphPlot.
"""



class WavPlotStdCanvas:
    def __init__(self, source, sink, opath, debug=0):
        self.in_wav = source
        self.rec_wav = sink
        self.curr_wav = source
        self.out_dir = opath
        self.wdata = []
        self.wdlen = 0
        self.wbit_cnt = 8
        self.srate = 8000
        self.freq = []

        self.debug = 1
        self.graph_loc = 1      #The coordinate of canvas where it has to plot the graph.
        self.final_result_freq_orig = []
        self.final_result_pow_freq_orig = []
        self.orig_frq_bup = []
        self.ori_list = []
        self.fre_list = []
        self.pow_list = []
        self.final_match = []
        self.orig_max_frq = 0

        # if self.debug:
        #     self.graph_cnt=4
        # else:
        #     self.graph_cnt=3


    def plotWavAnalysisGraphs(self, analysis_type):
        g_index = 1
        g_rows = 3
        g_cols = 2

        fig, axes = pl.subplots(g_rows, g_cols, figsize=(20,15), sharex="row", sharey="row")

        for i, row in enumerate(axes):
            for j, col in enumerate(row):
                if i == 0 :
                    if j == 0:
                        print "Source file's waveform is being plotted...."
                        self.readWavFile(self.in_wav)
                        self.plotWavAmplLev(col)
                        continue
                    elif j == 1:
                        print "Recorded file's waveform is being plotted...."
                        self.readWavFile(self.rec_wav)
                        self.plotWavAmplLev(col)
                        continue
                elif i == 1:
                    if j == 0:
                        print "Source file's PSD is being plotted...."
                        self.readWavFile(self.in_wav)
                        self.plotSpectralDensity(col)
                        continue
                    elif j == 1:
                        print "Recorded file's PSD is being plotted...."
                        self.readWavFile(self.rec_wav)
                        self.plotSpectralDensity(col)
                        continue
                elif i == 2:
                    if j == 0:
                        print "Source file's Spectrogram is being plotted...."
                        self.readWavFile(self.in_wav)
                        self.plotSpectrogram(col)
                        continue
                    elif j == 1:
                        print "Recorded file's Spectrogram is being plotted...."
                        self.readWavFile(self.rec_wav)
                        self.plotSpectrogram(col)
                        continue
        pl.tight_layout()

        name = getfilename(self.rec_wav)
        if analysis_type == 'multiple':
            save_file = self.out_dir + 'RESULT_' + name + '.png'
        else:
            save_file = self.out_dir + 'RESULT_graph.png'
        pl.savefig(save_file)
        pl.gcf()
        pl.gca()
        pl.close('all')
        gc.get_referrers()
        gc.collect()
#*----------------------------------------------------------------------------------------------------------------------


    def selectPlotType(self, type):
        if type == 1:
            self.plotWavAnalysisGraphs('multiple')
        elif type == 2:
            self.plotWavAnalysisGraphs('single')
#*----------------------------------------------------------------------------------------------------------------------



##iter=0
##save_file="C:\\automation\Voice_Test_Tool\Output\\"
##
##if int(sys.argv[1])==0:
##    o_file='C:\\automation\Voice_Test_Tool\Input\sirtest_nb.wav'
##else:
##    o_file='C:\\automation\Voice_Test_Tool\Input\sirtest_wb_63.wav'
##
##r_file='C:\\automation\Voice_Test_Tool\Output\SIR_TEST_REC.0.wav'
##
##imaged=image_draw(o_file, r_file, save_file, iter)
##imaged.graph_plot(imaged)




# s_file="/home/sreekanth/Documents/Output/"
# #o_file='/home/sreekanth/Documents/audio/male_8k_short_orig.wav'
# o_file='/home/sreekanth/Documents/audio/male_8k_orig.wav'
# #r_file='/home/sreekanth/Documents/audio/male_8k_short_rec.wav'
# r_file='/home/sreekanth/Documents/audio/male_8k_rec.wav'
# print 10*"#"+"Start"+10*"#"
# result_plot(o_file, r_file,s_file, 'multiple')
# print 10*"#"+"End"+10*"#"
# pl.close('all')



if __name__ == '__main__':
    print "Capturing...."
