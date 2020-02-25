


########################################################################################################################
########################################################################################################################
## File              :: lib/generic/packetutils.py
## Description       :: VoIP Automation Common API : Functions for packet capture, analysis and post processing captured
##                      pcap files.
## Developer         :: Sreekanth S
## Version           :: v1.0
## Release Date      :: 11/04/2019
## Changes made      :: Initial version.
## Changes made Date :: 11/04/2019
## Changes made by   :: Sreekanth S
########################################################################################################################
########################################################################################################################



import subprocess

from globalutils import *



"""
NetCapAnalyis is a utility that captures data packets and parses and analyzes them.
"""



class NetCapAnalyis:
    def __init__(self, debug=0):
        self.src_ip = ""
        self.dst_ip = ""
        self.cap_file = ""
        self.filter = ""
        self.duration = 0.0
        self.DEBUG = debug
#*----------------------------------------------------------------------------------------------------------------------

# Capture network traffic during a session for a given duration using tshark.

    def wirecapture(self, B1, B2, op_fold, file_name, cap_duration):
        self.src_ip = B1
        self.dst_ip = B2
        self.cap_file = op_fold + file_name
        self.duration = cap_duration
        if self.DEBUG == 1:
            print "Executing a wireshark capture...."
            print "DUT IP : ", B1
            print "Output file path : ", self.cap_file
        if self.duration == 0:
            cmd = 'tshark -i 1 -P -w ' + self.cap_file + '.pcap src ' + str(self.src_ip) + ' or src ' + \
                  str(self.dst_ip) + ' or dst ' + str(self.src_ip) + ' or dst ' + str(self.dst_ip)
        elif self.duration == -1:
            cmd = 'tshark -i 1 -P -w ' + self.cap_file + '.pcap'
        else:
            cmd = 'tshark -i 1 -a duration:' + str(self.duration) + ' -P -w ' + self.cap_file + '.pcap src ' + \
                  str(self.src_ip) + ' or src ' + str(self.dst_ip) + ' or dst ' + str(self.src_ip) + ' or dst ' + \
                  str(self.dst_ip)

        p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

        # DEVNULL = open(os.devnull, 'wb')
        # p = subprocess.Popen(cmd, shell=True, stderr=DEVNULL, stdout=DEVNULL)

        while True:
            out = p.stderr.read(1)
            if out == '' and p.poll() != None:
                break
            if out != '':
                if int(self.debug) == 1:
                    sys.stdout.write(out)
                    sys.stdout.flush()
#*----------------------------------------------------------------------------------------------------------------------



if __name__ == '__main__':
    print "Capturing...."
