#!/usr/bin/env python
# -*- coding: utf-8 -*-


##########################################################################################################################################
##########################################################################################################################################
## File              :: asv_routines.py
## Description       :: Audio, speech verification routines/functions using tkSnack.
## Developer         :: Sreekanth S
## Version           :: v2.0
## Release Date      :: 28/03/2019
## Changes made      :: Created a class based API.
## Changes made Date :: 23/08/2018
## Changes made by   :: Sreekanth S
##########################################################################################################################################
##########################################################################################################################################



from Tkinter import*
import tkSnack

root=Tk()
tkSnack.initializeSnack(root)
root.withdraw()

import wave
import os
import string
import time
import gc

import numpy
from math import sqrt
from numpy.fft import fft

import vaca_graph_plot


class asv:
    def __init__(self, in_file, out_file, op_fold, counter, debug):
        self.in_wav = in_file
        self.rec_wav = out_file
        self.out_path = op_fold
        self.debug = debug
        self.test_count = counter


    def delay_work(self):
        source = tkSnack.Sound()
        source.read(self.in_wav)
        sink = tkSnack.Sound()
        sink.read(self.rec_wav)
        orig = source.pitch()
        rec = sink.pitch()
        corr = numpy.correlate(orig, rec, 'full')
        delay = int(len(corr) / 2) - numpy.argmax(corr)
        print "Delay = ", delay
        return delay
#*-----------------------------------------------------------------------------------------------------------------------------------------


    def speech_analysis(self):

##  Processing Original/Input Wave File

        source = tkSnack.Sound()
        source.read(self.in_wav)
        source_pitchvals = source.pitch()
        source_pitchlen = len(source_pitchvals)
        source_pitchsum = 0
        temp_count = 0

## Pitch Calculation, Pitch Text Write of Input Wave File

        while temp_count < source_pitchlen:
            source_pitchsum = source_pitchsum + source_pitchvals[temp_count]
            temp_count += 1
        source_pitchcnt = source_pitchsum/temp_count
        source_pitchcount, source_pitchvalues = self.pitch_result(source_pitchlen, source_pitchvals, 0)

## RMS calculation of FFT of Input Wave file

        source_raw_fft = fft(source_pitchvals)
        source_fft_values = abs(source_raw_fft)
        source_fft_length = len(source_fft_values)
        sourceRMS = self.calculateRMS(source_fft_length, source_fft_values)

        source.destroy()

## Processing Recorded Wave File

        sink = tkSnack.Sound()
        sink.read(self.rec_wav)

## Pitch Calculation, Pitch Text Write of Recorded Wave File

        sink_pitchvals = sink.pitch()
        try:
            sink_pitchlen = len(sink_pitchvals)
            wave_rec = 1
        except:
            wave_rec = 0

        if wave_rec == 1:
            sink_pitchsum = 0
            temp_count = 0
            while temp_count < sink_pitchlen:
                sink_pitchsum = sink_pitchsum + sink_pitchvals[temp_count]
                temp_count += 1
            sink_pitchcnt = sink_pitchsum / temp_count
            sink_pitchcount, sink_pitchvalues = self.pitch_result(sink_pitchlen, sink_pitchvals, 1)

## RMS calculation of FFT of Input Wave file

            sink_raw_fft = fft(sink_pitchvals)
            sink_fft_values = abs(sink_raw_fft)
            sink_fft_length = len(sink_fft_values)
            sinkRMS = self.calculateRMS(sink_fft_length, sink_fft_values)

## RMS match and Pitch match percentage calculation

            percRMS, percPITCH = self.match_result(sourceRMS, sinkRMS, source_pitchsum, sink_pitchsum)

            if self.debug == 1:
                print "Output_Pitch_Count = ", sink_pitchcount
                print "Output_Pitch_Value = ", sink_pitchvalues
                print "Input_Pitch_Count = ", source_pitchcount
                print "Input_Pitch_Value = ", source_pitchvalues

## Modified to last 50 pitch values from last 100 values

            lastBlanks = sink_pitchlen - 50
            sumLastSink = 0
            while lastBlanks < sink_pitchlen:
                sumLastSink += sink_pitchvals[lastBlanks]
                lastBlanks += 1

## Calculating the time delay b/w play and record

            delay_rec = (sink_pitchcount - source_pitchcount) * 10
            print "Time delay between playing and recording = %s m sec" %delay_rec
            delay_rec = delay_rec * 0.001
            print "Time delay between playing and recording = %f sec" %delay_rec
            reason = "Audio/Speech exists"
            if self.debug == 1:
                print "Test End Time (12hr) :", time.strftime("%I:%M:%S %p", time.localtime())
            if (0 < sink_pitchcount) and (sink_pitchcount < (source_pitchcount)*(0.8)):
                result_file=open(self.out_path + "Fail_Result.txt", "a")
                result_file.write(str(self.test_count))
                result_file.write("\t\t\t\tFail\n")
                result_file.close()
                reason="Noisy audio...."
                result="Fail"

            elif delay_rec < -50:
                result_file=open(self.out_path + "Fail_Result.txt", "a")
                result_file.write(str(self.test_count))
                result_file.write("\t\t\t\tFail\n")
                result_file.close()
                reason="Components seen before audio started...."
                result="Fail"

            elif sumLastSink > 50:
                result_file=open(self.out_path + "Fail_Result.txt", "a")
                result_file.write(str(self.test_count))
                result_file.write("\t\t\t\tFail\n")
                result_file.close()
                print "SUM-50 = ", sumLastSink
                reason="High audio gain, check gain setting(s)...."
                result="Fail"

            else:
                if percPITCH > 260 and percRMS > 200:
                    print "Condition 1"
                    reason="Audio Gains/Noise is too high...."
                    result="Fail"
                    result_file=open(self.out_path + "Fail_Result.txt", "a")
                    result_file.write(str(self.test_count))
                    result_file.write("\t\t\t\tFail\n")
                    result_file.close()

                elif percPITCH < 80 and percRMS < 80:
                    print "Condition 2"
                    reason="Components are below threshold...."
                    result="Fail"
                    result_file=open(self.out_path + "Fail_Result.txt", "a")
                    result_file.write(str(self.test_count))
                    result_file.write("\t\t\t\tFail\n")
                    result_file.close()

                elif percPITCH > 60 and percRMS < 70:
                    print "Condition 3"
                    reason="Components are much below threshold...."
                    result="Fail"
                    result_file=open(self.out_path + "Fail_Result.txt", "a")
                    result_file.write(str(self.test_count))
                    result_file.write("\t\t\t\tFail\n")
                    result_file.close()

                elif percPITCH > 80 and percRMS > 80 and percPITCH < 150 and percRMS < 130:
                    reason="Voice/Speech exists...."
                    result="Pass"
                    result_file=open(self.out_path + "Fail_Result.txt", "a")
                    result_file.write(str(self.test_count))
                    result_file.write("\t\t\t\tPass\n")
                    result_file.close()

                elif percPITCH > 80 and percRMS > 80 and percPITCH < 260.01 and percRMS < 200.01:
                    reason="Voice/Speech exists...."
                    result="Pass"
                    result_file=open(self.out_path + "Fail_Result.txt", "a")
                    result_file.write(str(self.test_count))
                    result_file.write("\t\t\t\tPass\n")
                    result_file.close()

                elif percPITCH > 65 and percRMS > 90 and percPITCH < 150 and percRMS < 200:
                    reason="Voice/Speech exists...."
                    result="Pass"
                    result_file=open(self.out_path + "Fail_Result.txt", "a")
                    result_file.write(str(self.test_count))
                    result_file.write("\t\t\t\tPass\n")
                    result_file.close()

                else:
                    print "Condition 4", percPITCH, percRMS
                    reason="Faulty audio, please check the Graphs and audio files...."
                    result="Fail"
                    result_file=open(self.out_path + "Fail_Result.txt", "a")
                    result_file.write(str(self.test_count))
                    result_file.write("\t\t\t\tFail\n")
                    result_file.close()

        else:
            print "Condition 4"
            reason="Faulty audio, please check the supporting files...."
            result="Fail"
            result_file=open(self.out_path + "Fail_Result.txt", "a")
            result_file.write(str(self.test_count))
            result_file.write("\t\t\t\tFail\n")
            result_file.close()

        print "Inputs = ",INPUT_WAVE_FILE, OUTPUT_WAVE_FILES, OUTPUT_GRAPH_FILES, self.test_count
        vaca_graph_plot.result_plot(INPUT_WAVE_FILE, OUTPUT_WAVE_FILES, OUTPUT_GRAPH_FILES, self.test_count)

        sink.destroy()
    ##    root.destroy()
    ##    root.quit()

        del sink_raw_fft, sink_fft_values, sink_pitchvalues, sink_pitchvals, source_raw_fft, source_fft_values, source_pitchvalues, source_pitchvals
        gc.get_referrers()
        gc.collect()
        return result, reason
#*-----------------------------------------------------------------------------------------------------------------------------------------


    def inout_gain_levels(self):
        print "Getting the gain levels of input and output files...."
# Use 'SoX' command sox <filename>.wav -n stats to get dB levels (most likely its 'Pk lev dB')
#*-----------------------------------------------------------------------------------------------------------------------------------------


    def pitch_result(self, pitchlen, pitchvalues, recorded):
        count_pitch = 0
        pitch_stop_flag = 0
        out_pitch_count = 0
        out_pitch_value = 0

        if recorded == 0:
            path = self.out_path + 'inputpitch.txt'
            if self.debug == 1:
                print path
            text_file = open(path, "a")
        else:
            path = self.out_path + 'outputpitch.txt'
            if self.debug == 1:
                print path
            text_file = open(path, "a")

        while (count_pitch < pitchlen):
            text_file.write("fft no\t\tfft abs value")
            text_file.write("\n")
            text_file.write(" ")
            text_file.write(str(count_pitch))
            text_file.write("----------------->")

            if pitch_stop_flag == 0:
                if pitchvalues[count_pitch] != 0:
                    pitch_stop_flag = 1
                    if self.debug == 1:
                        print "pitch_stop_counter", pitch_stop_flag
                    if recorded == 0:
                        in_pitch_count = count_pitch
                        in_pitch_value = pitchvalues[count_pitch]
                        print "Input pitch count    ::", in_pitch_count
                        print "Input Pitch Value    ::", in_pitch_value
                    elif recorded == 1:
                        out_pitch_count = count_pitch
                        out_pitch_value = pitchvalues[count_pitch]
                        print "Output pitch count   ::", out_pitch_count
                        print "Output Pitch Value   ::", out_pitch_value

            text_file.write(str(pitchvalues[count_pitch]))
            text_file.write("\n\n")
            count_pitch = count_pitch + 1

        if recorded == 0:
            return in_pitch_count, in_pitch_value
        elif recorded == 1:
            if self.debug == 1:
                print "recorded = ", recorded
            return out_pitch_count, out_pitch_value
#*-----------------------------------------------------------------------------------------------------------------------------------------


    def calculateRMS(fft_len, fft_vals):
        count = 0
        sum_value = 0
        while (count < fft_len):
            if fft_vals[count] > 0:
                root_fft = sqrt(fft_vals[count])
                sum_value = sum_value + root_fft
            count += 1
        mean = sum_value / count
        square = mean * mean
        return square
#*-----------------------------------------------------------------------------------------------------------------------------------------


    def match_result(self, inRMS, recRMS, in_pitch_sum, out_pitch_sum):
        percRMSmatch = 0
        percPITCHmatch = 0
        res_path = self.out_path + 'final_result.txt'
        if recRMS == 0:
            percRMSmatch = 0.0
        else:
            percRMSmatch = inRMS * 100 / recRMS
            if percRMSmatch > 300:
                if self.debug == 1:
                    print "Check if any other audio is playing........."
                reason = "Check if any other audio is playing........."
                result = "Fail"
                return result,reason
            else:
                if percRMSmatch > 100:
                    noise_rmsperc = percRMSmatch - 100
                    percRMSmatch -= noise_rmsperc
                    print "RESULTS"
                    print "RMS_MATCH = ", percRMSmatch
                    print "NOISE = ", noise_rmsperc/4
                else :
                    if percRMSmatch < 50:
                        if self.debug == 1:
                            print "NOISE = ", percRMSmatch
                    else:
                        if self.debug == 1:
                            print "RMS_MATCH = ", percRMSmatch
                            print "Noise is negligible...."
                text_file = open(res_path, "a")
                text_file.write("RMS_MATCH = ")
                text_file.write(str(percRMSmatch))
                text_file.write("\n")
                text_file.close()

        if out_pitch_sum==0:
            percPITCHmatch = 0
        else:
            percPITCHmatch = in_pitch_sum * 100 / out_pitch_sum

        if percPITCHmatch < 50 :
            print "Test fails....."
        else:
            print "###########################################################################"
            if percPITCHmatch > 300:
                    print "check input...."
            else:
                if percPITCHmatch > 100:
                    noise_pitchperc = percPITCHmatch -100
                    print "PITCH_MATCH = 100"
                    percPITCHmatch -= noise_pitchperc
                    print "NOISE_PITCH = ", noise_pitchperc/4
                else:
                    print "PITCH_MATCH = ",percRMSmatch

        print "###########################################################################"
        text_file = open(res_path, "a")
        text_file.write("PITCH_MATCH = ")
        text_file.write(str(percPITCHmatch))
        text_file.write("\n")
        text_file.close()
        return percPITCHmatch, percRMSmatch
#*-----------------------------------------------------------------------------------------------------------------------------------------


    def power_result_write(self, power_length, power_values, recorded):
        count_power = 0
        if recorded == 0:
            text_file = open(self.out_path + 'input-power-values.txt', "a")
        else:
            text_file = open(self.out_path + 'output-power-values.txt', "a")
        while (count_power < power_length):
            text_file.write("sample no\t\tpower value")
            text_file.write("\n")
            text_file.write(" ")
            text_file.write(str(count_power))
            text_file.write("----------------->")
            text_file.write(str(power_values[count_power]))
            text_file.write("\n\n")
            count_power = count_power + 1
#*-----------------------------------------------------------------------------------------------------------------------------------------


    def fft_result_write(self, fft_length , fft_values, recorded):
        count_fft = 0
        if recorded == 0:
            text_file = open(self.out_path + 'input-abs-values.txt', "a")
        else:
            text_file = open(self.out_path + 'output-abs-values.txt', "a")
        while (count_fft < fft_length):
            text_file.write("fft no\t\tfft abs value")
            text_file.write("\n")
            text_file.write(" ")
            text_file.write(str(count_fft))
            text_file.write("----------------->")
            text_file.write(str(fft_values[count_fft]))
            text_file.write("\n\n")
            count_fft = count_fft + 1
#*-----------------------------------------------------------------------------------------------------------------------------------------


##iter=0
##
##while iter<100:
##    DEBUG=1
##    sin='C:\\automation\Voice_Test_Tool\Input\sirtest.wav'
##    sout='C:\\automation\Voice_Test_Tool\Output\SIR_TEST_REC.1.wav'
##    op_fold="C:\\automation\Voice_Test_Tool\Output\\"
##    op_fold="C:\\automation\Voice_Test_Tool\Output\\"
##    print 50*"*"
##    snack_work(sin,DEBUG,sout,iter,op_fold,op_fold)
##    iter+=1
