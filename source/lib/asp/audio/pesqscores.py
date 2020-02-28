


########################################################################################################################
########################################################################################################################
## File              :: lib/asp/audio/pesqscores.py
## Description       :: VoIP Automation Common API : Functions for calculating ITU-T's P.862, P.862.1, P.862.2 based
##                      PESQ values (MOS).
## Developer         :: Sreekanth S
## Version           :: v1.0
## Release Date      :: 11/04/2019
## Changes made      :: Initial version.
## Changes made Date :: 11/04/2019
## Changes made by   :: Sreekanth S
########################################################################################################################
########################################################################################################################



import subprocess
import os
import getopt

from lib.generic.globalutils import *



"""
ITUTPESQ functions computes the MOS Score using ITU-T's PESQ utility and dumps them into a result file.
"""



class ITUTPESQ:
    def __init__(self, debug=0):
        environset = 0
        for ppath in ((os.environ['PYTHONPATH']).split(':')):
            if "/automation/voip/dvf-automation/" in ppath:
                self.path = ppath + 'tools/'
                environset = 1
        if environset == 0:
            print "PYTHONPATH not set!!!"
            sys.exit(-1)
        self.samprate = 8000
        self.source = ""
        self.sink = ""
        self.rawMOS = 0.0
        self.lqoMOS = 0.0
        self.support = 0
        self.defresfile = "pesq_results.txt"
        self.DEBUG = debug
#*----------------------------------------------------------------------------------------------------------------------

# Run PESQ utility and return the computed MOS (PESQ) Scores.

    def computeMOS(self, **kwargs):
        self._removedefresult()
        if kwargs:
            validargs = ['source', 'sink', 'samplerate']
            argchk = checkkeywords(kwargs, validargs)
            if self.DEBUG == 1:
                print argchk
            if argchk != "No keywords match":
                if 'source' in kwargs:
                    self.source = kwargs['source']
                if 'sink' in kwargs:
                    self.sink = kwargs['sink']
                if 'samplerate' in kwargs:
                    self.samprate = kwargs['samplerate']
            else:
                if self.DEBUG == 1:
                    print "Keyword error, using default values...."

        if self.samprate == 16000:
            self.support = 1
            line = subprocess.check_output([self.path + "/" + './PESQ', '+16000', self.source, self.sink])
        elif self.samprate == 8000:
            self.support = 1
            line = subprocess.check_output([self.path + "/" + './PESQ', '+8000', self.source, self.sink])
        else:
            self.support = 0
            line = "Sampling rate not supported...."
        if self.DEBUG == 1:
            print line
        if self.support == 1 and "MOS-LQO):" in line:
            result_rMOS = float(line.split("MOS-LQO):  =")[1].split()[0])
            result_lMOS = float(line.split("MOS-LQO):  =")[1].split()[1])
            if self.DEBUG == 1:
                print "Raw MOS for " + getfilename(self.sink) + " : ", result_rMOS
                print "MOS-LQO for " + getfilename(self.sink) + " : ", result_lMOS
            if result_rMOS >= 3.5 or result_lMOS >= 3.5:
                reason = "PASS! Good MOS Score...."
            else:
                reason = "FAIL! Bad MOS Score...."
        else:
            result_rMOS, result_lMOS = 0.0, 0.0
            reason = "Error!!! No MOS scores available...."

        if self.DEBUG == 1:
            print reason

        print "Raw MOS : " + str(result_rMOS) + "\n" + "MOS-LQO : " + str(result_lMOS) + "\n"

        return result_rMOS, result_lMOS
#*----------------------------------------------------------------------------------------------------------------------

# Dump the computed MOS scores into a file.

    def getnsetMOS(self, resfile, **kwargs):
        self._removedefresult()
        if kwargs:
            validargs = ['source', 'sink', 'samplerate']
            argchk = checkkeywords(kwargs, validargs)
            if self.DEBUG == 1:
                print argchk
            if argchk != "No keywords match":
                if 'source' in kwargs:
                    self.source = kwargs['source']
                if 'sink' in kwargs:
                    self.sink = kwargs['sink']
                if 'samplerate' in kwargs:
                    self.samprate = kwargs['samplerate']
            else:
                if self.DEBUG == 1:
                    print "Keyword error, using default values...."

        if self.samprate in [8000, 16000]:
            self.support = 1
        else:
            self.support = 0

        if self.support == 1:
            self.rawMOS, self.lqoMOS = self.computeMOS()
            with open(self.defresfile, 'r') as file:
                defresult = file.read()
            mos_file = open(resfile, "a+")
            mos_file.write("\n\n" + defresult + "\n")
            mos_file.write("++++++++++++++" + getfilename(self.sink) + "++++++++++++++" + "\n")
            mos_file.write("Raw MOS for " + getfilename(self.sink) + "   ----->  " + str(self.rawMOS) + "\n")
            mos_file.write("MOS-LQO for " + getfilename(self.sink) + "   ----->  " + str(self.lqoMOS) + "\n")
            mos_file.write("++++++++++++++" + getfilename(self.sink) + "++++++++++++++" + "\n")
            if self.DEBUG == 1:
                print 100 * "#"
                print "Raw MOS : ", self.rawMOS
                print "MOS-LQO : ", self.lqoMOS
                print 100 * "#"
            print "MOS values computed and written to file : ", resfile
        else:
            mos_file = open(resfile, "a+")
            mos_file.write("++++++++++++++" + getfilename(self.sink) + "++++++++++++++" + "\n")
            mos_file.write("Unsupported sample rate for " + getfilename(self.sink) + ", MOS (PESQ) not available" + "\n")
            mos_file.write("++++++++++++++" + getfilename(self.sink) + "++++++++++++++" + "\n")
            if self.DEBUG == 1:
                print 100 * "#"
                print "Raw MOS : ", self.rawMOS
                print "MOS-LQO : ", self.lqoMOS
                print 100 * "#"
            print "MOS values computed and written to file : ", resfile

        mos_file.close()

        self._removedefresult()

        return self.rawMOS, self.lqoMOS
#*----------------------------------------------------------------------------------------------------------------------

# Dump the computed MOS scores into a file.

    def _removedefresult(self):
        if os.path.exists(self.defresfile):
            print "Removing default results file...."
            os.remove(self.defresfile)

# How to use the code above.

def usage():
    print "Use the following command options (if needed):\n"
    print "pesqscores.py -i, --source <sourcefile> -o, --sink <recordedfile> -s, --samplerate <samplerate>"
    print "\n\n" + 120 * "%" + "\n\n\t\t\t\t\tProgram to calculate MOS Scores\n\n" + 120 * "%" + "\n\n"
#*----------------------------------------------------------------------------------------------------------------------



if __name__ == '__main__':
    print "\n\n" + 120 * "%" + "\n\n\t\t\t\t\tProgram to calculate MOS Scores\n\n" + 120 * "%" + "\n\n"

    pesqres = ITUTPESQ(debug=1)

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:s:", ["source", "sink", "samplerate"])
    except getopt.GetoptError:
        usage()

    srcpath = '/home/sreekanth/automation_v5/automation/voip/dvf-automation/input/audio/'

    if len(opts) != 0:
        for opt, arg in opts:
            if opt == '-h':
                usage()
                sys.exit(0)
            if opt == '-i' or opt == '--source':
                pesqres.source = srcpath + arg
            elif opt == '-o' or opt == '--sink':
                pesqres.sink = arg
            elif opt == '-s' or opt == '--samplerate':
                pesqres.samprate = int(arg)

        mos1, mos2 = pesqres.computeMOS()
        mos1, mos2 = pesqres.getnsetMOS('output.txt')
    else:
        pesqres.source = srcpath + 'male_8k.wav'
        pesqres.sink = 'output.wav'

        mos1, mos2 = pesqres.computeMOS()
        rmos, lmos = pesqres.getnsetMOS('output.txt')
        pesqres.samprate = 16000
        mos1, mos2 = pesqres.computeMOS(source=srcpath + 'male_16k.wav', sink='output.wav')
        mos1, mos2 = pesqres.computeMOS(source=srcpath + 'male_16k.wav', sink='output_16k.wav', samplerate=16000)
        rmos, lmos = pesqres.getnsetMOS('output.txt', source=srcpath + 'male_16k.wav', sink='output_16k.wav',
                                        samplerate=16000)

    print "\n\n" + 120 * "%" + "\n\n\t\t\t\t\tProgram to calculate MOS Scores\n\n" + 120 * "%" + "\n\n"
