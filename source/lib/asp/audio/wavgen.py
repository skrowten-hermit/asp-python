


########################################################################################################################
########################################################################################################################
## File              :: lib/asp/audio/wavgen.py
## Description       :: VoIP Automation Common API : Functions for creating a '.wav' file out of raw PCM data.
## Developer         :: Sreekanth S
## Version           :: v1.0
## Release Date      :: 11/04/2019
## Changes made      :: Initial version.
## Changes made Date :: 11/04/2019
## Changes made by   :: Sreekanth S
########################################################################################################################
########################################################################################################################



import wave
import getopt

from lib.generic.globalutils import *



"""
WavGenerator takes in raw audio (PCM) data and converts it into a .wav file by adding the wav headers for better 
compatibility and usability.
"""



class WavGenerator:
    def __init__(self, debug=0):
        self.sampleRate = 16000
        self.sampleSize = 2
        self.channels = 1
        self.skip = 0
        self.every = 0
        self.inputFileName = None
        self.outputFileName = "output.wav"
        self.DEBUG = debug
#*----------------------------------------------------------------------------------------------------------------------

# Create a .wav file from raw file.

    def wavSynthesis(self, **kwargs):
        if kwargs:
            validargs = ['inputfile', 'samplerate', 'channels', 'samplesize', 'targetfile']
            argchk = checkkeywords(kwargs, validargs)
            if self.DEBUG == 1:
                print argchk
            if argchk != "No keywords match":
                if 'inputfile' in kwargs:
                    self.inputFileName = kwargs['inputfile']
                if 'samplerate' in kwargs:
                    self.sampleRate = kwargs['samplerate']
                if 'channels' in kwargs:
                    self.channels = kwargs['channels']
                if 'samplesize' in kwargs:
                    self.sampleSize = kwargs['samplesize']
                if 'targetfile' in kwargs:
                    self.outputFileName = kwargs['targetfile']
            else:
                if self.DEBUG == 1:
                    print "Keyword error, using default values...."
        output = wave.open(self.outputFileName, 'w')

        with open(self.inputFileName, 'rb') as inputFile:
            inputData = inputFile.read()

        output.setparams((self.channels, self.sampleSize, self.sampleRate, 0, 'NONE', 'not compressed'))
        data = inputData[self.skip:]
        nrSamples = len(data) / self.sampleSize
        if self.every != 0:
            irange = nrSamples
            ldata = [data[x * self.sampleSize:x * self.sampleSize + self.sampleSize]
                     for x in range(irange) if x % self.every == 0]
            nrSamples /= self.every
            data = "".join(ldata)

        output.writeframes(data)

        print "created %s" % self.outputFileName
        print "  rate       : %uHz" % self.sampleRate
        print "  channels   : %u" % self.channels
        print "  sample size: %ubytes" % self.sampleSize
        print "  samples    : %u (%4.1fs)" % (nrSamples, float(nrSamples) / self.sampleRate)

        output.close()
#*----------------------------------------------------------------------------------------------------------------------

# How to use the code above.

def usage():
    print "Use the following command options (if needed):\n"
    print "wavgen.py -i <file> -o <file> -c <channels -f <bytes per sample> -r <rate in Hz> --every=<frame to take> " \
          "--skip=<bytes to skip>"
    print "\n\n" + 120 * "%" + "\n\n\t\t\t\tProgram to Generate a .wav file from raw PCM data\n\n" + 120 * "%" + "\n\n"
#*----------------------------------------------------------------------------------------------------------------------



if __name__ == "__main__":
    print "\n\n" + 120 * "%" + "\n\n\t\t\t\tProgram to Generate a .wav file from raw PCM data\n\n" + 120 * "%" + "\n\n"

    cW = WavGenerator(debug=1)

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:c:f:r:", ["every=", "skip="])
    except getopt.GetoptError:
        usage()
        sys.exit(-1)

    if len(opts) != 0:
        for opt, arg in opts:
            if opt == '-h':
                usage()
                sys.exit(0)
            if opt == '-i':
                cW.inputFileName = arg
            elif opt == '-o':
                cW.outputFileName = arg
            elif opt == '--every':
                cW.every = int(arg, 10)
            elif opt == '--skip':
                cW.skip = int(arg, 10)
            elif opt == '-c':
                cW.channels = int(arg, 10)
            elif opt == '-f':
                cW.sampleSize = int(arg, 10)
            elif opt == '-r':
                cW.sampleRate = int(arg, 10)
    else:
        cW.inputFileName = ""
        cW.outputFileName = ""
        cW.every = 1000
        cW.skip = 10
        cW.channels = 1
        cW.sampleSize = 40000
        cW.sampleRate = 8000

    if cW.inputFileName is None:
        usage()
        sys.exit(-1)

    if cW.every < 0:
        usage()
        sys.exit(-1)

    if cW.skip < 0:
        usage()
        sys.exit(-1)

    if cW.channels <= 0:
        usage()
        sys.exit(-1)

    if cW.sampleSize <= 0:
        usage()
        sys.exit(-1)

    if cW.sampleRate <= 0:
        usage()
        sys.exit(-1)

    cW.wavSynthesis()

    print "\n\n" + 120 * "%" + "\n\n\t\t\t\tProgram to Generate a .wav file from raw PCM data\n\n" + 120 * "%" + "\n\n"
