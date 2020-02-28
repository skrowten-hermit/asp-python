


########################################################################################################################
########################################################################################################################
## File              :: lib/asp/audio/speechverify.py
## Description       :: VoIP Automation Common API : Audio, speech verification routines/functions using tkSnack.
## Developer         :: Sreekanth S
## Version           :: v2.0
## Release Date      :: 28/03/2019
## Changes made      :: Created a class based API.
## Changes made Date :: 23/08/2018
## Changes made by   :: Sreekanth S
########################################################################################################################
########################################################################################################################



import os
import time
import gc
import getopt

import numpy
from math import sqrt
from numpy.fft import fft

from lib.generic.globalutils import *

from Tkinter import*
import tkSnack



"""
SpeechVerify is a utility to verify the presence of speech on a given file with respect to a source file using 'tksnack'
library.
NOTE: speechAnalysis() IS LEGACY CODE. NOT IDEAL AND EFFICIENT.
"""



root = Tk()
tkSnack.initializeSnack(root)
root.withdraw()



class SpeechVerify:
    def __init__(self, debug=0):
        self.inwav = ""
        self.recwav = ""
        self.outpath = ""
        self.DEBUG = debug
#*----------------------------------------------------------------------------------------------------------------------

# Calculate the onset delay between the two.

    def calcDelay(self, *args, **kwargs):
        if args:
            if len(args) > 0:
                self.inwav = args[0]
                if len(args) > 1:
                    self.recwav = args[1]
        if kwargs:
            validargs = ['infile', 'outfile']
            argchk = checkkeywords(kwargs, validargs)
            if self.DEBUG == 1:
                print argchk
            if argchk != "No keywords match":
                if 'infile' in kwargs:
                    self.inwav = kwargs['infile']
                if 'outfile' in kwargs:
                    self.recwav = kwargs['outfile']
            else:
                if self.DEBUG == 1:
                    print "\nKeyword error, using default values...."
        source = tkSnack.Sound()
        source.read(self.inwav)
        sink = tkSnack.Sound()
        sink.read(self.recwav)
        orig = source.pitch()
        rec = sink.pitch()
        corr = numpy.correlate(orig, rec, 'full')
        delay = int(len(corr) / 2) - numpy.argmax(corr)
        if self.DEBUG == 1:
            print "\n\n"
            print "input file = ", self.inwav
            print "Output file = ", self.recwav
            print "\n\nDelay = ", delay
            print "\n\n"
        return delay
#*----------------------------------------------------------------------------------------------------------------------

# Play audio using ALSA on a given output interface.

    def speechAnalysis(self, *args, **kwargs):
        if args:
            if len(args) > 0:
                self.inwav = args[0]
                if len(args) > 1:
                    self.recwav = args[1]
        if kwargs:
            validargs = ['infile', 'outfile']
            argchk = checkkeywords(kwargs, validargs)
            if self.DEBUG == 1:
                print argchk
            if argchk != "No keywords match":
                if 'infile' in kwargs:
                    self.inwav = kwargs['infile']
                if 'outfile' in kwargs:
                    self.recwav = kwargs['outfile']
            else:
                if self.DEBUG == 1:
                    print "\nKeyword error, using default values...."

        if self.DEBUG == 1:
            print "\n\n"
            print "input file = ", self.inwav
            print "Output file = ", self.recwav
            print "\n\n"

        ##  Processing Original/input Wave File

        source = tkSnack.Sound()
        source.read(self.inwav)
        source_pitchvals = source.pitch()
        source_pitchlen = len(source_pitchvals)
        source_pitchsum = 0
        temp_count = 0

        ## Pitch Calculation, Pitch Text Write of input Wave File

        while temp_count < source_pitchlen:
            source_pitchsum = source_pitchsum + source_pitchvals[temp_count]
            temp_count += 1
        source_pitchcnt = source_pitchsum/temp_count
        source_pitchcount, source_pitchvalues = self._pitchResult(source_pitchlen, source_pitchvals, 0)

        ## RMS calculation of FFT of input Wave file

        source_raw_fft = fft(source_pitchvals)
        source_fft_values = abs(source_raw_fft)
        source_fft_length = len(source_fft_values)
        sourceRMS = self._calculateRMS(source_fft_length, source_fft_values)

        source.destroy()

        ## Processing Recorded Wave File

        sink = tkSnack.Sound()
        sink.read(self.recwav)

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
            sink_pitchcount, sink_pitchvalues = self._pitchResult(sink_pitchlen, sink_pitchvals, 1)

            ## RMS calculation of FFT of input Wave file

            sink_raw_fft = fft(sink_pitchvals)
            sink_fft_values = abs(sink_raw_fft)
            sink_fft_length = len(sink_fft_values)
            sinkRMS = self._calculateRMS(sink_fft_length, sink_fft_values)

            ## RMS match and Pitch match percentage calculation

            percRMS, percPITCH = self._matchResult(sourceRMS, sinkRMS, source_pitchsum, sink_pitchsum)

            if self.DEBUG == 1:
                print "Output Pitch Count = ", sink_pitchcount
                print "Output Pitch Value = ", sink_pitchvalues
                print "input Pitch Count = ", source_pitchcount
                print "input Pitch Value = ", source_pitchvalues

            ## Modified to last 50 pitch values from last 100 values

            lastBlanks = sink_pitchlen - 50
            sumLastSink = 0
            while lastBlanks < sink_pitchlen:
                sumLastSink += sink_pitchvals[lastBlanks]
                lastBlanks += 1

            ## Calculating the time delay b/w play and record

            delay_rec = (sink_pitchcount - source_pitchcount) * 10
            if self.DEBUG == 1:
                print "Time delay between playing and recording = %s m sec" % delay_rec
            delay_rec = delay_rec * 0.001
            if self.DEBUG == 1:
                print "Time delay between playing and recording = %f sec" % delay_rec
            reason = "Audio/Speech exists"
            if self.DEBUG == 1:
                print "Test End Time (12hr) :", time.strftime("%I:%M:%S %p", time.localtime())
            if (0 < sink_pitchcount) and (sink_pitchcount < (source_pitchcount) * (0.8)):
                result_file = open(self.outpath + "fail.dump", "a")
                result_file.write("\t\t\t\tFail\n")
                result_file.close()
                reason = "Noisy audio...."
                result = "Fail"

            elif delay_rec < -50:
                result_file = open(self.outpath + "fail.dump", "a")
                result_file.write("\t\t\t\tFail\n")
                result_file.close()
                reason = "Components seen before audio started...."
                result = "Fail"

            elif sumLastSink > 50:
                result_file = open(self.outpath + "fail.dump", "a")
                result_file.write("\t\t\t\tFail\n")
                result_file.close()
                print "SUM-50 = ", sumLastSink
                reason = "High audio gain, check gain setting(s)...."
                result = "Fail"

            else:
                if percPITCH > 260 and percRMS > 200:
                    print "Condition 1"
                    reason = "Audio Gains/Noise is too high...."
                    result = "Fail"
                    result_file = open(self.outpath + "fail.dump", "a")
                    result_file.write("\t\t\t\tFail\n")
                    result_file.close()

                elif percPITCH < 80 and percRMS < 80:
                    print "Condition 2"
                    reason = "Components are below threshold...."
                    result = "Fail"
                    result_file = open(self.outpath + "fail.dump", "a")
                    result_file.write("\t\t\t\tFail\n")
                    result_file.close()

                elif percPITCH > 60 and percRMS < 70:
                    print "Condition 3"
                    reason = "Components are much below threshold...."
                    result = "Fail"
                    result_file = open(self.outpath + "fail.dump", "a")
                    result_file.write("\t\t\t\tFail\n")
                    result_file.close()

                elif percPITCH > 80 and percRMS > 80 and percPITCH < 150 and percRMS < 130:
                    reason = "Voice/Speech exists...."
                    result = "Pass"
                    result_file = open(self.outpath + "fail.dump", "a")
                    result_file.write("\t\t\t\tPass\n")
                    result_file.close()

                elif percPITCH > 80 and percRMS > 80 and percPITCH < 260.01 and percRMS < 200.01:
                    reason = "Voice/Speech exists...."
                    result = "Pass"
                    result_file = open(self.outpath + "fail.dump", "a")
                    result_file.write("\t\t\t\tPass\n")
                    result_file.close()

                elif percPITCH > 65 and percRMS > 90 and percPITCH < 150 and percRMS < 200:
                    reason = "Voice/Speech exists...."
                    result = "Pass"
                    result_file = open(self.outpath + "fail.dump", "a")
                    result_file.write("\t\t\t\tPass\n")
                    result_file.close()

                else:
                    print "Condition 4", percPITCH, percRMS
                    reason = "Faulty audio, please check the Graphs and audio files...."
                    result = "Fail"
                    result_file = open(self.outpath + "fail.dump", "a")
                    result_file.write("\t\t\t\tFail\n")
                    result_file.close()

        else:
            print "Condition 4"
            reason = "Faulty audio, please check the supporting files...."
            result = "Fail"
            result_file = open(self.outpath + "fail.dump", "a")
            result_file.write("\t\t\t\tFail\n")
            result_file.close()

        # out_graphs = GP.graph_plot(self.inwav, self.recwav, self.outpath)
        # out_graphs.wav_plot_compare(1)

        sink.destroy()
    ##    root.destroy()
    ##    root.quit()

        del sink_raw_fft, sink_fft_values, sink_pitchvalues, sink_pitchvals, source_raw_fft, source_fft_values, source_pitchvalues, source_pitchvals
        gc.get_referrers()
        gc.collect()
        return result, reason
#*----------------------------------------------------------------------------------------------------------------------

# Calculate the RMS value of the pitch from the array.

    def _calculateRMS(self, fft_len, fft_vals):
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
#*----------------------------------------------------------------------------------------------------------------------

# Calculate the RMS value match percentage with respect to the source and the sink.

    def _matchResult(self, inRMS, recRMS, in_pitch_sum, out_pitch_sum):
        percRMSmatch = 0
        percPITCHmatch = 0
        res_path = self.outpath + 'match-result.dump'
        if recRMS == 0:
            percRMSmatch = 0.0
        else:
            percRMSmatch = inRMS * 100 / recRMS
            if percRMSmatch > 300:
                if self.DEBUG == 1:
                    print "Check if any other audio is playing........."
                reason = "Check if any other audio is playing........."
                result = "Fail"
                return result,reason
            else:
                if percRMSmatch > 100:
                    noise_rmsperc = percRMSmatch - 100
                    percRMSmatch -= noise_rmsperc
                    print "RESULTS"
                    print "RMS MATCH = ", percRMSmatch
                    print "NOISE = ", noise_rmsperc/4
                else :
                    if percRMSmatch < 50:
                        if self.DEBUG == 1:
                            print "NOISE = ", percRMSmatch
                    else:
                        if self.DEBUG == 1:
                            print "RMS MATCH = ", percRMSmatch
                            print "Noise is negligible...."
                outresultfile = open(res_path, "a")
                outresultfile.write("RMS MATCH = ")
                outresultfile.write(str(percRMSmatch))
                outresultfile.write("\n")
                outresultfile.close()

        if out_pitch_sum==0:
            percPITCHmatch = 0
        else:
            percPITCHmatch = in_pitch_sum * 100 / out_pitch_sum

        if percPITCHmatch < 50 :
            if self.DEBUG == 1:
                print "Test fails....."
        else:
            if self.DEBUG == 1:
                print "###########################################################################"
            if percPITCHmatch > 300:
                if self.DEBUG == 1:
                    print "check input...."
            else:
                if percPITCHmatch > 100:
                    noise_pitchperc = percPITCHmatch -100
                    if self.DEBUG == 1:
                        print "PITCH MATCH = 100"
                    percPITCHmatch -= noise_pitchperc
                    if self.DEBUG == 1:
                        print "NOISE PITCH = ", noise_pitchperc/4
                else:
                    if self.DEBUG == 1:
                        print "PITCH MATCH = ", percRMSmatch

        if self.DEBUG == 1:
            print "###########################################################################"
        outresultfile = open(res_path, "a")
        outresultfile.write("PITCH MATCH = ")
        outresultfile.write(str(percPITCHmatch))
        outresultfile.write("\n")
        outresultfile.close()
        return percPITCHmatch, percRMSmatch
#*----------------------------------------------------------------------------------------------------------------------

# Write the pitch value results to a file.

    def _pitchResult(self, pitchlen, pitchvalues, recorded):
        count_pitch = 0
        pitch_stop_flag = 0
        out_pitch_count = 0
        out_pitch_value = 0

        if recorded == 0:
            path = self.outpath + 'inputpitch.dump'
            if self.DEBUG == 1:
                print path
            outresultfile = open(path, "a")
        else:
            path = self.outpath + 'outputpitch.dump'
            if self.DEBUG == 1:
                print path
            outresultfile = open(path, "a")

        while (count_pitch < pitchlen):
            outresultfile.write("fft no\t\tfft abs value")
            outresultfile.write("\n")
            outresultfile.write(" ")
            outresultfile.write(str(count_pitch))
            outresultfile.write("----------------->")

            if pitch_stop_flag == 0:
                if pitchvalues[count_pitch] != 0:
                    pitch_stop_flag = 1
                    if self.DEBUG == 1:
                        print "pitch_stop_counter", pitch_stop_flag
                    if recorded == 0:
                        in_pitch_count = count_pitch
                        in_pitch_value = pitchvalues[count_pitch]
                        if self.DEBUG == 1:
                            print "input pitch count    :: ", in_pitch_count
                            print "input Pitch Value    :: ", in_pitch_value
                    elif recorded == 1:
                        out_pitch_count = count_pitch
                        out_pitch_value = pitchvalues[count_pitch]
                        if self.DEBUG == 1:
                            print "Output pitch count   :: ", out_pitch_count
                            print "Output Pitch Value   :: ", out_pitch_value

            outresultfile.write(str(pitchvalues[count_pitch]))
            outresultfile.write("\n\n")
            count_pitch = count_pitch + 1

        if recorded == 0:
            return in_pitch_count, in_pitch_value
        elif recorded == 1:
            if self.DEBUG == 1:
                print "recorded = ", recorded
            return out_pitch_count, out_pitch_value
#*----------------------------------------------------------------------------------------------------------------------

# Write the calculated Power values to a text file.

    def _writePowerResult(self, power_length, power_values, recorded):
        count_power = 0
        if recorded == 0:
            outresultfile = open(self.outpath + 'input-power-vals.dump', "a")
        else:
            outresultfile = open(self.outpath + 'output-power-vals.dump', "a")
        while (count_power < power_length):
            outresultfile.write("sample no\t\tpower value")
            outresultfile.write("\n")
            outresultfile.write(" ")
            outresultfile.write(str(count_power))
            outresultfile.write("----------------->")
            outresultfile.write(str(power_values[count_power]))
            outresultfile.write("\n\n")
            count_power = count_power + 1
#*----------------------------------------------------------------------------------------------------------------------

# Write the calculated FFT values to a text file.

    def _writeFFTResult(self, fft_length , fft_values, recorded):
        count_fft = 0
        if recorded == 0:
            outresultfile = open(self.outpath + 'input-abs-vals.dump', "a")
        else:
            outresultfile = open(self.outpath + 'output-abs-vals.dump', "a")
        while (count_fft < fft_length):
            outresultfile.write("fft no\t\tfft abs value")
            outresultfile.write("\n")
            outresultfile.write(" ")
            outresultfile.write(str(count_fft))
            outresultfile.write("----------------->")
            outresultfile.write(str(fft_values[count_fft]))
            outresultfile.write("\n\n")
            count_fft = count_fft + 1
#*----------------------------------------------------------------------------------------------------------------------

# How to use the code above.

def usage():
    print "Use the following command options (if needed):\n"
    print "wavgen.py -i <file> -o <file> -c <channels -f <bytes per sample> -r <rate in Hz> --every=<frame to take> " \
          "--skip=<bytes to skip>"
#*----------------------------------------------------------------------------------------------------------------------



##iter=0
##
##while iter<100:
##    DEBUG=1
##    sin='C:\\automation\Voice_Test_Tool\input\sirtest.wav'
##    sout='C:\\automation\Voice_Test_Tool\Output\SIR_TEST_REC.1.wav'
##    outdir="C:\\automation\Voice_Test_Tool\Output\\"
##    outdir="C:\\automation\Voice_Test_Tool\Output\\"
##    print 50*"*"
##    snack_work(sin,DEBUG,sout,iter,outdir,outdir)
##    iter+=1



if __name__ == '__main__':
    print "\n\n" + 120 * "%" + "\n\n\t\t\t\t\tProgram to verify speech/audio\n\n" + 120 * "%" + "\n\n"

    srccpath = '/home/sreekanth/automation_v5/automation/voip/dvf-automation/input/audio/'

    svold = SpeechVerify(debug=1)
    svold.inwav = srccpath + 'male_8k.wav'
    svold.recwav = "output.wav"

    environset = 0
    for ppath in ((os.environ['PYTHONPATH']).split(':')):
        if "/automation/voip/dvf-automation/" in ppath:
            svold.outpath = ppath + 'tools/'
            environset = 1
    if environset == 0:
        print "PYTHONPATH not set!!!"

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:", ["infile", "outfile"])
    except getopt.GetoptError:
        usage()
        sys.exit(-1)

    svold.outpath = ''
    outpath = os.curdir

    if len(opts) != 0:
        for opt, arg in opts:
            if opt == '-h':
                usage()
                sys.exit(0)
            if opt == '-i' or opt == '--infile':
                svold.inwav = arg
            elif opt == '-o' or opt == '--outfile':
                svold.recwav = arg

        svold.calcDelay()
        svold.calcDelay(srccpath + 'male_48k.wav')
        svold.calcDelay(srccpath + 'male_8k.wav', "output_16k.wav")
        svold.calcDelay(infile=srccpath + 'male_8k_short.wav', outfile="output.wav")

        svold.speechAnalysis()
        svold.speechAnalysis(srccpath + 'male_48k.wav')
        svold.speechAnalysis(srccpath + 'male_8k.wav', "output_16k.wav")
        svold.speechAnalysis(infile=srccpath + 'male_8k_short.wav', outfile="output.wav")
    else:
        svold.calcDelay()
        svold.calcDelay(srccpath + 'male_16k.wav', "output_16k.wav")
        svold.calcDelay(infile=srccpath + 'male_16k.wav', outfile="NB_PCMA_b1_b2.wav")

        svold.speechAnalysis()
        svold.speechAnalysis(srccpath + 'male_16k.wav', "output_16k.wav")
        svold.speechAnalysis(outfile="NB_PCMA_b2_b1.wav", infile=srccpath + 'male_16k.wav')

    print "\n\n" + 120 * "%" + "\n\n\t\t\t\t\tProgram to verify speech/audio\n\n" + 120 * "%" + "\n\n"
