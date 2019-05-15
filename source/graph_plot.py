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



class graph_plot:
    def __init__(self, source, sink, opath):
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
        self.graph_loc = 1
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


    def ret_title(self, wfile):
        plist = wfile.split('/')
        file_name = plist[len(plist) - 1]
        return file_name
#*-----------------------------------------------------------------------------------------------------------------------------------------


    def ret_fname(self, wfile):
        plist = wfile.split('/')
        l = len(plist)
        name = plist[l - 1].split('.')[0]
        print "File=", name
        return name
#*-----------------------------------------------------------------------------------------------------------------------------------------


    def read_file(self, wfile):
        self.srate, self.wdata = read(wfile)
        self.wdlen = len(self.wdata)
        self.curr_wav = wfile
#*-----------------------------------------------------------------------------------------------------------------------------------------


    def plotWavAmplLev(self, subgraph):
        print "Printing Signal graph (amplitude vs seconds)...."
        s = self.wdata.dtype
        if "int16" == s:
            self.wbit_cnt = 16
        else:
            self.wbit_cnt = 8
        nsamples = self.wdlen / self.srate
        sample_arr = np.linspace(0, nsamples, self.wdlen)
        subgraph.plot(sample_arr, self.wdata)
        title = self.ret_title(self.curr_wav)
        subgraph.set_title(title)
        subgraph.tick_params(axis='x', labelsize=10)
        subgraph.tick_params(axis='y', labelsize=10)
        subgraph.set_xlabel('Time')
        subgraph.set_ylabel('Numerical level')
        print "Waveform of " + str(title) + " plotted...."
#*-----------------------------------------------------------------------------------------------------------------------------------------


    def plotSpectralDensity(self, subgraph):
        print "Printing Power Spectral Density (dB vs Hz)...."
        title = self.ret_title(self.curr_wav)
        tdata = arange(self.wdlen)
        nsamples = self.wdlen / self.srate
        self.freq = tdata / nsamples # two sides frequency range
        self.freq = self.freq[range(self.wdlen/2)] # one side frequency range
        self.fft_vals = fft(self.wdata)/self.wdlen # fft computing and normalization
        self.fft_vals = self.fft_vals[range(self.wdlen/2)]
        subgraph.plot(self.freq, abs(self.fft_vals), 'r')  # plotting the spectrum
        subgraph.tick_params(axis='x', labelsize=10)
        subgraph.tick_params(axis='y', labelsize=10)
        subgraph.tick_params()
        subgraph.set_xlabel('Frequency')
        subgraph.set_ylabel('Power')
        del self.fft_vals, tdata
        gc.collect()
        print "Spectral Density (dB vs Hz) of " + str(title) + " plotted...."
#*-----------------------------------------------------------------------------------------------------------------------------------------


    def plotSpectrogram(self, subgraph):
        print "Plotting Spectrogram (kHz vs seconds)...."
        title = self.ret_title(self.curr_wav)
        frq = self.srate / 1000
        subgraph.specgram(self.wdata, NFFT=128, noverlap=0, Fs=frq)
        subgraph.tick_params(axis='x', labelsize=10)
        subgraph.tick_params(axis='y', labelsize=10)
        subgraph.set_xlabel('Time')
        subgraph.set_ylabel('Frequency')
        print "Spectrogram (kHz vs seconds) of " + str(title) + " plotted...."
#*-----------------------------------------------------------------------------------------------------------------------------------------


    def wav_plot_analyse(self, analysis_type):
        g_index = 1
        g_rows = 3
        g_cols = 2

        fig, axes = pl.subplots(g_rows, g_cols, figsize=(20,15), sharex="row", sharey="row")

        for i, row in enumerate(axes):
            for j, col in enumerate(row):
                if i == 0 :
                    if j == 0:
                        print "Source file waveform is being plotted...."
                        self.read_file(self.in_wav)
                        self.plotWavAmplLev(col)
                        continue
                    elif j == 1:
                        print "Recorded file waveform is being plotted...."
                        self.read_file(self.rec_wav)
                        self.plotWavAmplLev(col)
                        continue
                elif i == 1:
                    if j == 0:
                        print "Source file PSD is being plotted...."
                        self.read_file(self.in_wav)
                        self.plotSpectralDensity(col)
                        continue
                    elif j == 1:
                        print "Recorded file PSD is being plotted...."
                        self.read_file(self.rec_wav)
                        self.plotSpectralDensity(col)
                        continue
                elif i == 2:
                    if j == 0:
                        print "Source file Spectrogram is being plotted...."
                        self.read_file(self.in_wav)
                        self.plotSpectrogram(col)
                        continue
                    elif j == 1:
                        print "Recorded file Spectrogram is being plotted...."
                        self.read_file(self.rec_wav)
                        self.plotSpectrogram(col)
                        continue
        pl.tight_layout()

        name = self.ret_fname(self.rec_wav)
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
#*-----------------------------------------------------------------------------------------------------------------------------------------


    def wav_plot_compare(self):
        self.wav_plot_analyse('multiple')
        self.wav_plot_analyse('single')
#*-----------------------------------------------------------------------------------------------------------------------------------------


    def MOS_graph(self, res_dic):
        #main_control_1100_spcli
        N = len(res_dic)
        cmap = pylab.cm.get_cmap("hsv", N + 1)
        pwd_tree=os.getcwd().split('/')
        base = '/'.join(pwd_tree[0:-1]) + "/Output/RESULT_MOS.png"
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

        pylab.savefig(base, bbox_inches='tight',dpi=250 )
        pylab.gcf()
        pylab.gca()
        pylab.close('all')
        gc.get_referrers()
        gc.collect()


    def nextpow2(self, i):
        n = 1
        while n < i: n *= 2
        return n


    def freq_time_specgram(self):
        window=ceil(100*self.rate/1000)
        step=ceil(20*self.rate/1000)
        pylab.subplot(self.graph_cnt,2,self.graph_loc+4)
        self.Pxx, self.freqs, self.bins, self.im=pylab.specgram(
        self.data,
        2^self.draw.nextpow2(window),
        Fs=self.rate,
        detrend=pylab.detrend_none,
        window=pylab.window_hanning,
        noverlap=0)
        pylab.tick_params(axis='x', labelsize=8)
        pylab.tick_params(axis='y', labelsize=8)
        pylab.xticks(rotation=0)
        if self.graph_loc==1:
            pylab.xlabel('Time')
            pylab.ylabel('Frequecy')

        print "Graph Plot done 3"


    def plot_amplitudetime(self):
        self.d_len=len(self.data)
        s=self.data.dtype

        if "int16" == s:
            self.bit_cnt=16
        else:
            self.bit_cnt=8

        t=np.linspace(0,self.d_len/self.rate,self.d_len)

        pylab.subplot(self.graph_cnt,2,self.graph_loc)
        pylab.plot(t,self.data)
        pylab.tick_params(axis='x', labelsize=8)
        pylab.tick_params(axis='y', labelsize=8)
        pylab.xticks(rotation=0)
        if self.graph_loc==1:
            pylab.xlabel('Time')
            pylab.ylabel('Numerical level')
        print "Graph Plot done 1"


    def plot_spectraldensity(self):
        n = len(self.data) # lungime semnal
        k = arange(n)
        T = n/self.rate
        i_frq = k/T # two sides frequency range
        self.frq = i_frq[range(n/2)] # one side frequency range
        self.ff_valu = fft(self.data)/n # fft computing and normalization
        self.ff_valu = self.ff_valu[range(n/2)]
        pylab.subplot(self.graph_cnt,2,self.graph_loc+2)
        if self.graph_loc==1:
            pylab.xlabel('Frequency')
            pylab.ylabel('Power')
        pylab.plot(self.frq,abs(self.ff_valu),'r') # plotting the spectrum
        pylab.tick_params(axis='x', labelsize=8)
        pylab.tick_params(axis='y', labelsize=8)
        pylab.xticks(rotation=0)
        print "Graph Plot done 2"


    def myround(self, x, base=100):
        return base * round(x / base)


    def frequency_comparision(self):
        data_size = 40000
        wav_file = wave.open(self.wav_file, 'r')
        data = wav_file.readframes(data_size)
        wav_file.close()
        data = struct.unpack('{n}h'.format(n=data_size), data)
        data = np.array(data)
        w = np.fft.fft(data)
        freqs = np.fft.fftfreq(len(w))
        # print "Min & Max=", freqs.min(), freqs.max()
        # Find the peak in the coefficients
        idx = np.argmax(np.abs(w))
        freq = freqs[idx]
        freq_in_hertz = abs(freq * self.rate)
        # print"freq_in_hertz=", freq_in_hertz


    def user_graph_2(self):
        result="Pass"
        reason="pass"
        pdata = struct.unpack('{n}h'.format(n=self.d_len), self.data)
        pdata = np.array(pdata)

        w = np.fft.fft(pdata)
        f = np.fft.fftfreq(len(w))

        self.freqs=abs(f*self.rate)

        a=np.abs(w)/len(pdata)

        print "level 0", len(self.freqs), len(a) ##, self.freqs

        np.append(self.freqs, 0)
        np.append(a, 0)

        print "level 1", len(self.freqs), len(a)

###########################################
        self.final_freq_rec=[]
        self.rec_final_freq=[]
        self.rec_final_power=[]
        self.Fresult_check=[]
        self.Presult_check=[]
        rp_max,cnt, r_pow_max=0,0, 0
        while cnt<len(self.freqs):
            if a[cnt]==0:
                self.final_freq_rec.append(0)
            else:
                self.final_freq_rec.append(int(self.freqs[cnt]))
            cnt+=1

        print "level 2", len(self.final_freq_rec), len(a) ##, self.final_freq_rec

        cnt, max_cnt=0,0

        while cnt<(len(self.final_freq_rec)-1):
##            print "Test", cnt, self.final_freq_rec[cnt], a[cnt]
            if cnt>0:
                if self.final_freq_rec[cnt]>self.final_freq_rec[cnt-1]:
                    r_pow_max=int(a[cnt])

            if self.final_freq_rec[cnt]==self.final_freq_rec[cnt+1]:
                if r_pow_max < int(a[cnt]):
                    r_pow_max=int(a[cnt])
            else:
                self.rec_final_freq.append(self.final_freq_rec[cnt])
                self.rec_final_power.append(r_pow_max)
                if r_pow_max>max_cnt:
                    max_cnt=r_pow_max
                r_pow_max=0
            cnt+=1

        print "level 3", len(self.rec_final_freq), len(self.rec_final_power), max_cnt, max_cnt/2 ##, self.rec_final_freq

        cnt=0
        while cnt<len(self.rec_final_freq):
            if self.rec_final_power[cnt] >= (max_cnt*0.4):
                if self.rec_final_freq[cnt]%100==0:
##                    print "Before final", cnt,self.rec_final_freq[cnt],self.rec_final_power[cnt]
                    self.Fresult_check.append(self.rec_final_freq[cnt])
                    self.Presult_check.append(self.rec_final_power[cnt])
            cnt+=1

        print "level 4", len(self.Fresult_check), len(self.Presult_check) ##, self.Fresult_check, self.Presult_check

        self.Fresult_check=self.Fresult_check[:len(self.Fresult_check)/2+1]
        self.Presult_check=self.Presult_check[:len(self.Presult_check)/2+1]

        print "level 5", len(self.Fresult_check), len(self.Presult_check)

        if self.graph_loc==1:
            self.final_match = self.Fresult_check
            print "len of final=", len(self.final_match), self.final_match

##        self.rec_final_freq=self.rec_final_freq[:len(self.rec_final_freq)/2]
##        self.rec_final_power=self.rec_final_power[:len(self.rec_final_power)/2]

##        cnt=0
##        while cnt<len(self.rec_final_freq):
##            print "final check result", self.rec_final_freq[cnt], self.rec_final_power[cnt]
##            cnt+=1

##        cnt=0
##        while cnt<len(self.Fresult_check):
##            print "final", self.Fresult_check[cnt], self.Presult_check[cnt]
##            cnt+=1

        idx = np.argmax(a)
        idx_min=np.argmin(a)

        if self.graph_loc==2:
            cnt, pcnt=0, 0
            fail_fre=[]
            if self.orig_max_frq==4000: # frequency comp compared from 300 to 3500
                ca_cnt=5
            elif self.orig_max_frq==8000:   # frequency comp compared from 300 to 7000
                ca_cnt=10
            else:
                ca_cnt=1

            self.orig_threshold_frq= self.orig_max_frq-(ca_cnt*100)
            print "Ready to compare :",self.Fresult_check

            for n in self.final_match[:(len(self.final_match))]:
                if self.chirp==1:
                    if n > self.orig_threshold_frq and n <=self.orig_max_frq:
                        print "pcnt",n
                        pcnt+=1
                    else:
                        if n in self.Fresult_check:
                            cnt+=1
                        else:
                            print "Missing=",n
                            fail_fre.append(n)
                    print "FChirp : %s %s    %s    %s"%(str(cnt), str(n),  str(self.orig_threshold_frq), str(self.orig_max_frq))
                else:
                    print "FC:",n
                    if n in self.Fresult_check:
                        cnt+=1
                    else:
                        fail_fre.append(n)
                        print "Missing=",n
                    print "Fdisc : %s %s"%(str(cnt), str(n))

            if ((len(self.final_match))==(cnt+pcnt)):
                result = "Pass"
                reason ="All frequency components are preset"
            elif ((len(self.final_match))>=((cnt+pcnt)-2)) or ((len(self.final_match))<=((cnt+pcnt)-1)):
                result = "Pass"
                reason ="Boundary components missing..."+str(fail_fre)
            else:
                result="Fail"
                reason="Missing frequency"+str(fail_fre)

            print result, reason
            print "Final length", len(self.final_match)
            print "Missing", cnt
            print "Beyond limit", pcnt
        else:
            self.orig_max_frq=self.draw.myround(self.freqs[idx])
            print "Max frequency =", self.orig_max_frq

###########################################
        if self.debug_flag:
            pylab.subplot(self.graph_cnt,2,self.graph_loc+6)
##            pylab.plot(self.freqs, a)
            pylab.plot(self.Fresult_check, self.Presult_check)

            pylab.tick_params(axis='x', labelsize=8)
            pylab.tick_params(axis='y', labelsize=8)
            pylab.xticks(rotation=0)
            if self.graph_loc==1:
                pylab.xlabel('Frequecy')
                pylab.ylabel('Power')
            print "Graph Plot done 5"

        if self.graph_loc==2:
            name = self.wav_file.split("/")
            lnth = len(name)
            name = self.wav_file.split("/")[lnth - 1].split(".")[0]
            print "File=", name
            save_file = self.OUTPUT_GRAPH_FILES+'RESULT_'+name+'.png'
            pylab.savefig(save_file)
            pylab.gcf()
            pylab.gca()
            pylab.close('all')
            gc.get_referrers()
            gc.collect()
            print "Saving the results...."
        return  result, reason+" "+str(len(self.final_match))


    def plotChirpGraph(self, idraw, orig_file, rec_file, OUTPUT_GRAPH_FILES, seq, chirp):
        self.rec_file=rec_file
        self.OUTPUT_GRAPH_FILES=OUTPUT_GRAPH_FILES
        self.seq=seq
        self.orig_file=orig_file
        self.chirp=chirp
        self.draw=idraw

        for n in range(2):
            self.graph_loc = n + 1
            if self.graph_loc == 1:
                self.wav_file = self.orig_file
            else:
                self.wav_file = self.rec_file
            self.rate,self.data = read(self.wav_file)
            print "file, rate, data=",self.wav_file, self.rate, self.data.dtype
            self.draw.plot_amplitime()
            self.draw.plotSpectru()
            self.draw.plot_spectrogram()
            rs, ra = self.draw.user_graph_2()

        return  rs, ra


    def mem_graph(self, mem_values,OUTPUT_GRAPH_FILES):
        pylab.plot(range(len(mem_values)), mem_values)
        pylab.xlabel('Count')
        pylab.ylabel('Value in KB')
        pylab.tick_params(axis='x', labelsize=8)
        pylab.tick_params(axis='y', labelsize=8)
        pylab.xticks(rotation=0)
        save_file = OUTPUT_GRAPH_FILES + 'MEM_PLOT_RESULT.png'
        pylab.savefig(save_file)
        print "Mem Graph Plot done"


    def user_graph_BE(self):
        result="pass"
        reason="pass"
        pdata = struct.unpack('{n}h'.format(n=self.d_len), self.data)
        pdata = np.array(pdata)
        w = np.fft.fft(pdata)
        f = np.fft.fftfreq(len(w))
        self.freqs=abs(f*self.rate)
        a=np.abs(w)/len(pdata)
        # print "Self.freqs=", self.graph_loc, self.freqs, len(self.freqs)
        np.append(self.freqs, 0)
        np.append(a, 0)
        self.final_freq_rec=[]
        self.rec_final_freq=[]
        self.rec_final_power=[]
        self.Fresult_check=[]
        self.Presult_check=[]
        rp_max,cnt, r_pow_max=0,0, 0

        while cnt<len(self.freqs):
            if a[cnt]==0:
                self.final_freq_rec.append(0)
            else:
                self.final_freq_rec.append(int(self.freqs[cnt]))
            cnt+=1
        cnt=0
        del_values=[]
        while cnt < 200:
            del_values.append(np.argmax(a))
            a[del_values[cnt]]=0
            cnt+=1


        max_cnt=int(max(a))
        print "Max_power=", max_cnt

        for j in del_values:
            a[j]= max_cnt

        cnt=0
        # print "final_freq_rec=", self.final_freq_rec[0],self.final_freq_rec[1], self.final_freq_rec[2]
        while cnt<(len(self.final_freq_rec)-1):
            if cnt>0:
                if self.final_freq_rec[cnt]==self.final_freq_rec[cnt+1]:
                    if r_pow_max < int(a[cnt]):
                        r_pow_max=int(a[cnt])
                else:
                    self.rec_final_freq.append(self.final_freq_rec[cnt])
                    self.rec_final_power.append(r_pow_max)
                    if r_pow_max>max_cnt:
                        max_cnt=r_pow_max
                    r_pow_max=0
            else:
                self.rec_final_freq.append(self.final_freq_rec[cnt])
                self.rec_final_power.append(max_cnt)
            cnt+=1

        if max_cnt >=2:
            cnt=0
            while cnt<len(self.rec_final_freq):
                if self.rec_final_power[cnt] >= max_cnt*0.5:
                    if self.rec_final_freq[cnt]%100==0:
                        self.Fresult_check.append(self.rec_final_freq[cnt])
                        self.Presult_check.append(self.rec_final_power[cnt])
                cnt+=1
            self.Fresult_check=self.Fresult_check[:len(self.Fresult_check)/2+1]
            self.Presult_check=self.Presult_check[:len(self.Presult_check)/2+1]
            self.recorded_freqs=self.Fresult_check
            # print "\nFrequencies=", self.Fresult_check
            if self.graph_loc==1:
                self.final_match = self.Fresult_check
                self.original_freqs = self.Fresult_check



            if self.graph_loc==2:
                hcnt, fcnt, pcnt, bcnt=0, 0, 0, 0
                fail_fre=[]
                bndry_fre=[]

                self.orig_max_frq=self.rate/2

                if self.user_remove_freq>0:
                    remove_freq=self.user_remove_freq
                else:
                    if self.rate <= 4000:
                        remove_freq=4
                    elif self.rate <= 8000:
                        remove_freq=8
                    elif self.rate <= 16000:
                        remove_freq=10
                    elif self.rate <= 24000:
                        remove_freq=12
                    elif self.rate <= 32000:
                        remove_freq=15
                    elif self.rate <= 40000:
                        remove_freq=18
                    elif self.rate <= 48000:
                        remove_freq=20
                    else:
                        remove_freq=4
                self.orig_threshold_frq= self.orig_max_frq-(remove_freq*100)

                print "self.orig_threshold_frq=", self.orig_threshold_frq
                while (remove_freq)>0:
                    for n in self.original_freqs:
                        if n > self.orig_threshold_frq:
                            print "Removing=",self.orig_threshold_frq, n
                            self.original_freqs.remove(n)
                    remove_freq-=1


                print "\nOriginal=", self.original_freqs
                print "\nRecorded=", self.recorded_freqs

                for n in self.original_freqs:
                    if n in self.recorded_freqs:
                        pcnt+=1
                    else:
                        fail_fre.append(n)
                        fcnt+=1

                for n in self.recorded_freqs:
                    if n >= self.orig_threshold_frq and n <= self.orig_max_frq:
                        bcnt+=1
                        bndry_fre.append(n)
                    elif n > self.orig_max_frq:
                        hcnt+=1
                    else:
                        pass


                print "\n"
                print "\noriginal_freqs", len(self.original_freqs)
                print "\nrecorded_freqs", len(self.recorded_freqs)
                print "\nPass Values=", pcnt
                print "\nFail Values=", fcnt
                print "\nBoundarry Values=", bcnt
                print "\nHarmonice Values=", hcnt
                print "\nValue=", pcnt, len(self.original_freqs)
                print "\nPercentage of Match ="+str(int((float(pcnt)/float(len(self.original_freqs)))*100))+"%"
                print "\n"


                if len(self.Fresult_check)>=(len(self.original_freqs)+len(self.original_freqs)/2):
                    result="fail"
                    reason="Too many components"
                elif (pcnt >= (len(self.original_freqs)-1)) and (pcnt <= (len(self.original_freqs))):
                    result = "pass"
                    reason ="All frequency components are present"
                elif (bcnt>0 and bcnt <3) and pcnt >= (len(self.original_freqs)/2):
                    result = "pass"
                    reason =str(bcnt)+" Boundary components missing..."+str(bndry_fre)
                else:
                    if len(fail_fre)<3:
                        result="pass"
                    else:
                        result="fail"
                    reason=str(fcnt)+" Missing frequency"+str(fail_fre)

                print result, reason
        else:
            print "Result=Fail, Max power is 0"

        if self.graph_loc==2:
            name = self.wav_file.split("/")
            lnth = len(name)
            name = self.wav_file.split("/")[lnth - 1].split(".")[0]
            save_file = self.audio_record+".png"
            pylab.savefig(save_file)
            pylab.gcf()
            pylab.gca()
            pylab.close('all')
            gc.get_referrers()
            gc.collect()
            # print "Saving the results...."


            try:
                print "\nGetting Pesq results..."
                cmd="./pesq "+str(self.audio_play)+" "+str(self.audio_record)+" +"+str(self.rate)+"\n"
                print "Cmd=", cmd
                out=os.popen(cmd).readlines()
                for line in out:
                    if "P.862 Prediction (Raw MOS, MOS-LQO):  = " in line:
                        MOS=line.split("P.862 Prediction (Raw MOS, MOS-LQO):  = ")[1].split("\n")[0].split("\t")
                        print "MOS=", MOS
                if "fail" not in result and float(MOS[0])>2 and float(MOS[1])>2:
                    result="pass"
                else:
                    result="fail"
                    if "All frequency components are present" in reason:
                        reason+=" May be noise is high"
                    reason+=" Board "+self.audio_record.split("/")[-1].split(".wav")[0]
                reason+=" "+ str(MOS)
            except:
                print "Couldn't get MOS value"
        return  result, reason


    def graph_plotBE(self,orig_file, out_put_file,  rate, user_call):
        self.rate=rate
        self.audio_record=out_put_file
        self.audio_play=orig_file
        self.user_remove_freq = user_call
        for n in range(2):
            self.graph_loc=n+1
            if self.graph_loc==1:
                self.wav_file=self.audio_play
            else:
                self.wav_file=self.audio_record
            self.rate,self.data=read(self.wav_file)
            self.numerical_graph()
            self.plotSpectru()
            self.freq_time_specgram()
            rs, ra=self.user_graph_2()
        return  rs, ra


    def new_canvas(self):
# This program creats a new canvas for plotting the image.
        global fig
        fig = plt.figure()
#*-----------------------------------------------------------------------------------------------------------------------------------------


    def pitch_graph(self, pitch_length, pitch_values, recorded):
# This program creats graph of pitch values.
        t = arange(0, pitch_length, 1)
        ax = fig.add_subplot(3, 2, self.graph_loc)
        ax.plot(t, pitch_values)
        grid("on")
        xlabel('Time (in ms)')
        ylabel('Pitch Values')
        axis('tight')

        if recorded == 1:
            title('Original')
        else:
            title('Recorded')
        return
#*-----------------------------------------------------------------------------------------------------------------------------------------


    def power_graph(self, power_length, power_values):
# This program creats graph of power values.
        t = arange(0, power_length, 1)
        bx = fig.add_subplot(3, 2, self.graph_loc)
        bx.plot(t, power_values)
        grid("on")
        xlabel('Power Length')
        ylabel('Power (in dB)')
        axis('tight')
        return
#*-----------------------------------------------------------------------------------------------------------------------------------------


    def fft_graph(self, fft_length, fft_values, square_values, recorded, counter):
# This program creats graph of power values.
        if square_values > 0:   # Square value of pitch sum.
            t = arange(0, fft_length, 1)
            cx = fig.add_subplot(3, 2, self.graph_loc)
            cx.semilogy(t, fft_values)
            grid("on")
            xlabel('FFT Samples')
            ylabel('FFT Values')
            title('FFT')
            axis('tight')
        else:
            t = arange(0, fft_length, 1)
            dx = fig.add_subplot(3, 2, self.graph_loc)
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
#*-----------------------------------------------------------------------------------------------------------------------------------------


    def save_wave(self, samples, counter):
        new_f = plt.figure()
        new_fig = new_f.add_subplot(1, 1, 1)
        new_fig.plot(samples)
        grid("on")
        new_fig.axis((0, 70000, -6000, 6000))

        if counter == 1: title = 'sout.wav'
        if counter == 2: title = 'rout.wav'
        save_loc = self.out_dir + 'wave_file_%s.png' % counter
        new_f.savefig(save_loc)
#*-----------------------------------------------------------------------------------------------------------------------------------------



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

s_file="/home/sreekanth/Documents/Output/"
#o_file='/home/sreekanth/Documents/audio/male_8k_short_orig.wav'
o_file='/home/sreekanth/Documents/audio/male_8k_orig.wav'
#r_file='/home/sreekanth/Documents/audio/male_8k_short_rec.wav'
r_file='/home/sreekanth/Documents/audio/male_8k_rec.wav'
print 10*"#"+"Start"+10*"#"
result_plot(o_file, r_file,s_file, 'multiple')
print 10*"#"+"End"+10*"#"
pl.close('all')
