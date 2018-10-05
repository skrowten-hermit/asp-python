##Audio & Speech Verification routines


### From snack_operations



from Tkinter import*
import tkSnack
root=Tk()
tkSnack.initializeSnack(root)
root.withdraw()
import wave
##import graph_plot_voip
import os
import string
import time

import numpy

import gc

import graph_plot
import result_write
import rms_calculate
import result_calculate_voip
from numpy.fft import fft

##from pympler.tracker import SummaryTracker
##from mem_top import mem_top
##import logging
##from memory_profiler import profile
##fp1=open('snack.log','a+')
##@profile(stream=fp1)

def delay_work(INPUT_WAVE_FILE,OUTPUT_WAVE_FILES):
    mysound=tkSnack.Sound()
    mysound.read(INPUT_WAVE_FILE)
    mysound2 = tkSnack.Sound()
    mysound2.read(OUTPUT_WAVE_FILES)
    orig=mysound.pitch()
    rec=mysound2.pitch()
    corr = numpy.correlate(orig, rec, 'full')
    delay = int(len(corr) / 2) - numpy.argmax(corr)
    print "Delay =", delay
    return delay

def snack_work(INPUT_WAVE_FILE,DEBUG,OUTPUT_WAVE_FILES,COUNTER_MAIN,OUTPUT_TEXT_FILES,OUTPUT_GRAPH_FILES):
##    log_in=10*"#"+"Snack_%s"+10*"#"
##    fp1.write(log_in)

##   processing original wave file
    mysound=tkSnack.Sound()
    mysound.read(INPUT_WAVE_FILE)

## pitch calculation/pitch plot/pitch text write
    PITCH_VALUES= mysound.pitch()
    PITCH_LENGTH=len(PITCH_VALUES)

    PITCH_SUM_ORIG=0
    temp_count=0
    while temp_count<PITCH_LENGTH:
        PITCH_SUM_ORIG=PITCH_SUM_ORIG+PITCH_VALUES[temp_count]
        temp_count=temp_count+1
    pitch_count_orig=PITCH_SUM_ORIG/temp_count
    Pitch_Count_Orig,Pitch_Value_Orig=result_write.pitch_result(PITCH_LENGTH,PITCH_VALUES,0,OUTPUT_TEXT_FILES,DEBUG)

## RMS calculation/fft plot/fft text write
    e= fft(PITCH_VALUES)
    FFT_VALUES=abs(e)
    FFT_LENGTH=len(FFT_VALUES)
    SQUARE_ORIG=rms_calculate.RMS_FIND(FFT_LENGTH,FFT_VALUES,DEBUG)

    mysound.destroy()

## processing recorded wave file
    mysound=tkSnack.Sound()
    Rec_path=OUTPUT_WAVE_FILES
    mysound.read(Rec_path)
    if DEBUG==1:
        print "Rec_path=",Rec_path

## pitch calculation/pitch plot/pitch text write
    REC_PITCH_VALUES= mysound.pitch()
    try:
        REC_PITCH_LENGTH=len(REC_PITCH_VALUES)
        wave_rec=1
    except:
        wave_rec=0
    if wave_rec==1:
        PITCH_SUM_REC=0
        temp_count=0
        while temp_count<REC_PITCH_LENGTH:
                PITCH_SUM_REC=PITCH_SUM_REC+REC_PITCH_VALUES[temp_count]
                temp_count=temp_count+1
        pitch_count_rec=PITCH_SUM_REC/temp_count
        Pitch_Count_Rec,Pitch_Value_Rec=result_write.pitch_result(REC_PITCH_LENGTH,REC_PITCH_VALUES,1,OUTPUT_TEXT_FILES,DEBUG)

    ## RMS calculation/fft plot/fft text write
        e= fft(REC_PITCH_VALUES)
        REC_FFT_VALUES=abs(e)
        REC_FFT_LENGTH=len(REC_FFT_VALUES)
        SQUARE_REC=rms_calculate.RMS_FIND(REC_FFT_LENGTH,REC_FFT_VALUES,DEBUG)

    ## final step RMS match and pitch match calculation
        par1,par2=result_calculate_voip.Print_result(SQUARE_REC,SQUARE_ORIG,PITCH_SUM_ORIG,PITCH_SUM_REC,OUTPUT_TEXT_FILES,DEBUG)

        if DEBUG==1:
            print "Output_Pitch_Count=",Pitch_Count_Rec
            print "Output_Pitch_Value=",Pitch_Value_Rec
            print "Input_Pitch_Count=",Pitch_Count_Orig
            print "Input_Pitch_Value=",Pitch_Value_Orig

        Last_blanks=REC_PITCH_LENGTH-50 ##modified to last 50 pitch values from last 100 values
        Sum_last=0
        while Last_blanks<REC_PITCH_LENGTH:
            Sum_last+=REC_PITCH_VALUES[Last_blanks]
            Last_blanks+=1

    ## calculating time delay b/w play and record
        delay_rec=(Pitch_Count_Rec-Pitch_Count_Orig)*10
        print "Time delay between playing and recording = %s m sec"% delay_rec
        delay_rec_sec = delay_rec*0.001
        print "Time delay between playing and recording = %f sec"% delay_rec_sec
        reason="Audio exists"
        if DEBUG==1:
            print "Test End Time (12hr) :", time.strftime("%I:%M:%S %p", time.localtime())
        if 0 < Pitch_Count_Rec and Pitch_Count_Rec < ((Pitch_Count_Orig)*(0.8)):
            result_file=open(OUTPUT_TEXT_FILES+"Fail_Result.txt", "a")
            result_file.write(str(COUNTER_MAIN))
            result_file.write("\t\t\t\tFail\n")
            result_file.close()
            reason="Noisy audio...."
            result="Fail"

        elif delay_rec_sec<-50:
            result_file=open(OUTPUT_TEXT_FILES+"Fail_Result.txt", "a")
            result_file.write(str(COUNTER_MAIN))
            result_file.write("\t\t\t\tFail\n")
            result_file.close()
            reason="Components seen before audio started...."
            result="Fail"

        elif Sum_last>50:
            result_file=open(OUTPUT_TEXT_FILES+"Fail_Result.txt", "a")
            result_file.write(str(COUNTER_MAIN))
            result_file.write("\t\t\t\tFail\n")
            result_file.close()
            print "SUM-100=",Sum_last
            reason="High audio gain, check gain setting(s)...."
            result="Fail"

        else:
            if par1>260 and par2 > 200:
                print "Condition 1"
                reason="Audio Gains/Noise is too high...."
                result="Fail"
                result_file=open(OUTPUT_TEXT_FILES+"Fail_Result.txt", "a")
                result_file.write(str(COUNTER_MAIN))
                result_file.write("\t\t\t\tFail\n")
                result_file.close()

            elif par1<80 and par2<80:
                print "Condition 2"
                reason="Components are below threshold...."
                result="Fail"
                result_file=open(OUTPUT_TEXT_FILES+"Fail_Result.txt", "a")
                result_file.write(str(COUNTER_MAIN))
                result_file.write("\t\t\t\tFail\n")
                result_file.close()

            elif par1>60 and par2<70:
                print "Condition 3"
                reason="Components are much below threshold...."
                result="Fail"
                result_file=open(OUTPUT_TEXT_FILES+"Fail_Result.txt", "a")
                result_file.write(str(COUNTER_MAIN))
                result_file.write("\t\t\t\tFail\n")
                result_file.close()

            elif par1>80 and par2 >80 and par1<150 and par2<130:
                reason="Voice/Speech exists...."
                result="Pass"
                result_file=open(OUTPUT_TEXT_FILES+"Fail_Result.txt", "a")
                result_file.write(str(COUNTER_MAIN))
                result_file.write("\t\t\t\tPass\n")
                result_file.close()

            elif par1>80 and par2>80 and par1<260.01 and par2<200.01:
                reason="Voice/Speech exists...."
                result="Pass"
                result_file=open(OUTPUT_TEXT_FILES+"Fail_Result.txt", "a")
                result_file.write(str(COUNTER_MAIN))
                result_file.write("\t\t\t\tPass\n")
                result_file.close()

            elif par1>65 and par2>90 and par1 <150 and par2<200:
                reason="Voice/Speech exists...."
                result="Pass"
                result_file=open(OUTPUT_TEXT_FILES+"Fail_Result.txt", "a")
                result_file.write(str(COUNTER_MAIN))
                result_file.write("\t\t\t\tPass\n")
                result_file.close()

            else:
                print "Condition 4", par1, par2
                reason="Faulty audio, please check the Graphs and audio files...."
                result="Fail"
                result_file=open(OUTPUT_TEXT_FILES+"Fail_Result.txt", "a")
                result_file.write(str(COUNTER_MAIN))
                result_file.write("\t\t\t\tFail\n")
                result_file.close()

    else:
        print "Condition 4"
        reason="Faulty audio, please check the supporting files...."
        result="Fail"
        result_file=open(OUTPUT_TEXT_FILES+"Fail_Result.txt", "a")
        result_file.write(str(COUNTER_MAIN))
        result_file.write("\t\t\t\tFail\n")
        result_file.close()
    if OUTPUT_WAVE_FILES:
        print "Inputs=",INPUT_WAVE_FILE, OUTPUT_WAVE_FILES, OUTPUT_GRAPH_FILES, COUNTER_MAIN
        graph_plot.result_plot(INPUT_WAVE_FILE, OUTPUT_WAVE_FILES, OUTPUT_GRAPH_FILES, COUNTER_MAIN)

    mysound.destroy()
##    root.destroy()
##    root.quit()

    del par1, par2, PITCH_LENGTH,PITCH_VALUES,OUTPUT_TEXT_FILES,DEBUG, REC_FFT_LENGTH,REC_FFT_VALUES
    gc.get_referrers()
    gc.collect()
    return result,reason


# TEST_CASE_RESULT_IS_sin,TEST_CASE_OBSERVATION_IS_sin=snack_operations.snack_work(sin,DEBUG,sout,COUNTER_MAIN,op_fold,op_fold)





#### From rms_calculate



##########################################################################################################################################
## Function          :: power_result
## Arguments         :: EPOWER_LENGTH       - Total number of power values.
##                   :: EPOWER_VALUES       - Value of each power sample
##                   :: PRECORDED           - Flag to decide the argumets belongs to original wave file or recorded wave.
##                      OUTPUT_TEXT_FILES   - path where output text files has to be saved.
##                      DEBUG               - Enable to print DEBUG prints.
## Description       :: This function writes the power values to text file.
##########################################################################################################################################


def power_result(EPOWER_LENGTH, EPOWER_VALUES, PRECORDED, OUTPUT_TEXT_FILES, DEBUG):
    DEBUG = int(DEBUG)
    count_power = 0
    if PRECORDED == 0:
        text_file = open(OUTPUT_TEXT_FILES + 'input-power-values.txt', "a")
    else:
        text_file = open(OUTPUT_TEXT_FILES + 'output-power-values.txt', "a")
    while (count_power < EPOWER_LENGTH):
        text_file.write("sample no\t\tpower value")
        text_file.write("\n")
        text_file.write(" ")
        text_file.write(str(count_power))
        text_file.write("----------------->")
        text_file.write(str(EPOWER_VALUES[count_power]))
        text_file.write("\n\n")
        count_power = count_power + 1


##########################################################################################################################################
## Function          :: fft_result
## Arguments         :: EFFT_LENGTH         - Total number of fft values.
##                   :: EFFT_VALUES         - Value of each fft sample
##                   :: FRECORDED           - Flag to decide the argumets belongs to original wave file or recorded wave.
##                      OUTPUT_TEXT_FILES   - path where output text files has to be saved.
##                      DEBUG               - Enable to print DEBUG prints.
## Description       :: This function writes the pitch values to text file.
##########################################################################################################################################


def fft_result(EFFT_LENGTH, EFFT_VALUES, FRECORDED, OUTPUT_TEXT_FILES, DEBUG):
    DEBUG = int(DEBUG)
    count_fft = 0

    if FRECORDED == 0:
        text_file = open(OUTPUT_TEXT_FILES + 'input-abs-values.txt', "a")
    else:
        text_file = open(OUTPUT_TEXT_FILES + 'output-abs-values.txt', "a")
    while (count_fft < EFFT_LENGTH):
        text_file.write("fft no\t\tfft abs value")
        text_file.write("\n")
        text_file.write(" ")
        text_file.write(str(count_fft))
        text_file.write("----------------->")
        text_file.write(str(EFFT_VALUES[count_fft]))
        text_file.write("\n\n")
        count_fft = count_fft + 1


# ! /bin/env/python
##########################################################################################################################################
##########################################################################################################################################
## File              :: rms_calculate.py
## Developer         :: Guruprasad K S
## Version           :: v1.0
## Release Date      :: 13/03/2010
## Changes made      :: Nill
## Changes made Date :: Nill
## Changes made by   :: Nill
##########################################################################################################################################
##########################################################################################################################################
from math import sqrt


##########################################################################################################################################
## Function          :: RMS_FIND
## Arguments         :: RFFT_LENGTH         - Total number of fft values.
##                   :: RFFT_VALUES         - Value of each fft sample
##                   :: DEBUG               - Enable to print DEBUG prints.
## Description       :: This function writes the pitch values to text file.
##########################################################################################################################################
def RMS_FIND(RFFT_LENGTH, RFFT_VALUES, DEBUG):
    DEBUG = int(DEBUG)
    count = 0
    sum_value = 0
    while (count < RFFT_LENGTH):
        if RFFT_VALUES[count] > 0:
            root = sqrt(RFFT_VALUES[count])
            sum_value = sum_value + root
        count = count + 1
    mean = sum_value / count
    square = mean * mean
    return square
# *-----------------------------------------------------------------------------------------------------------------------------------------



### from result_calculate_voip