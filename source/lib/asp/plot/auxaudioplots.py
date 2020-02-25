


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


# TODO: Compare and add usable fucntions or statements to wavgraphplot.py and remove this file.


class graph_plot:
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

        if self.graphloc==1:
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

        if self.graphloc==2:
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
            self.orig_max_frq = customroundoff(self.freqs[idx])
            print "Max frequency =", self.orig_max_frq

###########################################
        if self.debug_flag:
            pylab.subplot(self.graph_cnt,2,self.graphloc+6)
##            pylab.plot(self.freqs, a)
            pylab.plot(self.Fresult_check, self.Presult_check)

            pylab.tick_params(axis='x', labelsize=8)
            pylab.tick_params(axis='y', labelsize=8)
            pylab.xticks(rotation=0)
            if self.graphloc==1:
                pylab.xlabel('Frequecy')
                pylab.ylabel('Power')
            print "Graph Plot done 5"

        if self.graphloc==2:
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


    def user_graph_BE(self):
        result="pass"
        reason="pass"
        pdata = struct.unpack('{n}h'.format(n=self.d_len), self.data)
        pdata = np.array(pdata)
        w = np.fft.fft(pdata)
        f = np.fft.fftfreq(len(w))
        self.freqs=abs(f*self.rate)
        a=np.abs(w)/len(pdata)
        # print "Self.freqs=", self.graphloc, self.freqs, len(self.freqs)
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
            if self.graphloc==1:
                self.final_match = self.Fresult_check
                self.original_freqs = self.Fresult_check



            if self.graphloc==2:
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

        if self.graphloc==2:
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
            self.graphloc=n+1
            if self.graphloc==1:
                self.wav_file=self.audio_play
            else:
                self.wav_file=self.audio_record
            self.rate,self.data=readWav(self.wav_file)
            self.numerical_graph()
            self.plotSpectru()
            self.freq_time_specgram()
            rs, ra=self.user_graph_2()
        return  rs, ra
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
