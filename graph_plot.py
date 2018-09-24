import matplotlib.pyplot as pl
import time
from scipy import fft, arange
from numpy import linspace
from scipy.io.wavfile import read
import gc
import sys



def plotWavAmplLev(in_file, sub_graph):
    print "Printing Signal graph (amplitude vs seconds)...."
    rate, data = read(in_file)
    dlen = len(data)
    timp = dlen / rate
    t = linspace(0,timp,dlen)

    sub_graph.plot(t, data)

    fl = in_file.split('/')
    file_name = fl[len(fl) - 1]
    sub_graph.set_title(file_name)
    sub_graph.tick_params(axis='x', labelsize=10)
    sub_graph.tick_params(axis='y', labelsize=10)
    sub_graph.set_xlabel('Time')
    sub_graph.set_ylabel('Numerical level')


def plotSpectralDensity(y, fs, sub_graph):
    print "Printing Power Spectral Density (dB vs Hz)...."
    n = len(y)  # lungime semnal
    k = arange(n)
    T = n / fs
    frq = k / T  # two sides frequency range
    frq = frq[range(n / 2)]  # one side frequency range
    ff_valu = fft(y) / n  # fft computing and normalization
    ff_valu = ff_valu[range(n / 2)]
    sub_graph.plot(frq, abs(ff_valu), 'r')  # plotting the spectrum
    sub_graph.tick_params(axis='x', labelsize=10)
    sub_graph.tick_params(axis='y', labelsize=10)
    sub_graph.tick_params()
    sub_graph.set_xlabel('Frequency')
    sub_graph.set_ylabel('Power')
    del frq, ff_valu, n, k, T, y
    gc.collect()
    return


def plotSpectrogram(rate, data, sub_graph):
    print "Plotting Spectrogram (kHz vs seconds)...."
    if rate == 16000:
        frq = 16
    else:
        frq = 8
    sub_graph.specgram(data, NFFT=128, noverlap=0, Fs=frq)
    sub_graph.tick_params(axis='x', labelsize=10)
    sub_graph.tick_params(axis='y', labelsize=10)
    sub_graph.set_xlabel('Time')
    sub_graph.set_ylabel('Frequency')


def graph_plot(in_file_list, output_folder, func_type):
    orig_file = in_file_list[0]
    rec_file = in_file_list[1]
    g_index = 1
    g_rows = 3
    g_cols = 2

    # for file in in_file_list:
    #     pl.subplot(g_rows, g_cols, g_index)
    #     rate, data = plotWavAmplLev(file)
    #     pl.subplot(g_rows, g_cols, g_index+2)
    #     plotSpectralDensity(data, rate)
    #     pl.subplot(g_rows, g_cols, g_index+4)
    #     plotSpectrogram(rate, data)
    #     g_index+=1

    fig, axes = pl.subplots(g_rows, g_cols, figsize=(20,15), sharex="row", sharey="row")

    for i, row in enumerate(axes):
        for j, col in enumerate(row):
            if i == 0 :
                if j == 0:
                    print "Source file waveform is being plotted...."
                    rate, data = read(orig_file)
                    plotWavAmplLev(orig_file, col)
                    continue
                elif j == 1:
                    print "Recorded file waveform is being plotted...."
                    rate, data = read(rec_file)
                    plotWavAmplLev(rec_file, col)
                    continue
            elif i == 1:
                if j == 0:
                    print "Source file PSD is being plotted...."
                    rate, data = read(orig_file)
                    plotSpectralDensity(data, rate, col)
                    continue
                elif j == 1:
                    print "Recorded file PSD is being plotted...."
                    rate, data = read(rec_file)
                    plotSpectralDensity(data, rate, col)
                    continue
            elif i == 2:
                if j == 0:
                    print "Source file Spectrogram is being plotted...."
                    rate, data = read(orig_file)
                    plotSpectrogram(rate, data, col)
                    continue
                elif j == 1:
                    print "Recorded file Spectrogram is being plotted...."
                    rate, data = read(rec_file)
                    plotSpectrogram(rate, data, col)
                    continue
    pl.tight_layout()

    name = in_file_list[0].split("/")
    lnth = len(name)
    name = in_file_list[0].split("/")[lnth - 1].split(".")[0]
    print "File=", name
    if func_type == 'multiple':
        save_file = output_folder + 'RESULT_' + name + '.png'
    else:
        save_file = output_folder + 'RESULT_graph.png'
    pl.savefig(save_file)
    pl.gcf()
    pl.gca()
    pl.close('all')
    del in_file_list, output_folder, rate, data
    gc.get_referrers()
    gc.collect()


def result_plot(orig_file, rec_file, output_folder, seq):
    flist = [orig_file, rec_file]
    graph_plot(flist, output_folder, 'multiple')
    graph_plot(flist, output_folder, 'single')



s_file="/home/sreekanth/Documents/Output/"
#o_file='/home/sreekanth/Documents/audio/male_8k_short_orig.wav'
o_file='/home/sreekanth/Documents/audio/male_8k_orig.wav'
#r_file='/home/sreekanth/Documents/audio/male_8k_short_rec.wav'
r_file='/home/sreekanth/Documents/audio/male_8k_rec.wav'
print 10*"#"+"Start"+10*"#"
result_plot(o_file, r_file,s_file, 'multiple')
print 10*"#"+"End"+10*"#"
pl.close('all')
