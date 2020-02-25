
########################################################################################################################
########################################################################################################################
## File              :: lib/asp/audio/audplayrec.py
## Description       :: VoIP Automation Common API : Audio play and record functions.
## Developer         :: Sreekanth S
## Version           :: v1.0
## Release Date      :: 11/04/2019
## Changes made      :: Initial version.
## Changes made Date :: 11/04/2019
## Changes made by   :: Sreekanth S
########################################################################################################################
########################################################################################################################



import thread
import threading
import wave
import os
import subprocess
import time
import argparse

from lib.generic.globalutils import *



"""
SYSPlayRecord functions use ALSA libraries to play and record audio under various scenarios. Supports parallel 
recordings on multiple interfaces.
"""



class SYSPlayRecord:
    def __init__(self, debug=0):
        self.playpath = "" # Will remain constant
        self.recpath = "" # Will vary from case to case
        self.playsamprate = 8000
        self.recsamprate = 8000
        self.outif = "outch1"
        self.inif = "inch1"
        self.playif = []
        self.reciflst = []
        self.playtimes = 1
        self.reclen = 9 # Only integer values are accepted by ALSA
        self.multiple_th = 2
        self.inwav = ""
        self.outwav = ""
        self.playwav = self.playpath + self.inwav
        self.recwav = self.recpath + self.outwav
        self.plwavlst = []
        self.recwavlst = []
        self.replug = 0 # Will determine if sound card is relay controlled and if it needs to be unplugged and replugged
        self.relayif = "VN407_1" # The relay ID and pin number connected to the power cable of USB soundcard
        self.DEBUG = debug
#*----------------------------------------------------------------------------------------------------------------------

# Play audio using ALSA on a given output interface.

    def playAudio(self, *args, **kwargs):
        if args:
            if len(args) > 0:
                self.outif = args[0]
                if len(args) > 1:
                    self.playsamprate = args[1]
                    if len(args) > 2:
                        self.playwav = args[2]
        if kwargs:
            validargs = ['outif', 'samplerate', 'playfile']
            argchk = checkkeywords(kwargs, validargs)
            if self.DEBUG == 1:
                print argchk
            if argchk != "No keywords match":
                if 'outif' in kwargs:
                    self.outif = kwargs['outif']
                if 'samplerate' in kwargs:
                    self.playsamprate = kwargs['samplerate']
                if 'playfile' in kwargs:
                    self.playwav = kwargs['playfile']
            else:
                if self.DEBUG == 1:
                    print "\nKeyword error, using default values...."
        self.inwav = getfilename(self.playwav)
        cmd = "aplay -D plug:" + str(self.outif) + " -c 1 -r " + str(self.playsamprate) + " " + self.playwav
        if self.DEBUG == 1:
            print "\nPlaying " + self.inwav + " through the output interface " + str(self.outif) + "...."
            print "\nWill start playing now...."
            print "\n" + "#" * 100 + "\n" + "#" * 100
            print "\nPlay interface/channel\t:\t" + str(self.outif)
            print "\nPlaying file\t\t:\t", self.playwav
            print "\nSampling rate\t\t:\t", self.playsamprate
            print "\nALSA command\t\t:\t", cmd
            print "\n" + "#" * 100 + "\n" + "#" * 100 + "\n"
        os.system(cmd)
        if self.DEBUG == 1:
            print "\nEnd of play...\n"
#*----------------------------------------------------------------------------------------------------------------------

# Play audio using ALSA on a given output interface and number of times.

    def nplayAudio(self, n, *args, **kwargs):
        if args:
            if len(args) > 0:
                self.outif = args[0]
                if len(args) > 1:
                    self.playsamprate = args[1]
                    if len(args) > 2:
                        self.playwav = args[2]
        if kwargs:
            validargs = ['outif', 'samplerate', 'playfile']
            argchk = checkkeywords(kwargs, validargs)
            if self.DEBUG == 1:
                print argchk
            if argchk != "No keywords match":
                if 'outif' in kwargs:
                    self.outif = kwargs['outif']
                if 'samplerate' in kwargs:
                    self.playsamprate = kwargs['samplerate']
                if 'playfile' in kwargs:
                    self.playwav = kwargs['playfile']
            else:
                if self.DEBUG == 1:
                    print "\nKeyword error, using default values...."
        self.inwav = getfilename(self.playwav)
        cmd = "aplay -D plug:" + str(self.outif) + " -c 1 -r " + str(self.playsamprate) + " " + self.playwav
        if self.DEBUG == 1:
            print "\nPlaying " + self.inwav + " through the output interface " + str(self.outif) + " for " + str(n) + \
                  " times...."
            print "\nWill start playing now...."
        for pt in range(0, n):
            if self.DEBUG == 1:
                print "\n" + "#" * 100 + "\n" + "#" * 100
                print "\nPlay number\t\t:\t", str(pt + 1)
                print "\nPlay interface/channel\t:\t" + str(self.outif)
                print "\nPlaying file\t\t:\t", self.playwav
                print "\nSampling rate\t\t:\t", self.playsamprate
                print "\nALSA command\t\t:\t", cmd
                print "\n" + "#" * 100 + "\n" + "#" * 100 + "\n"
            os.system(cmd)
        if self.DEBUG == 1:
            print "\nEnd of play...\n"
#*----------------------------------------------------------------------------------------------------------------------

# Record audio using ALSA on a given input interface.

    def recordAudio(self, *args, **kwargs):
        if args:
            if len(args) > 0:
                self.inif = args[0]
                if len(args) > 1:
                    self.recsamprate = args[1]
                    if len(args) > 2:
                        self.recwav = args[2]
                        if len(args) > 3:
                            self.reclen = int(round(int(args[3])))
        if kwargs:
            validargs = ['inif', 'samplerate', 'recfile', 'recduration']
            argchk = checkkeywords(kwargs, validargs)
            if self.DEBUG == 1:
                print argchk
            if argchk != "No keywords match":
                if 'inif' in kwargs:
                    self.inif = kwargs['inif']
                if 'samplerate' in kwargs:
                    self.recsamprate = kwargs['samplerate']
                if 'recfile' in kwargs:
                    self.recwav = kwargs['recfile']
                if 'recduration' in kwargs:
                    self.reclen = int(round(int(kwargs['recduration'])))
            else:
                if self.DEBUG == 1:
                    print "\nKeyword error, using default values...."
        cmd = "arecord -D plug:" + str(self.inif) + " -c 1 -d " + str(self.reclen) + " -f S16_LE -r " + \
              str(self.recsamprate) + " " + self.recwav
        if self.DEBUG == 1:
            print "\nRecording to " + self.recwav + " through the input interface " + str(self.inif) + "...."
            print "\nWill start recording now...."
            print "\n" + "#" * 100 + "\n" + "#" * 100
            print "\nRecord interface/channel:\t", str(self.inif)
            print "\nRecord/Target file\t:\t", self.recwav
            print "\nDuration\t\t:\t", str(self.reclen)
            print "\nSampling rate\t\t:\t", str(self.recsamprate)
            print "\nALSA command\t\t:\t", cmd
            print "\n" + "#" * 100 + "\n" + "#" * 100 + "\n"
        os.system(cmd)
        if self.DEBUG == 1:
            print "\nEnd of recording...\n"
#*----------------------------------------------------------------------------------------------------------------------

# Record audio using ALSA on a given input interface infinitely.

    def nrecordAudio(self, n, *args, **kwargs):
        if args:
            if len(args) > 0:
                self.inif = args[0]
                if len(args) > 1:
                    self.recsamprate = args[1]
                    if len(args) > 2:
                        self.recwav = args[2]
                        if len(args) > 3:
                            self.reclen = int(round(int(args[3])))
        if kwargs:
            validargs = ['inif', 'samplerate', 'recfile', 'recduration']
            argchk = checkkeywords(kwargs, validargs)
            if self.DEBUG == 1:
                print argchk
            if argchk != "No keywords match":
                if 'inif' in kwargs:
                    self.outif = kwargs['inif']
                if 'samplerate' in kwargs:
                    self.recsamprate = kwargs['samplerate']
                if 'recfile' in kwargs:
                    self.recwav = kwargs['recfile']
                if 'recduration' in kwargs:
                    self.reclen = int(round(int(kwargs['recduration'])))
            else:
                if self.DEBUG == 1:
                    print "\nKeyword error, using default values...."
        tmpfname = getfilename(self.recwav)
        origname = self.recwav
        for rt in range(0, n):
            self.recwav = tmpfname.split('.wav')[0] + "_" + str(rt + 1) + '.wav'
            cmd = "arecord -D plug:" + str(self.inif) + " -c 1 -d " + str(int(round(self.reclen))) + " -f S16_LE -r " \
                  + str(self.recsamprate) + " " + self.recwav
            if self.DEBUG == 1:
                print "\nRecording to " + self.recwav + " through the input interface " + str(self.inif) + "...."
                print "\nWill start recording now...."
                print "\n" + "#" * 100 + "\n" + "#" * 100
                print "\nRecord number\t\t:\t", str(rt + 1)
                print "\nRecord interface/channel:\t", str(self.inif)
                print "\nRecord/Target file\t:\t", self.recwav
                print "\nDuration\t\t:\t", str(self.reclen)
                print "\nSampling rate\t\t:\t", str(self.recsamprate)
                print "\nALSA command\t\t:\t", cmd
                print "\n" + "#" * 100 + "\n" + "#" * 100 + "\n"
            os.system(cmd)
            self.recwav = origname
        if self.DEBUG == 1:
            print "\nEnd of recording...\n"
#*----------------------------------------------------------------------------------------------------------------------

# Play and Record audio with shell command using ALSA on a given output/input interface pair to a given file.

    def playrecordAudio(self, *args, **kwargs):
        if args:
            if len(args) > 0:
                self.outif = args[0]
                if len(args) > 1:
                    self.playsamprate = args[1]
                    if len(args) > 2:
                        self.playwav = args[2]
                        if len(args) > 3:
                            self.inif = args[3]
                            if len(args) > 4:
                                self.recsamprate = args[4]
                                if len(args) > 5:
                                    self.recwav = args[5]
                                    if len(args) > 6:
                                        self.reclen = int(round(int(args[6])))
        if kwargs:
            validargs = ['outif', 'plsamplerate', 'playfile', 'inif', 'recsamplerate', 'recfile', 'recduration']
            argchk = checkkeywords(kwargs, validargs)
            if self.DEBUG == 1:
                print argchk
            if argchk != "No keywords match":
                if 'outif' in kwargs:
                    self.outif = kwargs['outif']
                if 'plsamplerate' in kwargs:
                    self.playsamprate = kwargs['plsamplerate']
                if 'playfile' in kwargs:
                    self.playwav = kwargs['playfile']
                if 'inif' in kwargs:
                    self.inif = kwargs['inif']
                if 'recsamplerate' in kwargs:
                    self.recsamprate = kwargs['recsamplerate']
                if 'recfile' in kwargs:
                    self.recwav = kwargs['recfile']
                if 'recduration' in kwargs:
                    self.reclen = int(round(int(kwargs['recduration'])))
            else:
                if self.DEBUG == 1:
                    print "\nKeyword error, using default values...."
        if self.DEBUG == 1:
            print "\nPlaying " + self.inwav + " through the output interface " + str(self.outif) + " and recording to " \
                  + self.recwav + " through the input interface " + str(self.inif) + " simultaneously (in the same " \
                  "command)...."
        # cmd = "{ sleep 0.5; aplay -D plug:" + str(self.outif) + " -c 1 -r " + str(self.playsamprate) + " " + \
        #       self.playwav + " ; }" + " | arecord -D plug:" + str(self.inif) + " -c 1 -d " + str(self.reclen + 1) + \
        #       " -f S16_LE -r " + str(self.recsamprate) + " " + self.recwav
        cmd = "aplay -D plug:" + str(self.outif) + " -c 1 -r " + str(self.playsamprate) + " " + \
              self.playwav + " | arecord -D plug:" + str(self.inif) + " -c 1 -d " + str(self.reclen + 1) + \
              " -f S16_LE -r " + str(self.recsamprate) + " " + self.recwav
        if self.replug:
            proberes = self.__usbreplug()
            if proberes == "not connected":
                return "PlayRecord failed"
            else:
                pass
        if self.DEBUG == 1:
            print "\n" + "#" * 100 + "\n" + "#" * 100
            print "\nPlay interface/channel\t:\t" + str(self.outif)
            print "\nPlaying file\t\t:\t", self.playwav
            print "\nSampling rate (play)\t:\t", self.playsamprate
            print "\nRecord interface/channel:\t", str(self.inif)
            print "\nRecord/Target file\t:\t", self.recwav
            print "\nDuration\t\t:\t", str(self.reclen)
            print "\nSampling rate (record)\t:\t", str(self.recsamprate)
            print "\nALSA command\t\t:\t", cmd
            print "\n" + "#" * 100 + "\n" + "#" * 100 + "\n"
        os.system(cmd)
        if self.DEBUG == 1:
            print "\nEnd of play and record...\n"

        return "PlayRecord successful"
#*----------------------------------------------------------------------------------------------------------------------

# Play and Record audio on threads using ALSA on a given output/input interface pair to a given file.

    def playrecordAudio_th(self, *args, **kwargs):
        if args:
            if len(args) > 0:
                self.outif = args[0]
                if len(args) > 1:
                    self.playsamprate = args[1]
                    if len(args) > 2:
                        self.playwav = args[2]
                        if len(args) > 3:
                            self.inif = args[3]
                            if len(args) > 4:
                                self.recsamprate = args[4]
                                if len(args) > 5:
                                    self.recwav = args[5]
                                    if len(args) > 6:
                                        self.reclen = int(round(int(args[6])))
        if kwargs:
            validargs = ['outif', 'plsamplerate', 'playfile', 'inif', 'recsamplerate', 'recfile', 'recduration']
            argchk = checkkeywords(kwargs, validargs)
            if self.DEBUG == 1:
                print argchk
            if argchk != "No keywords match":
                if 'outif' in kwargs:
                    self.outif = kwargs['outif']
                if 'plsamplerate' in kwargs:
                    self.playsamprate = kwargs['plsamplerate']
                if 'playfile' in kwargs:
                    self.playwav = kwargs['playfile']
                if 'inif' in kwargs:
                    self.inif = kwargs['inif']
                if 'recsamplerate' in kwargs:
                    self.recsamprate = kwargs['recsamplerate']
                if 'recfile' in kwargs:
                    self.recwav = kwargs['recfile']
                if 'recduration' in kwargs:
                    self.reclen = int(round(int(kwargs['recduration'])))
            else:
                if self.DEBUG == 1:
                    print "\nKeyword error, using default values...."
        if self.DEBUG == 1:
            print "\n\nWill start playing and recording simultaneously using threads...."
        if self.replug:
            proberes = self.__usbreplug()
            if proberes == "not connected":
                return "PlayRecord failed"
            else:
                pass
        thPlay = threading.Thread(name='SinglePlay', target=self.playAudio)
        thPlay.setDaemon(True)
        thRecord = threading.Thread(name='SingleRecord', target=self.recordAudio)
        thRecord.start()
        time.sleep(1)
        if self.DEBUG == 1:
            print "\nplayrecordAudio --> Record thread started...."
        thPlay.start()
        if self.DEBUG == 1:
            print "\nplayrecordAudio --> Play thread started...."
        thRecord.join()
        if self.DEBUG == 1:
            print "\nplayrecordAudio --> Record thread joined...."
        thPlay.join()
        if self.DEBUG == 1:
            print "\nplayrecordAudio --> Play thread joined...."
        time.sleep(1)

        return "PlayRecord successful"
#*----------------------------------------------------------------------------------------------------------------------

# Play and Record audio with shell command using ALSA on a given output interface to more than one input interfaces and
# any given corresponding file list.

    def playmultirecordAudio(self, *args, **kwargs):
        recording = 1
        if args:
            if len(args) > 0:
                self.outif = args[0]
                if len(args) > 1:
                    self.playsamprate = args[1]
                    if len(args) > 2:
                        self.playwav = args[2]
                        if len(args) > 3:
                            self.reciflst = args[3]
                            if len(args) > 4:
                                self.recsamprate = args[4]
                                if len(args) > 5:
                                    self.recwavlst = args[5]
                                    if len(args) > 6:
                                        self.reclen = int(round(int(args[6])))
        # num_if = len(iniflist)   ---->   move to calling function
        # num_files = len(recfilelist)
        # if num_if == num_files:
        #     num = num_if
        # else:
        #     if num_if > num_files:
        #         print "Not enough sinks...."
        #     elif num_if < num_files:
        #         print "Not enough sources...."
        #     sys.exit()
        if kwargs:
            validargs = ['outif', 'plsamplerate', 'playfile', 'iniflist', 'recsamplerate', 'recfilelist', 'recduration']
            argchk = checkkeywords(kwargs, validargs)
            if self.DEBUG == 1:
                print argchk
            if argchk != "No keywords match":
                if 'outif' in kwargs:
                    self.outif = kwargs['outif']
                if 'plsamplerate' in kwargs:
                    self.playsamprate = kwargs['plsamplerate']
                if 'playfile' in kwargs:
                    self.playwav = kwargs['playfile']
                if 'iniflist' in kwargs:
                    self.reciflst = kwargs['iniflist']
                if 'recsamplerate' in kwargs:
                    self.recsamprate = kwargs['recsamplerate']
                if 'recfilelist' in kwargs:
                    self.recwavlst = kwargs['recfilelist']
                if 'recduration' in kwargs:
                    self.reclen = int(round(int(kwargs['recduration'])))
            else:
                if self.DEBUG == 1:
                    print "\nKeyword error, using default values...."
        if self.DEBUG == 1:
            print "\nPlaying " + self.inwav + " through the output interface \'" + str(self.outif) + "\' and " \
                  "recording to " + str(self.recwavlst)[1:-1] + " through the input interface " + \
                  str(self.reciflst)[1:-1] + " simultaneously (in the same command)...."
        if self.replug:
            proberes = self.__usbreplug()
            if proberes == "not connected":
                return "PlayRecord failed"
            else:
                pass
        cmd = "aplay -D plug:" + str(self.outif) + " -c 1 -r " + str(self.playsamprate) + " " + self.playwav
        if self.DEBUG == 1:
            print "\nPlaying " + self.inwav + " through the output interface " + str(self.outif) + "...."
            print "\nWill start playing now...."
            print "\n" + "#" * 100 + "\n" + "#" * 100
            print "\nPlay interface/channel\t:\t" + str(self.outif)
            print "\nPlaying file\t\t:\t", self.playwav
            print "\nSampling rate\t\t:\t", self.playsamprate
            print "\nALSA command\t\t:\t", cmd
            print "\n" + "#" * 100 + "\n" + "#" * 100 + "\n"
        if self.DEBUG == 1:
            print "\n" + "*" * 100 + "\n" + "*" * 100
        for inif, infile in zip(self.reciflst, self.recwavlst):
            acmd = "arecord -D plug:" + str(inif) + " -c 1 -d " + str(self.reclen) + " -f S16_LE -r " + \
                   str(self.recsamprate) + " " + infile
            cmd += " | " + acmd
            if self.DEBUG == 1:
                print "\nRecording\t\t--->\t(" + str(recording) + ")"
                print "\nRecord interface/channel:\t", str(inif)
                print "\nRecord/Target file\t:\t", infile
                print "\nDuration\t\t:\t", str(self.reclen)
                print "\nSampling rate\t\t:\t", str(self.recsamprate)
                print "\nALSA command\t\t:\t", acmd
            recording += 1
        if self.DEBUG == 1:
            print "\n" + "*" * 100 + "\n" + "*" * 100 + "\n"
        os.system(cmd)
        if self.DEBUG == 1:
            print "\nEnd of play and record...\n"

        return "PlayRecord successful"
#*----------------------------------------------------------------------------------------------------------------------

# Play and Record audio on threads using ALSA on a given output interface to more than one input interfaces and
# any given corresponding file list.

    def playmultirecordAudio_th(self, *args, **kwargs):
        recording = 1
        if args:
            if len(args) > 0:
                self.outif = args[0]
                if len(args) > 1:
                    self.playsamprate = args[1]
                    if len(args) > 2:
                        self.playwav = args[2]
                        if len(args) > 3:
                            self.reciflst = args[3]
                            if len(args) > 4:
                                self.recsamprate = args[4]
                                if len(args) > 5:
                                    self.recwavlst = args[5]
                                    if len(args) > 6:
                                        self.reclen = int(round(int(args[6])))
        if kwargs:
            validargs = ['outif', 'plsamplerate', 'playfile', 'iniflist', 'recsamplerate', 'recfilelist', 'recduration']
            argchk = checkkeywords(kwargs, validargs)
            if self.DEBUG == 1:
                print argchk
            if argchk != "No keywords match":
                if 'outif' in kwargs:
                    self.outif = kwargs['outif']
                if 'plsamplerate' in kwargs:
                    self.playsamprate = kwargs['plsamplerate']
                if 'playfile' in kwargs:
                    self.playwav = kwargs['playfile']
                if 'iniflist' in kwargs:
                    self.reciflst = kwargs['iniflist']
                if 'recsamplerate' in kwargs:
                    self.recsamprate = kwargs['recsamplerate']
                if 'recfilelist' in kwargs:
                    self.recwavlst = kwargs['recfilelist']
                if 'recduration' in kwargs:
                    self.reclen = int(round(int(kwargs['recduration'])))
            else:
                if self.DEBUG == 1:
                    print "\nKeyword error, using default values...."
        num = len(self.recwavlst)
        if self.DEBUG == 1:
            print "\nPlaying " + self.inwav + " through the output interface \'" + str(self.outif) + \
                  "\' and recording  to " + str(self.recwavlst)[1:-1] + " through the input interface " + \
                  str(self.reciflst)[1:-1] + " simultaneously (using threads)...."
        if self.replug:
            proberes = self.__usbreplug()
            if proberes == "not connected":
                return "PlayRecord failed"
            else:
                pass
        tlist = []
        t1 = threading.Thread(name='MultiPlay', target=self.playAudio)
        t1.setDaemon(True)
        tlist.append(t1)
        if self.DEBUG == 1:
            print "\n" + "*" * 100 + "\n" + "*" * 100
        if num >= 1:
            t2 = threading.Thread(name='MultiRecord1', target=self.recordAudio, kwargs=dict(inif=self.reciflst[0],
                                                                                      recfile=self.recwavlst[0]))
            t2.start()
            tlist.append(t2)
            if num >= 2:
                t3 = threading.Thread(name='MultiRecord2', target=self.recordAudio, kwargs=dict(inif=self.reciflst[1],
                                                                                          recfile=self.recwavlst[1]))
                t3.start()
                tlist.append(t3)
                if num >= 3:
                    t4 = threading.Thread(name='MultiRecord3', target=self.recordAudio,
                                          kwargs=dict(self.reciflst[2], recfile=self.recwavlst[2]))
                    t4.start()
                    tlist.append(t4)
                    if num >= 4:
                        t5 = threading.Thread(name='MultiRecord4', target=self.recordAudio,
                                              kwargs=dict(inif=self.reciflst[3], recfile=self.recwavlst[3]))
                        t5.start()
                        tlist.append(t5)
        t1.start()
        for t in tlist:
            if t == t1:
                continue
            else:
                t.join()
        t1.join()
        if self.DEBUG == 1:
            print "\n" + "*" * 100 + "\n" + "*" * 100
            print "\nEnd of play and record...\n"

        return "PlayRecord successful"
#*----------------------------------------------------------------------------------------------------------------------

# Control the USB soundcard hardware using relays -- to switch off and switch on (replug).

    def __usbreplug(self):
        cnt = 0
        line = subprocess.check_output(["aplay", "-l"])
        if "Eight [M-Track Eight]" in line:
            return "connected"
        else:
            if self.DEBUG == 1:
                print "Replugging the USB soundcard...."
            os.system("sudo ./usbrelay " + self.relay_if + "=0")
            time.sleep(1)
            os.system("sudo ./usbrelay " + self.relay_if + "=1")
            line = subprocess.check_output(["aplay", "-l"])
            while "Eight [M-Track Eight]" not in line and cnt < 20:
                line = subprocess.check_output(["aplay", "-l"])
                if self.DEBUG == 1:
                    print "Sound card probe....", line
                time.sleep(1)
                cnt += 1
            if cnt == 20:
                return "not connected"
            time.sleep(5)
#*----------------------------------------------------------------------------------------------------------------------



from essentia.standard import *



"""
EALPlayRecord functions use Essentia audio libraries to play and record audio under various scenarios. Supports parallel 
recordings on multiple interfaces.
"""



class EALPlayRecord:
    def __init__(self, debug=0):
        self.playpath = "" # Will remain constant
        self.recpath = "" # Will vary from case to case
        self.playsamprate = 8000
        self.recsamprate = 8000
        self.outif = ""
        self.inif = ""
        self.playif = []
        self.reciflst = []
        self.playtimes = 1
        self.reclen = 9 # Only integer calues are accepted by ALSA
        self.multiple_th = 2
        self.inwav = ""
        self.outwav = ""
        self.playwav = self.playpath + self.inwav
        self.recwav = self.recpath + self.outwav
        self.replug = 0 # Will determine if sound card is relay controlled and if it needs to be unplugged and replugged
        self.relayif = "VN407_1" # The relay ID and pin number connected to the power cable of USB soundcard
        self.DEBUG = debug
#*----------------------------------------------------------------------------------------------------------------------

# Play audio using ALSA on a given output interface.

    def playAudio(self, **kwargs):
        if kwargs:
            validargs = ['outif', 'samplerate']
            argchk = checkkeywords(kwargs, validargs)
            if self.DEBUG == 1:
                print argchk
            if argchk != "No keywords match":
                if 'outif' in kwargs:
                    self.outif = kwargs['outif']
                if 'samplerate' in kwargs:
                    self.playsamprate = kwargs['samplerate']
            else:
                if self.DEBUG == 1:
                    print "Keyword error, using default values...."
        self.inwav = getfilename(self.playwav)
        cmd = "aplay -D plug:" + str(self.outif) + " -c 1 -r " + str(self.playsamprate) + " " + self.playwav
        if self.DEBUG == 1:
            print "Playing " + self.inwav + " through the output interface " + str(self.outif) + "...."
            print "Will start playing now...."
            print "#" * 100
            print "#" * 100
            print "Play interface/channel : " + str(self.outif)
            print "Playing file : ", self.playwav
            print "Sampling rate : ", self.playsamprate
            print "ALSA command : ", cmd
            print "#" * 100
            print "#" * 100
        os.system(cmd)
        if self.DEBUG == 1:
            print "End of play...\n"
#*----------------------------------------------------------------------------------------------------------------------



# ----------------------------------------------------------------------------------
# Play a wav file through the sound object
# http://pymedia.org/
##fname="C:\CCM_WA\VoIP823_Automation\Input_Wave_Config_Files\sirtest.wav"
##card=4
##playWAV(fname,card)

# import pymedia.audio.sound as soundCard
# import pymedia.audio.acodec as acodec



"""
PMLPlayRecord functions uses python's package 'pymedia' to play and record audio under various scenarios.
NOTE: LEGACY CODE. CURRENTLY NOT USED.
"""



class PMLPlayRecord(object):
    def play_file(card):
    # Asume the very first is the the Master volume
        volume= 6800
        conns= sound.Mixer().getControls()
        if len( conns ):
            conns[ 0 ][ 'control' ].setValue(volume )
        print "Started Playing\n"
        f = wave.open('C:\automation\DVF99_Automation\Input\test.wav', 'rb')
        p_samplerate = f.getframerate()
        p_channels = f.getnchannels()
        p_format = soundCard.AFMT_S16_LE
        snd = soundCard.Output(p_samplerate, p_channels, p_format, 0)
        s = f.readframes(300000)
        snd.play(s)
        # s= ' '
        # while len( s ):
        #     s= f.readframes(512)
        #     snd1.play( s )
    # Since sound module is not synchronous we want everything to be played before we exit
        while snd.isPlaying():
            time.sleep(0.05)
#*----------------------------------------------------------------------------------------------------------------------


    def record_file():
        print "\nStarted Recording\n"
        g = open('C:\automation\DVF99_Automation\Output\test.wav', 'wb')
        cparams = {'id': acodec.getCodecID('wav'),
                   'bitrate': 128000,
                   'sample_rate': 8000,
                   'channels': 1}
        r_samplerate = 8000
        r_channels = 1
        r_format = soundCard.AFMT_S16_LE
        ac = acodec.Encoder(cparams)
        snd = soundCard.Input(r_samplerate, r_channels, r_format)
        snd.start()
        while snd.getPosition() <= 8.5:
            s = snd.getData()
            if s and len(s):
                for fr in ac.encode(s):
                    g.write(fr)
            else:
                time.sleep(0.5)
        snd.stop()
#*----------------------------------------------------------------------------------------------------------------------


    def play_record():
        thread.start_new_thread(play_file, ())
        thread.start_new_thread(record_file, ())
#*----------------------------------------------------------------------------------------------------------------------



if __name__ == '__main__':
    print "\n\n" + 120 * "%" + "\n\n\t\t\t\t\tProgram to PLAY and/or RECORD Audio\n\n" + 120 * "%" + "\n\n"

    homedir = os.environ['HOME']
    options = 1
    type = "play-record"

    numplay = 2
    numrec = 2

    plrec = SYSPlayRecord(debug=1)
    plrec.playpath = homedir + '/automation_v5/automation/voip_automation/DVF_Automation/Input/audio/'
    plrec.playwav = plrec.playpath + 'male_8k.wav'
    plrec.recpath = homedir + '/Downloads/wav_out/'
    plrec.outwav = 'output.wav'
    plrec.recwav = plrec.recpath + plrec.outwav

    optargparser = argparse.ArgumentParser(description='Program\'s Description : Play and record audio files using a PC'
                                                       ' sound card\'s output and input channels/interfaces.',
                                           prog='audplayrec.py', usage='%(prog)s [options]')
    proghelp = "The type of function to be executed:" \
               " 1 --> play a specified file," \
               " 2 --> record from a specific interface/channel," \
               " 3 --> play multiple times on a loop on a specific interface/channel," \
               " 4 --> record multiple times on a loop on a specific interface/channel," \
               " 5 --> play on a specific interface and record at a specific interface/channel," \
               " 6 --> play on a specific interface and record at a multiple interfaces/channels,"
    if len(sys.argv) > 1:
        optargparser.add_argument('-t', '--type', type=int, dest='t', help=proghelp, required=True)
    else:
        optargparser.add_argument('-t', '--type', type=int, dest='t', help=proghelp)
    optargparser.add_argument('-o', '--outiface', dest='o', help="The output interface/channel for a file to be "
                                                                 "played at.")
    optargparser.add_argument('-s', '--psamprate', type=int, dest='s', help="The sample rate of the audio output to "
                                                                              "be played at the output "
                                                                              "interface/channel (in Hz).")
    optargparser.add_argument('-p', '--playfile', dest='p', help="The audio file (.wav) to be played at the output "
                                                                 "interface/channel.")
    optargparser.add_argument('-n', '--playnum', type=int, dest='n', help="The number of times a given audio file "
                                                                          "should be played.")
    optargparser.add_argument('-m', '--recnum', type=int, dest='m', help="The number of times audio should be recorded "
                                                                         "at a given input interface/channel for a "
                                                                         "given duration.")
    optargparser.add_argument('-i', '--iniface', dest='i', help="The input interface(s)/channel(s) to be played at. In "
                                                                "case of multiple interfaces involved, "
                                                                "separate them by a comma(',') without any "
                                                                "whitespace characters.")
    optargparser.add_argument('-f', '--rsamprate', type=int, dest='f', help="The sample rate of the audio output to be "
                                                                            "recorded at the input interface/channel "
                                                                            "(in Hz).")
    optargparser.add_argument('-r', '--recfiles', dest='r', help="The audio filename(s) to store recorded data, "
                                                                 "corresponding to the interface(s) given.")
    optargparser.add_argument('-d', '--recdur', type=int, dest='d', help="The duration (in seconds) of file(s) to be "
                                                                         "recorded.")

    try:
        optionsgiven = vars(optargparser.parse_args())
        print "optionsgiven : ", optionsgiven
    except argparse.ArgumentError:
        print "\nError in command-line inputs....\n"
        options = 0
    if not len(sys.argv) > 1:
        print "\nNot taking any command-line inputs....\n"
        options = 0

    if options == 1:
        for opt, arg in optionsgiven.items():
            if opt == 't' and arg is not None:
                if int(arg) == 1:
                    type = "play"
                elif int(arg) == 2:
                    type = "record"
                elif int(arg) == 3:
                    type = "play-loop"
                elif int(arg) == 4:
                    type = "record-loop"
                elif int(arg) == 5:
                    type = "play-record"
                elif int(arg) == 6:
                    type = "play-multiplerecord"
            elif opt == 'o' and arg is not None:
                plrec.outif = arg
            elif opt == 'p' and arg is not None:
                plrec.outwav = arg
            elif opt == 'n' and arg is not None:
                numplay = int(arg)
            elif opt == 'm' and arg is not None:
                numrec = int(arg)
            elif opt == 'i' and arg is not None:
                lst = arg.split(',')
                if len(lst) == 1:
                    plrec.inif = arg
                elif len(lst) > 1:
                    plrec.reciflst = lst
            elif opt == 'r' and arg is not None:
                lst = arg.split(',')
                if len(lst) == 1:
                    plrec.recwav = arg
                elif len(lst) > 1:
                    plrec.recwavlst = lst
            elif opt == 's' and arg is not None:
                plrec.playsamprate = int(arg)
            elif opt == 'f' and arg is not None:
                plrec.recsamprate = int(arg)
            elif opt == 'd' and arg is not None:
                plrec.reclen = int(arg)

        if type == 'play':
            plrec.playAudio()
            # plrec.playAudio('outch1', 16000)
            # plrec.playAudio('outch1', 24000, plrec.playpath + "male_16k.wav")
            # plrec.playAudio(outif='outch1')
            # plrec.playAudio(samplerate=16000)
            # plrec.playAudio(playfile=plrec.playpath + "male_16k.wav", samplerate=48000, outif='outch2')
            # plrec.playAudio(samplerate=32000, playfile=plrec.playpath + "male_16k.wav", outif='outch3')
        elif type == 'play-loop':
            plrec.nplayAudio(numplay)
            plrec.nplayAudio(2, 'outch1')
            plrec.nplayAudio(3, 'outch1')
            plrec.nplayAudio(2, 'outch1', 16000)
            plrec.nplayAudio(3, 'outch1', 24000, plrec.playpath + "male_16k.wav")
            plrec.nplayAudio(2, outif='outch1')
            plrec.nplayAudio(3, samplerate=16000)
            plrec.nplayAudio(2, playfile=plrec.playpath + "male_16k.wav", samplerate=48000, outif='outch2')
            plrec.nplayAudio(3, samplerate=32000, playfile=plrec.playpath + "male_16k.wav", outif='outch3')
        elif type == 'record':
            plrec.recordAudio('inch1')
            plrec.recordAudio('inch2', 24000)
            plrec.recordAudio('inch1', 16000, plrec.recpath + "new.wav")
            plrec.recordAudio('inch1', 16000, plrec.recpath + "new.wav", 4.5)
            plrec.recordAudio(inif='inch2')
            plrec.recordAudio(samplerate=16000)
            plrec.recordAudio(recfile=plrec.recpath + "rec.wav", recduration=4, samplerate=48000, inif='inch2')
            plrec.recordAudio(recduration=5.55, samplerate=16000, recfile=plrec.recpath + "recording.wav", inif='inch1')
        elif type == 'record-loop':
            plrec.nrecordAudio(numrec)
            plrec.nrecordAudio(2, 'inch1')
            plrec.nrecordAudio(3, 'inch2', 24000)
            plrec.nrecordAudio(2, 'inch1', 16000, plrec.recpath + "new.wav")
            plrec.nrecordAudio(3, 'inch1', 8000, plrec.recpath + "new.wav", 4.5)
            plrec.nrecordAudio(2, outif='inch1')
            plrec.nrecordAudio(3, samplerate=16000)
            plrec.nrecordAudio(2, recfile=plrec.recpath + "rec.wav", recduration=4, samplerate=48000, inif='inch2')
            plrec.nrecordAudio(3, recduration=5.55, samplerate=16000, recfile=plrec.recpath + "recording.wav", 
                               inif='inch1')
        elif type == 'play-record':
            plrec.playrecordAudio('outch1', 8000, plrec.playwav, 'inch1', 8000, plrec.recwav)
            plrec.playrecordAudio('outch1', 8000, plrec.playwav, 'inch1', 8000, plrec.recpath + "mini.wav", 5)
            plrec.playrecordAudio(outif='outch1', inif='inch1', plsamplerate=8000, recsamplerate=16000)
            plrec.playrecordAudio(recfile=plrec.recpath + "minirec.wav", outif='outch1', inif='inch1', recduration=6)
    
            # plrec.playrecordAudio_th('outch1', 8000, plrec.playwav, 'inch1', 8000, plrec.recwav)
            # plrec.playrecordAudio_th('outch1', 8000, plrec.playwav, 'inch1', 8000, plrec.recpath + "mini.wav", 5)
            # plrec.playrecordAudio_th(outif='outch1', inif='inch1', plsamplerate=8000, recsamplerate=16000)
            # plrec.playrecordAudio_th(recfile=plrec.recpath + "minirec.wav", outif='outch1', inif='inch1', recduration=6)
        elif type == 'play-multiplerecord':
            plrec.playmultirecordAudio('outch1', 8000, plrec.playwav, ['inch1', 'inch2'], 8000, ['output_1.wav',
                                                                                                 'output_2.wav'])
            plrec.playmultirecordAudio('outch2', 8000, plrec.playwav, ['inch2', 'inch1'], 8000, ['output_1.wav',
                                                                                                 'output_2.wav'], 5)
            plrec.playmultirecordAudio('outch1', 8000, plrec.playwav, ['inch1', 'inch2'], 8000, ['output_1.wav',
                                                                                                 'output_2.wav'])

            # plrec.playmultirecordAudio_th('outch1', 8000, plrec.playwav, ['inch1', 'inch2'], 8000,
            #                               ['output_1.wav', 'output_2.wav'])
            # plrec.playmultirecordAudio_th('outch2', 8000, plrec.playwav, ['inch2', 'inch1'], 8000,
            #                               ['output_1.wav', 'output_2.wav'])
    else:
        plrec.playAudio('outch1')
        plrec.playAudio('outch1', 16000)
        plrec.playAudio('outch1', 24000, plrec.playpath + "male_16k.wav")
        plrec.playAudio(outif='outch1')
        plrec.playAudio(samplerate=16000)
        plrec.playAudio(playfile=plrec.playpath + "male_16k.wav", samplerate=48000, outif='outch2')
        plrec.playAudio(samplerate=32000, playfile=plrec.playpath + "male_16k.wav", outif='outch3')

        # plrec.nplayAudio(2, 'outch1')
        # plrec.nplayAudio(3, 'outch1')
        # plrec.nplayAudio(2, 'outch1', 16000)
        # plrec.nplayAudio(3, 'outch1', 24000, plrec.playpath + "male_16k.wav")
        # plrec.nplayAudio(2, outif='outch1')
        # plrec.nplayAudio(3, samplerate=16000)
        # plrec.nplayAudio(2, playfile=plrec.playpath + "male_16k.wav", samplerate=48000, outif='outch2')
        # plrec.nplayAudio(3, samplerate=32000, playfile=plrec.playpath + "male_16k.wav", outif='outch3')
        #
        # plrec.recordAudio('inch1')
        # plrec.recordAudio('inch2', 24000)
        # plrec.recordAudio('inch1', 16000, plrec.recpath + "new.wav")
        # plrec.recordAudio('inch1', 16000, plrec.recpath + "new.wav", 4.5)
        # plrec.recordAudio(inif='inch2')
        # plrec.recordAudio(samplerate=16000)
        # plrec.recordAudio(recfile=plrec.recpath + "rec.wav", recduration=4, samplerate=48000, inif='inch2')
        # plrec.recordAudio(recduration=5.55, samplerate=16000, recfile=plrec.recpath + "recording.wav", inif='inch1')
        #
        # plrec.nrecordAudio(2, 'inch1')
        # plrec.nrecordAudio(3, 'inch2', 24000)
        # plrec.nrecordAudio(2, 'inch1', 16000, plrec.recpath + "new.wav")
        # plrec.nrecordAudio(3, 'inch1', 8000, plrec.recpath + "new.wav", 4.5)
        # plrec.nrecordAudio(2, outif='inch1')
        # plrec.nrecordAudio(3, samplerate=16000)
        # plrec.nrecordAudio(2, recfile=plrec.recpath + "rec.wav", recduration=4, samplerate=48000, inif='inch2')
        # plrec.nrecordAudio(3, recduration=5.55, samplerate=16000, recfile=plrec.recpath + "recording.wav", inif='inch1')
        #
        # plrec.playrecordAudio('outch1', 8000, plrec.playwav, 'inch1', 8000, plrec.recwav)
        # plrec.playrecordAudio('outch1', 8000, plrec.playwav, 'inch1', 8000, plrec.recpath + "mini.wav", 5)
        # plrec.playrecordAudio(outif='outch1', inif='inch1', plsamplerate=8000, recsamplerate=16000)
        # plrec.playrecordAudio(recfile=plrec.recpath + "minirec.wav", outif='outch1', inif='inch1', recduration=6)
        #
        # plrec.playrecordAudio_th('outch1', 8000, plrec.playwav, 'inch1', 8000, plrec.recwav)
        # plrec.playrecordAudio_th('outch1', 8000, plrec.playwav, 'inch1', 8000, plrec.recpath + "mini.wav", 5)
        # plrec.playrecordAudio_th(outif='outch1', inif='inch1', plsamplerate=8000, recsamplerate=16000)
        # plrec.playrecordAudio_th(recfile=plrec.recpath + "minirec.wav", outif='outch1', inif='inch1', recduration=6)
        #
        # plrec.playmultirecordAudio('outch1', 8000, plrec.playwav, ['inch1', 'inch2'], 8000, ['output_1.wav',
        #                                                                                      'output_2.wav'])
        # plrec.playmultirecordAudio('outch2', 8000, plrec.playwav, ['inch2', 'inch1'], 8000, ['output_1.wav',
        #                                                                                      'output_2.wav'], 5)
        # plrec.playmultirecordAudio('outch1', 8000, plrec.playwav, ['inch1', 'inch2'], 8000, ['output_1.wav',
        #                                                                                      'output_2.wav'])
        #
        # plrec.playmultirecordAudio_th('outch1', 8000, plrec.playwav, ['inch1', 'inch2'], 8000,
        #                               ['output_1.wav', 'output_2.wav'])
        # plrec.playmultirecordAudio_th('outch2', 8000, plrec.playwav, ['inch2', 'inch1'], 8000,
        #                               ['output_1.wav', 'output_2.wav'])

    print "\n\n" + 120 * "%" + "\n\n\t\t\t\t\tProgram to PLAY and/or RECORD Audio\n\n" + 120 * "%" + "\n\n"
