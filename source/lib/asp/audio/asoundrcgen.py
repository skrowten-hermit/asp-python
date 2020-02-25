


########################################################################################################################
########################################################################################################################
## File              :: lib/asp/audio/asoundrcgen.py
## Description       :: VoIP Automation Common API : Audio play and record functions.
## Developer         :: Sreekanth S
## Version           :: v1.0
## Release Date      :: 11/04/2019
## Changes made      :: Initial version.
## Changes made Date :: 11/04/2019
## Changes made by   :: Sreekanth S
########################################################################################################################
########################################################################################################################



import os
import getopt

from lib.generic.globalutils import *



"""
Generate asoundrc for a given hardware configuration on the PC running automation tests.
"""



class ALSAconfigGenerator:
    def __init__(self, soundcard, chnltype, chnlumber, debug=0):
        self.if_type = "USB"    #  Other possible value is -- PCI.
        self.outpath = os.environ['PYTHONPATH'] + '/configure/.asoundrc'
        self.confpath = os.environ['HOME'] + '/.asoundrc'
        self.DEBUG = debug

        print "Demanded configuration:\nSoundcard\t\t-->\t%s\nAudio Channel Type\t-->\t%s\nNo. of Channels\t\t-->\t%s" \
              %(soundcard, chnltype, chnlumber)
        print

        if soundcard == 'MTrackEight':
            self.genconfMTrackEight(chnltype, chnlumber)
        elif soundcard == '1010LT':
            self.genconfM1010LT(chnltype, chnlumber)
        elif soundcard == 'PlugableUSB':
            self.genconfPlugableUSB(chnltype, chnlumber)
        else:
            print "Unsupported Sound Card!!!"
#*----------------------------------------------------------------------------------------------------------------------

# Generate .asoundrc for M-Audio M-Track Eight.

    def genconfMTrackEight(self, channeltype, channelnumber):
        print "\nGenerating " + str(channeltype) + " configuration for M-Audio MTrackEight with " + str(channelnumber) + \
              " channels....\n"
#*----------------------------------------------------------------------------------------------------------------------

# Generate .asoundrc for Plugable USB soundcard.

    def genconfPlugableUSB(self, channeltype, channelnumber):
        print "\nGenerating " + str(channeltype) + " configuration for Plugable USB Audio Card with " + \
              str(channelnumber) + " channels....\n"
#*----------------------------------------------------------------------------------------------------------------------

# Generate .asoundrc for M-Audio 1010 LT.

    def genconfM1010LT(self, channeltype, channelnumber):
        print "\nGenerating " + str(channeltype) + " configuration for M-Audio 1010 LT Audio Card with " + \
              str(channelnumber) + " channels....\n"
#*----------------------------------------------------------------------------------------------------------------------

# Copy the generated .asoundrc to the home directory.

    def _confCopy(self):
        print "\nCopying the generated configuration to the system profile....\n"
#*----------------------------------------------------------------------------------------------------------------------

# Finish up the .asoundrc generation and copy the generated .asoundrc to the home directory or the specified directory.

    def __del__(self, *args):
        if args:
            self.confpath = args[0]
        print "\nAudio configuration done and copied to the system profile....\n"
        self._confCopy()
#*----------------------------------------------------------------------------------------------------------------------



if __name__ == '__main__':
    print "Capturing...."
