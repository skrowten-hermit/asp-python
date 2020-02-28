


########################################################################################################################
########################################################################################################################
## File              :: lib/asp/plot/graphplot.py
## Description       :: VoIP Automation Common API : Plots graphs of the output speech files for analysis.
## Developer         :: Sreekanth S
## Version           :: v1.0
## Release Date      :: 08/04/2019
## Changes made      :: Added function plot_graph to support DTMF, other improvements in graph presentation.
## Changes made Date :: 08/04/2019
## Changes made by   :: Sreekanth S
########################################################################################################################
########################################################################################################################



from scipy import fft, arange
from scipy.io.wavfile import read as readWav
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
WavGraphPlot contains functions to plot different types of graphs, specific to audio or speech extracted from .wav files 
which can be directly plotted or added to a bigger plot as sub-graphs.
"""



class WavGraphPlot:
    def __init__(self, source, sink, outpath, debug=0):
        self.inwav = source
        self.recwav = sink
        self.currwav = source
        self.outdir = outpath
        self.wavdata = []
        self.wavdlen = 0
        self.wavbitdepth = 8
        self.samplerate = 8000
        self.freq = []

        self.graphloc = 1      #The coordinate of canvas where it has to plot the graph.
        self.final_match = []
        self.origfreqresult = []
        self.origpowerresult = []
        self.orig_frq_bup = []
        self.ori_list = []
        self.fre_list = []
        self.pow_list = []
        self.orig_max_frq = 0
        self.DEBUG = debug

        # if self.debug:
        #     self.graph_cnt=4
        # else:
        #     self.graph_cnt=3
#*----------------------------------------------------------------------------------------------------------------------

# Read data from a given wav file.

    def _readWavFile(self, wavfile):
        self.samplerate, self.wavdata = readWav(wavfile)
        self.wavdlen = len(self.wavdata)
        self.curr_wav = wavfile
#*----------------------------------------------------------------------------------------------------------------------

# Plots the pitch graph - amplitude (normalized numerical value) vs time (seconds) of a given .wav file.

    def plotWavAmplLevTime(self, subgraph):
        if self.DEBUG == 1:
            print "Printing Signal graph (amplitude vs seconds)...."
        s = self.wavdata.dtype
        if "int16" == s:
            self.wavbitdepth = 16
        else:
            self.wavbitdepth = 8
        nsamples = self.wavdlen / self.samplerate
        sample_arr = np.linspace(0, nsamples, self.wavdlen)
        subgraph.plot(sample_arr, self.wavdata)
        title = getfilename(self.curr_wav)
        subgraph.set_title(title)
        subgraph.tick_params(axis='x', labelsize=10)
        subgraph.tick_params(axis='y', labelsize=10)
        subgraph.set_xlabel('Time')
        subgraph.set_ylabel('Numerical level')
        if self.DEBUG == 1:
            print "Waveform of " + str(title) + " plotted...."
#*----------------------------------------------------------------------------------------------------------------------

# Plots the power spectral density graph - power (dB) vs frequency (Hz) of a given .wav file.

    def plotSpectralDensity(self, subgraph):
        if self.DEBUG == 1:
            print "Printing Power Spectral Density (dB vs Hz)...."
        title = getfilename(self.curr_wav)
        tdata = arange(self.wavdlen)
        nsamples = self.wavdlen / self.samplerate
        self.freq = tdata / nsamples # two sides frequency range
        self.freq = self.freq[range(self.wavdlen/2)] # one side frequency range
        self.fft_vals = fft(self.wavdata)/self.wavdlen # fft computing and normalization
        self.fft_vals = self.fft_vals[range(self.wavdlen/2)]
        subgraph.plot(self.freq, abs(self.fft_vals), 'r')  # plotting the spectrum
        subgraph.tick_params(axis='x', labelsize=10)
        subgraph.tick_params(axis='y', labelsize=10)
        subgraph.tick_params()
        subgraph.set_xlabel('Frequency')
        subgraph.set_ylabel('Power')
        del self.fft_vals, tdata
        gc.collect()
        if self.DEBUG == 1:
            print "Spectral Density (dB vs Hz) of " + str(title) + " plotted...."
#*----------------------------------------------------------------------------------------------------------------------

# Plots the spectrogram - frequency (Hz) vs time (seconds) of a given .wav file.

    def plotSpectrogram(self, subgraph):
        if self.DEBUG == 1:
            print "Plotting Spectrogram (kHz vs seconds)...."
        title = getfilename(self.curr_wav)
        frq = self.samplerate / 1000
        # window = ceil(100*self.rate/1000)
        # step = ceil(20*self.rate/1000)
        # pylab.subplot(self.graph_cnt, 2, self.graphloc+4)
        # self.Pxx, self.freqs, self.bins, self.im = pylab.specgram(self.data, 2 ^ nextpowerof2(window),
        #                                                           Fs=self.rate, detrend=pylab.detrend_none,
        #                                                           window=pylab.window_hanning, noverlap=0)
        subgraph.specgram(self.wavdata, NFFT=128, noverlap=0, Fs=frq)
        subgraph.tick_params(axis='x', labelsize=10)
        subgraph.tick_params(axis='y', labelsize=10)
        subgraph.set_xlabel('Time')
        subgraph.set_ylabel('Frequency')
        if self.DEBUG == 1:
            print "Spectrogram (kHz vs seconds) of " + str(title) + " plotted...."
#*----------------------------------------------------------------------------------------------------------------------

# Plots the spectrogram - frequency (Hz) vs time (seconds) of a given .wav file.

    def plotChirpGraph(self, idraw, orig_file, rec_file, OUTPUT_GRAPH_FILES, seq, chirp):
        # remove pylab functions and replace with pyplot
        self.rec_file=rec_file
        self.OUTPUT_GRAPH_FILES=OUTPUT_GRAPH_FILES
        self.seq=seq
        self.orig_file=orig_file
        self.chirp=chirp
        self.draw=idraw

        for n in range(2):
            self.graphloc = n + 1
            if self.graphloc == 1:
                self.wav_file = self.orig_file
            else:
                self.wav_file = self.rec_file
            self.rate,self.data = readWav(self.wav_file)
            print "file, rate, data=",self.wav_file, self.rate, self.data.dtype
            self.draw.plot_amplitime()
            self.draw.plotSpectru()
            self.draw.plot_spectrogram()
            rs, ra = self.draw.user_graph_2()

        return  rs, ra
#*----------------------------------------------------------------------------------------------------------------------


    def plotFFTGraph(self, fft_length, fft_values, square_values, recorded, counter):
# This program creats graph of power values.
        # remove pylab functions and replace with pyplot
        if square_values > 0:   # Square value of pitch sum.
            t = arange(0, fft_length, 1)
            cx = fig.add_subplot(3, 2, self.graphloc)
            cx.semilogy(t, fft_values)
            grid("on")
            xlabel('FFT Samples')
            ylabel('FFT Values')
            title('FFT')
            axis('tight')
        else:
            t = arange(0, fft_length, 1)
            dx = fig.add_subplot(3, 2, self.graphloc)
            grid("on")
            xlabel('RMS Length')
            ylabel('RMS Values')

        if recorded == 1:
            return
        else:
            if self.debug == 1:
                print "COUNTER_MAIN=", counter
            save_loc = self.out_dir + 'RESULT.%s.png' % counter
            fig.savefig(save_loc)
            ##        a_in,a_Out=os.popen2(save_loc)
            ##        print a_in
            ##        print a_Out
            ##        time.sleep(5)
            ##        os.system("tskill PicasaPhotoViewer")
            if self.debug == 1:
                print "Running"
            close()
#*----------------------------------------------------------------------------------------------------------------------


    def saveWave(self, samples, counter):
        new_f = plt.figure()
        new_fig = new_f.add_subplot(1, 1, 1)
        new_fig.plot(samples)
        grid("on")
        new_fig.axis((0, 70000, -6000, 6000))

        if counter == 1: title = 'sout.wav'
        if counter == 2: title = 'rout.wav'
        save_loc = self.out_dir + 'wave_file_%s.png' % counter
        new_f.savefig(save_loc)
#*----------------------------------------------------------------------------------------------------------------------


    def new_canvas(self):
# This program creats a new canvas for plotting the image.
        global fig
        fig = plt.figure()
#*----------------------------------------------------------------------------------------------------------------------



"""
GenGraphPlot contains functions to plot different types of generic graphs for visualization, which can be directly 
plotted or added to a bigger plot as sub-graphs.
"""



class GenGraphPlot:
    def __init__(self, source, sink, outpath, debug=0):
        self.inwav = source
        self.recwav = sink
        self.currwav = source
        self.outdir = outpath
        self.wavdata = []
        self.wavdlen = 0
        self.wavbitdepth = 8
        self.samplerate = 8000
        self.freq = []

        self.graphloc = 1      #The coordinate of canvas where it has to plot the graph.
        self.final_match = []
        self.origfreqresult = []
        self.origpowerresult = []
        self.orig_frq_bup = []
        self.ori_list = []
        self.fre_list = []
        self.pow_list = []
        self.orig_max_frq = 0
        self.DEBUG = debug

        # if self.debug:
        #     self.graph_cnt=4
        # else:
        #     self.graph_cnt=3
#*----------------------------------------------------------------------------------------------------------------------


    def plotMOSGraph(self, res_dic):
        #main_control_1100_spcli
        # remove pylab functions and replace with pyplot
        N = len(res_dic)
        cmap = pylab.cm.get_cmap("hsv", N + 1)
        save_file = self.out_dir + "RESULT_MOS.png"
        pylab.subplot()
        for n in res_dic:
            tik=len(res_dic[n])
            pylab.plot(range(len(res_dic[n])),res_dic[n], label=n, color=cmap(N))
            N-=1
        pylab.xticks(range(tik))
        pylab.legend(loc='best')

        pylab.xlabel('Iteration')
        pylab.ylabel('MOS Score')
        print "MOS Plot Done...."

        pylab.savefig(save_file, bbox_inches='tight', dpi=250)
        pylab.gcf()
        pylab.gca()
        pylab.close('all')
        gc.get_referrers()
        gc.collect()
#*----------------------------------------------------------------------------------------------------------------------


    def plotMemoryGraph(self, mem_values,OUTPUT_GRAPH_FILES):
        # remove pylab functions and replace with pyplot
        pylab.plot(range(len(mem_values)), mem_values)
        pylab.xlabel('Count')
        pylab.ylabel('Value in KB')
        pylab.tick_params(axis='x', labelsize=8)
        pylab.tick_params(axis='y', labelsize=8)
        pylab.xticks(rotation=0)
        save_file = OUTPUT_GRAPH_FILES + 'MEM_PLOT_RESULT.png'
        pylab.savefig(save_file)
        print "Mem Graph Plot done"
#*----------------------------------------------------------------------------------------------------------------------
##iter=0
##save_file="C:\\automation\Voice_Test_Tool\Output\\"
##
##if int(sys.argv[1])==0:
##    o_file='C:\\automation\Voice_Test_Tool\input\sirtest_nb.wav'
##else:
##    o_file='C:\\automation\Voice_Test_Tool\input\sirtest_wb_63.wav'
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
