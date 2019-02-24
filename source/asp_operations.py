##Audio & Speech Verification routines, base version From snack_operations


from Tkinter import*
import tkSnack
import wave
import numpy
from numpy.fft import fft
from math import sqrt
import string
import os
import time
import gc



root = Tk()
tkSnack.initializeSnack(root)
root.withdraw()

mysound = tkSnack.Sound()
wave_rec = 1



def calc_pitch(wav_file):
    mysound.read(wav_file)
    pitch_val = mysound.pitch()
    return pitch_val

# *-----------------------------------------------------------------------------------------------------------------------------------------


def calc_delay(in_wav, rec_wav):
    orig_pitch = calc_pitch(in_wav)
    rec_pitch = calc_pitch(rec_wav)
    corr_pitch = numpy.correlate(orig_pitch, rec_pitch, 'full')
    delay = int(len(corr_pitch) / 2) - numpy.argmax(corr_pitch)
    print "Delay =", delay
    return delay

# *-----------------------------------------------------------------------------------------------------------------------------------------


def process_wav_file(wav_file, recorded, out_text_path, debug):
    if recorded == 0:
        print "Processing Input File...."
    else:
        print "Processing Output File...."

    if recorded == 1:
        try:
            wav_pitch_vals = calc_pitch(wav_file)
            wav_pitch_len = len(wav_pitch_vals)
            wave_rec = 1
        except:
            wave_rec = 0
    else:
        wav_pitch_vals = calc_pitch(wav_file)
        wav_pitch_len = len(wav_pitch_vals)

    pitch_sum = 0
    temp_count = 0
    while temp_count < wav_pitch_len:
        pitch_sum += wav_pitch_vals[temp_count]
        temp_count += 1

    pitch_count = pitch_sum/temp_count
    print "Print pitch count = ", pitch_count
    pitch_count = pitch_sum / wav_pitch_len
    print "Print pitch count = ", pitch_count

    pitch_count, pitch_val = pitch_result(wav_pitch_len, wav_pitch_vals, recorded, out_text_path, debug)

## RMS calculation/fft plot/fft text write
    fft_wav = fft(wav_pitch_vals)
    wav_fft_vals = abs(fft_wav)
    wav_fft_len = len(wav_fft_vals)
    wav_rms = rms_calculate(wav_fft_len, wav_fft_vals, debug)

    return pitch_count, pitch_val, pitch_sum, wav_pitch_len, wav_rms

# *-----------------------------------------------------------------------------------------------------------------------------------------


def speech_compare(in_wav_file , rec_wav_file, COUNTER_MAIN, out_files_path, out_graph_path, debug):

    pitch_count_orig, pitch_val_orig, pitch_sum_orig, pitch_len_orig, inwav_rms = process_wav_file(in_wav_file, 0, out_files_path, debug)
    pitch_count_rec, pitch_val_rec, pitch_sum_rec, pitch_len_rec, recwav_rms = process_wav_file(rec_wav_file, 1, out_files_path, debug)

    pit_mat, rms_mat = calc_match_perc(inwav_rms, recwav_rms, pitch_sum_orig , pitch_sum_rec, out_files_path , debug)

    if wave_rec == 1:
        if debug == 1:
            print "Output Pitch Count = ", pitch_count_rec
            print "Output Pitch Value = ", pitch_val_rec
            print "Input Pitch Count = ", pitch_count_orig
            print "Input Pitch Value = ", pitch_val_orig

        last_blanks = pitch_len_rec - 50 ##modified to last 50 pitch values from last 100 values
        sum_last = 0
        while last_blanks < pitch_len_rec:
            sum_last += pitch_val_rec[last_blanks]
            last_blanks += 1

    ## calculating time delay b/w play and record
        delay_rec = (pitch_count_rec - pitch_count_orig) * 10
        print "Time delay between playing and recording = %s milli seconds" %delay_rec
        delay_rec_sec = delay_rec * 0.001
        print "Time delay between playing and recording = %f seconds" %delay_rec_sec
        reason="Audio exists"
        if debug == 1:
            print "Test End Time (12hr) :", time.strftime("%I:%M:%S %p", time.localtime())
        if 0 < pitch_count_rec and pitch_count_rec < (pitch_count_orig *0.8):
            result_file=open(out_files_path + "Fail_Result.txt", "a")
            result_file.write(str(COUNTER_MAIN))
            result_file.write("\t\t\t\tFail\n")
            result_file.close()
            reason="Noisy audio...."
            result="Fail"
        elif delay_rec_sec < -50:
            result_file=open(out_files_path + "Fail_Result.txt", "a")
            result_file.write(str(COUNTER_MAIN))
            result_file.write("\t\t\t\tFail\n")
            result_file.close()
            reason="Components seen before audio started...."
            result="Fail"
        elif sum_last > 50:
            result_file=open(out_files_path + "Fail_Result.txt", "a")
            result_file.write(str(COUNTER_MAIN))
            result_file.write("\t\t\t\tFail\n")
            result_file.close()
            print "SUM - 100 = ", sum_last
            reason="High audio gain, check gain setting(s)...."
            result="Fail"
        else:
            if pit_mat > 260 and rms_mat > 200:
                print "Condition 1"
                reason="Audio Gains/Noise is too high...."
                result="Fail"
                result_file=open(out_files_path + "Fail_Result.txt", "a")
                result_file.write(str(COUNTER_MAIN))
                result_file.write("\t\t\t\tFail\n")
                result_file.close()
            elif pit_mat < 80 and rms_mat < 80:
                print "Condition 2"
                reason="Components are below threshold...."
                result="Fail"
                result_file=open(out_files_path + "Fail_Result.txt", "a")
                result_file.write(str(COUNTER_MAIN))
                result_file.write("\t\t\t\tFail\n")
                result_file.close()
            elif pit_mat > 60 and rms_mat < 70:
                print "Condition 3"
                reason="Components are much below threshold...."
                result="Fail"
                result_file=open(out_files_path + "Fail_Result.txt", "a")
                result_file.write(str(COUNTER_MAIN))
                result_file.write("\t\t\t\tFail\n")
                result_file.close()
            elif pit_mat > 80 and rms_mat > 80 and pit_mat < 150 and rms_mat < 130:
                reason="Voice/Speech exists...."
                result="Pass"
                result_file=open(out_files_path + "Fail_Result.txt", "a")
                result_file.write(str(COUNTER_MAIN))
                result_file.write("\t\t\t\tPass\n")
                result_file.close()
            elif pit_mat > 80 and rms_mat > 80 and pit_mat < 260.01 and rms_mat < 200.01:
                reason="Voice/Speech exists...."
                result="Pass"
                result_file=open(out_files_path + "Fail_Result.txt", "a")
                result_file.write(str(COUNTER_MAIN))
                result_file.write("\t\t\t\tPass\n")
                result_file.close()
            elif pit_mat > 65 and rms_mat > 90 and pit_mat < 150 and rms_mat < 200:
                reason="Voice/Speech exists...."
                result="Pass"
                result_file=open(out_files_path + "Fail_Result.txt", "a")
                result_file.write(str(COUNTER_MAIN))
                result_file.write("\t\t\t\tPass\n")
                result_file.close()
            else:
                print "Condition 4", pit_mat, rms_mat
                reason="Faulty audio, please check the Graphs and audio files...."
                result="Fail"
                result_file=open(out_files_path + "Fail_Result.txt", "a")
                result_file.write(str(COUNTER_MAIN))
                result_file.write("\t\t\t\tFail\n")
                result_file.close()
    else:
        print "Condition 4"
        reason="Faulty audio, please check the supporting files...."
        result="Fail"
        result_file=open(out_files_path + "Fail_Result.txt", "a")
        result_file.write(str(COUNTER_MAIN))
        result_file.write("\t\t\t\tFail\n")
        result_file.close()

    if rec_wav_file:
        print "Inputs=",in_wav_file, rec_wav_file, out_files_path, COUNTER_MAIN
        graph_plot.result_plot(in_wav_file, rec_wav_file, out_files_path, COUNTER_MAIN)

    mysound.destroy()
##    root.destroy()
##    root.quit()

    del par1, par2, PITCH_LENGTH,PITCH_VALUES,OUTPUT_TEXT_FILES,DEBUG, REC_FFT_LENGTH,REC_FFT_VALUES
    gc.get_referrers()
    gc.collect()
    return result,reason


# TEST_CASE_RESULT_IS_sin,TEST_CASE_OBSERVATION_IS_sin=snack_operations.snack_work(sin,DEBUG,sout,COUNTER_MAIN,op_fold,op_fold)


# *-----------------------------------------------------------------------------------------------------------------------------------------

def rms_calculate(fft_len, fft_vals, debug):
    debug = int(debug)
    count = 0
    sum_value = 0
    while (count < fft_len):
        if fft_vals[count] > 0:
            root = sqrt(fft_vals[count])
            sum_value += root
        count = count + 1
    mean = sum_value / count
    rms = mean * mean
    return rms

# *-----------------------------------------------------------------------------------------------------------------------------------------

def pitch_result(pitch_len, pitch_vals, recorded, out_text_path, debug):
    debug = int(debug)
    count_pitch = 0
    pitch_stop_flag = 0
    in_pitch_cnt = 0
    in_pitch_val = 0
    out_pitch_cnt = 0
    out_pitch_val = 0

    if recorded == 0:
        path = out_text_path + 'inputpitch.txt'
        if debug == 1:
            print path
        text_file = open(path, "a")
    else:
        path = out_text_path + 'outputpitch.txt'
        if debug == 1:
            print path
        text_file = open(path, "a")

    while (count_pitch < pitch_len):
        text_file.write("fft no\t\tfft abs value")
        text_file.write("\n")
        text_file.write(" ")
        text_file.write(str(count_pitch))
        text_file.write("----------------->")

        if pitch_stop_flag == 0:
            if pitch_vals[count_pitch] != 0:
                pitch_stop_flag = 1
                if debug == 1:
                    print "pitch_stop_counter", pitch_stop_flag
                if recorded == 0:
                    in_pitch_cnt = count_pitch
                    in_pitch_val = pitch_vals[count_pitch]
                    print "Input pitch count    ::", in_pitch_cnt
                    print "Input Pitch Value    ::", in_pitch_val
                else:
                    out_pitch_cnt = count_pitch
                    out_pitch_val = pitch_vals[count_pitch]
                    print "Output pitch count   ::", out_pitch_cnt
                    print "Output Pitch Value   ::", out_pitch_val

        text_file.write(str(pitch_vals[count_pitch]))
        text_file.write("\n\n")
        count_pitch = count_pitch + 1

    if debug == 1:
        print "Recorded = ", recorded

    if recorded == 0:
        return in_pitch_cnt, in_pitch_val
    elif recorded == 1:
        return out_pitch_cnt, out_pitch_val

# *-----------------------------------------------------------------------------------------------------------------------------------------

def power_result_write(epower_length, epower_values, recorded, out_text_path, debug):
    debug = int(debug)
    count_power = 0
    if recorded == 0:
        text_file = open(out_text_path + 'input-power-values.txt', "a")
    else:
        text_file = open(out_text_path + 'output-power-values.txt', "a")
    while (count_power < epower_length):
        text_file.write("sample no\t\tpower value")
        text_file.write("\n")
        text_file.write(" ")
        text_file.write(str(count_power))
        text_file.write("----------------->")
        text_file.write(str(epower_values[count_power]))
        text_file.write("\n\n")
        count_power = count_power + 1

# *-----------------------------------------------------------------------------------------------------------------------------------------


def fft_result_write(fft_length, fft_values, recorded, out_text_path, debug):
    debug = int(debug)
    count_fft = 0

    if recorded == 0:
        text_file = open(out_text_path + 'input-abs-values.txt', "a")
    else:
        text_file = open(out_text_path + 'output-abs-values.txt', "a")
    while (count_fft < fft_length):
        text_file.write("fft no\t\tfft abs value")
        text_file.write("\n")
        text_file.write(" ")
        text_file.write(str(count_fft))
        text_file.write("----------------->")
        text_file.write(str(fft_values[count_fft]))
        text_file.write("\n\n")
        count_fft = count_fft + 1

# *-----------------------------------------------------------------------------------------------------------------------------------------


def calc_match_perc(rms_in_wav, rms_rec_wav, pitch_sum_inwav , pitch_sum_recwav, text_out_path , debug):
    debug = int(debug)
    rms_match = 0.0
    if rms_rec_wav == 0:
        rms_match = 0.0
    else:
        rms_match = rms_in_wav *100 / rms_rec_wav
        if rms_match > 300:
            if debug == 1:
                print "Check if any other audio is playing...."
            reason = "Check if any other audio is playing...."
            result = "Fail"
            return result,reason
        else:
            if rms_match > 100:
                noise = rms_match - 100
                rms_match = rms_match - noise
                print "RESULTS"
                print "RMS_MATCH = ", rms_match
                print "NOISE = ", noise/4
            else :
                if rms_match < 50:
                    if debug == 1:
                        print "NOISE = ",rms_match
                else:
                    if debug == 1:
                        print "RMS_MATCH = ", rms_match
                        print "Noise is negligible...."
            path = text_out_path + 'final_result.txt'
            text_file = open(path, "a")
            text_file.write("RMS_MATCH = ")
            text_file.write(str(rms_match))
            text_file.write("\n")
            text_file.close()

    if pitch_sum_recwav == 0:
        pitch_match = 0
    else:
        pitch_match = pitch_sum_inwav * 100 / pitch_sum_recwav

    if pitch_match < 50:
        print "Test fails...."
    else:
        print "###########################################################################"
        if pitch_match > 300:
            print "Check input...."
        else:
            if pitch_match > 100:
                noise_pitch = pitch_match - 100
                print "PITCH_MATCH = 100"
                pitch_match = pitch_match - noise_pitch
                print "NOISE_PITCH = ", noise_pitch/4
                print "RMS_MATCH = ", rms_match

            else:
                print "RMS_MATCH = ", rms_match
                print "PITCH_MATCH = ", pitch_match

    print "###########################################################################"
    path = text_out_path + 'final_result.txt'
    text_file = open(path, "a")
    text_file.write("PITCH_MATCH = ")
    text_file.write(str(pitch_match))
    text_file.write("\n")
    text_file.close()
    return pitch_match, rms_match



## image_plot_spectrum.py



import pylab
import time
from scipy import fft, arange
import numpy as np
from scipy.io.wavfile import read
import gc
import struct
from math import ceil, pi
from matplotlib import mlab
from scipy.fftpack import fft, fftfreq, fftshift
import os
from scipy.signal import get_window
from array import array
import sys
import random
class image_draw():
    def __init__(self):
        self.graph_loc=1
        self.final_result_freq_orig=[]
        self.final_result_pow_freq_orig=[]
        self.orig_frq_bup=[]
        self.ori_list=[]
        self.fre_list=[]
        self.pow_list=[]
        self.final_match=[]
        self.data=[]
        self.orig_max_frq=0
        self.rate=8000
        self.debug_flag=1
        if self.debug_flag:
            self.graph_cnt=4
        else:
            self.graph_cnt=3


    def MOS_graph(self, res_dic):
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


    def numerical_graph(self):
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


    def plotSpectru(self):
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


    def myround(self, x, base=100):
        return base * round(x / base)

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

    def graph_plot(self, idraw, orig_file, rec_file, OUTPUT_GRAPH_FILES, seq, chirp):
        self.rec_file=rec_file
        self.OUTPUT_GRAPH_FILES=OUTPUT_GRAPH_FILES
        self.seq=seq
        self.orig_file=orig_file
        self.chirp=chirp
        self.draw=idraw

        for n in range(2):

            self.graph_loc=n+1

            if self.graph_loc==1:
                self.wav_file=self.orig_file
            else:
                self.wav_file=self.rec_file

            self.rate,self.data=read(self.wav_file)

            print "file, rate, data=",self.wav_file, self.rate, self.data.dtype

            self.draw.numerical_graph()

            self.draw.plotSpectru()

            self.draw.freq_time_specgram()

            rs, ra=self.draw.user_graph_2()


        return  rs, ra



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

