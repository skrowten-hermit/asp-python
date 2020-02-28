


########################################################################################################################
########################################################################################################################
## File              :: lib/generic/globalutils.py
## Description       :: VoIP Automation Common API : All the generic independent global functions not native to sdk.
## Developer         :: Sreekanth S
## Version           :: v2.0
## Release Date      :: 08/04/2019
## Changes made      :: Minimized and compressed API made out of earlier version.
## Changes made Date :: 11/04/2019
## Changes made by   :: Sreekanth S
########################################################################################################################
########################################################################################################################



import sys



"""
The following are the global utility functions which would be used in the libraries, platform packages and elsewhere.
"""



# Check if user has passed valid keywords to a function.

def checkkeywords(kwlist, validargs):
    arglist = []
    invalidcnt = 0
    for key, values in kwlist.items():
        arglist.append(key)
    argnum = len(arglist)
    for itm in arglist:
        if itm not in validargs:
            invalidcnt += 1
    if invalidcnt == argnum:
        return "No keywords match"
    else:
        return "Valid keyword(s) found"
#*----------------------------------------------------------------------------------------------------------------------



# Pad a given hexadecimal number with leading 0s.

def hexpad(hexin):
    print "input Hex : ", hexin
    print "Converting hex to writable form...."
    resulthex = "{0:#0{1}x}".format(hexin, 10).split('x')[1]
    return resulthex
#*----------------------------------------------------------------------------------------------------------------------



# Convert a given decimal number to an equivalent hexadecimal mask.

def dectohexmask(decin):
    hex_result = ''
    binhex = '00000000'
    t = 8 - decin
    print "Converting decimal to hex bit mask...."
    binhex = binhex[:t] + '1' + binhex[t + 1:]
    hexresult = hex(int(binhex, 2))
    hexmask = hexresult.split('x')[1]
    return hexmask
#*----------------------------------------------------------------------------------------------------------------------



# Convert a given decimal number to an equivalent hexadecimal number.

def dectohex(decin):
    hexnum = str(hex(int(decin, 10))).split('x')[1].zfill(2)
    return hexnum
#*----------------------------------------------------------------------------------------------------------------------



# Convert a given binary number to an equivalent hexadecimal number.

def bintohex(binin):
    hexnum = str(hex(int(binin, 2))).split('x')[1].zfill(2)
    return hexnum
#*----------------------------------------------------------------------------------------------------------------------



# Convert a given hexadecimal number to an equivalent binary number.

def hextobin(hexnum):
    binnum = str(bin(int(hexnum,16))[2:].zfill(8))
    return binnum
#*----------------------------------------------------------------------------------------------------------------------



# Translate a given hexadecimal to string for mask operations.

def hextranslate(inval):
    print "Translate hexadecimal to string for mask operations...."
    print "inval = ", inval
    strchk = isinstance(inval, basestring)
    if strchk == True:
        hexin = hex(int(inval, 16))
    else:
        hexin = inval
    print "input in hex = ", hexin
    hexresult = str(hexin).split('x')[1]
    return hexresult
#*----------------------------------------------------------------------------------------------------------------------



# Create hexadecimal mask of any given precision.

def makehexmask(nbits, lsb):
    print "Create hexadecimal mask...."
    zbits = 8 - nbits
    if lsb == 1:
        binmask = nbits * '0' + zbits * '1'
    else:
        binmask = nbits * '1' + zbits * '0'
    hexmask = str(hex(int(binmask, 2))).split('x')[1]
    return hexmask
#*----------------------------------------------------------------------------------------------------------------------



# Return Hexadecimal byte from a given hex number.

def hexbyte(hexin):
    print "input hex number : ", hexin
    binnum = hextobin(hexin)
    hbyte = '{:0{}x}'.format(int(binnum, 2), len(binnum) / 4)
    return hbyte
#*----------------------------------------------------------------------------------------------------------------------



# Extract MSB using a hex mask.

def extracthex(hexval, hexmask):
    print "Extract MSB using a hex mask...."
    msb = str(hex(int(hexval, 16) & int(hexmask, 16))).split('x')[1]
    return msb
#*----------------------------------------------------------------------------------------------------------------------



# Retrieve filename from a given Linux path.

def applyhexmask(msb, lsb):
    print "Apply strict hex mask...."
    hexres = str(hex(int(msb, 16) | int(lsb, 16))).split('x')[1]
    return hexres
#*----------------------------------------------------------------------------------------------------------------------



# Find the immediately next power of 2 of a given number.

def nextpowerof2(num):
    n = 1
    while n < num:
        n *= 2
    return n
#*----------------------------------------------------------------------------------------------------------------------



# Rounding a given value 'x' to nearest given base number.

def customroundoff(x, base=100):
    return base * round(x / base)
#*----------------------------------------------------------------------------------------------------------------------



# Find the index of a substring in a given string.

def findsubstringindex(listip, substr):
    for i, s in enumerate(listip):
        if substr in s:
            return i
    return -1
#*----------------------------------------------------------------------------------------------------------------------



# Retrieve hostname of host PC.

def gethostname():
    if 'subprocess' not in sys.modules:
        import subprocess
    hname = (subprocess.check_output(['hostname'])).strip()
    return hname
#*----------------------------------------------------------------------------------------------------------------------



# Retrieve username of host PC.

def getusername():
    if 'subprocess' not in sys.modules:
        import subprocess
    uname = str((subprocess.check_output(['whoami'])).strip())
    return uname
#*----------------------------------------------------------------------------------------------------------------------



# Retrieve host PC.

def gethost():
    uname = getusername()
    hname = gethostname()
    host = uname + '@' + hname
    return host
#*----------------------------------------------------------------------------------------------------------------------



# Retrieve filename from a given Linux path.

def getfilename(path):
    dtree = path.split('/')
    ltree = len(dtree)
    fname = dtree[ltree - 1]
    return fname
#*----------------------------------------------------------------------------------------------------------------------



# Start udp_reply server on a host PC.

def getipv4(linktype, link):
    if 'subprocess' not in sys.modules:
        import subprocess
    if 'time' not in sys.modules:
        import time
    if linktype == 1 or linktype == 2: # Serial or telnet connection to a board
        link.write("\n")
        link.write("root\n")
        link.write("\n")
        time.sleep(1)
        print "Logged in, getting the IPv4 address...."
        link.write("ifconfig\n")
        time.sleep(1)
    elif linktype == 0: # for the host PC
        read_buf = (subprocess.check_output(['ifconfig'])).strip()
    if linktype == 1: # Serial connection
        read_buf = link.read(1500)
    elif linktype == 2: # Telnet connection
        time.sleep(0.5)
        read_buf = link.read_very_eager()
    print "Buffer Contents : \n", read_buf
    ipv4res = read_buf.split('inet addr:')[1]
    ipv4addr = ipv4res.split('  Bcast:')[0]
    print "IP address is = ", ipv4addr
    return ipv4addr
#*----------------------------------------------------------------------------------------------------------------------



# Start udp_reply server on a host PC.

def start_udpreply(ipv4addr, path):
    if 'os' not in sys.modules:
        import os
    if 'subprocess' not in sys.modules:
        import subprocess
    os.system("cd " + path + "\n")
    print "Starting UDP reply server on ", ipv4addr
    cmd = path + './udp_reply -p 8500'
    p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
    # thread.exit()
#*----------------------------------------------------------------------------------------------------------------------



# Write data to a log file.

def logtofile(logfile, bufferstr, initflg, head):
    titlestr = 80 * "*" + "\n"
    if int(initflg):
        logfile.write("\n" + titlestr)
        logfile.write(titlestr)
        logfile.write(titlestr)
        logfile.write(str(head)+"\n")
        logfile.write(titlestr)
        logfile.write(bufferstr)
        logfile.close()
    else:
        logfile.write(str(bufferstr))
        logfile.close()
#*----------------------------------------------------------------------------------------------------------------------



# TODO: Check integrity of transferfiletoboard() and remove this redundant function.

def transfer_wav(ip_addr, path):
    if 'subprocess' not in sys.modules:
        import subprocess
    print "Transferring Wave file to the board for playing in the background....", ip_addr
    in_file = path + "male_16k.wav"
    print "The file to be used as a sample for playing : ", in_file
    cmd = 'scp -o StrictHostKeyChecking=no ' + in_file +' root@' + str(ip_addr) + ':/data/sample.wav'
    p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
#*----------------------------------------------------------------------------------------------------------------------



# Transfer files (types .txt, .wav, .xml) to a board over SCP.

def transferfiletoboard(ipv4addr, filetype, path, filename):
    if 'subprocess' not in sys.modules:
        import subprocess
    if filetype == '.wav':
        print "Transferring Wave file from the host PC to the board for playing in the background....", ipv4addr
    elif filetype == '.txt':
        print "Transferring .txt file from the host PC to the board....", ipv4addr
    elif filetype == '.xml':
        print "Transferring .xml file from the host PC to the board....", ipv4addr
    infile = path + filename
    print "The file to be transferred : ", infile
    if filetype == '.wav':
        cmd = 'scp -o StrictHostKeyChecking=no ' + infile +' root@' + str(ipv4addr)+':/data/sample.wav'
    else:
        cmd = 'scp -o StrictHostKeyChecking=no ' + infile +' root@' + str(ipv4addr)+':/data/' + filename
    p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
#*----------------------------------------------------------------------------------------------------------------------



# Add sub-directorie(s) from the same directory to a tar file.

def tardir(multi, dirpath, dirs, tname):
    if 'os' not in sys.modules:
        import os
    if 'time' not in sys.modules:
        import time
    dstr = ""
    tname += '_' + time.strftime("%d/%m/%Y, %H:%M:%S") + '.tar.bz2'
    outputarch = dirpath + tname
    if multi == 1:
        print "Compressing and accumulating multiple directories into a single tar file " + tname + "...."
        for d in dirs:
            if dstr == "":
                dstr += dirpath + d
            else:
                dstr += " " + dirpath + d
    elif multi == 0:
        print "Compressing and accumulating directory contents into a tar file " + tname + "...."
        dstr = dirs
    cmd = "tar -cjvf " + outputarch + " " + dstr
    os.system(cmd)
    return outputarch
#*----------------------------------------------------------------------------------------------------------------------



# Selectively add files from the same directory to a tar file.

def tarfiles(filelist, opath, tname):
    if 'os' not in sys.modules:
        import os
    if 'time' not in sys.modules:
        import time
    fstr = ""
    tname += '_' + time.strftime("%d/%m/%Y, %H:%M:%S") + '.tar.bz2'
    outputarch = opath + tname
    print "Compressing and putting " + ', '.join(getfilename(f) for f in filelist) + " in the tar file " + tname + "...."
    for f in filelist:
        if fstr == "":
            fstr += opath + f
        else:
            fstr += " " + opath + f
    cmd = "tar -cjvf " + outputarch + " " + fstr
    os.system(cmd)
    return outputarch
#*----------------------------------------------------------------------------------------------------------------------


# Expand the shorthand notation for USB ports to actual PC port names.

def prepareserial(compressedpnum):
    if 'U' in compressedpnum:
        expandedpnum = '/dev/ttyUSB' + compressedpnum.split('U')[1]
    elif 'S' in compressedpnum:
        expandedpnum = '/dev/ttyS' + compressedpnum.split('S')[1]
    elif 'M' in compressedpnum:
        expandedpnum = '/dev/ttyMI' + compressedpnum.split('M')[1]
    elif 'N' in compressedpnum:
        expandedpnum = '/dev/ttySX' + compressedpnum.split('N')[1]

    return expandedpnum
#*----------------------------------------------------------------------------------------------------------------------



# Login to board via Telnet.

def telnet_login(tn, boardname, debug):
    if 'time' not in sys.modules:
        import time
    cset = 'None'
    print "Attempting Telnet connection...."
    read_buf = tn.read_until("login: ")
    if debug == 1:
        print read_buf
    if "dvf9918 login" in read_buf:
        cset = 9918
    elif "dvf99 login" in read_buf:
        cset = 99
    elif "dvf101 login" in read_buf:
        cset = 101
    elif "dvf97 login" in read_buf:
        cset = 97
    elif "dspg login" in read_buf:
        cset = 1100
    else:
        cset = 'None'
    if debug == 1:
        print read_buf
    tn.write("root\n")
    time.sleep(1)
    tn.write("\n")
##    Checking chipset family flag
    if cset == 101:
        print "\n**********DVF101 login**********\n"
        read_buf = tn.read_until("root@dvf101:~#")
        if debug == 1:
            print read_buf
        if "root@dvf101:~#" in read_buf:
            print "Logged in successfully on " + str(boardname) + " (DVF101)....\n"
            tn.write("\n")
        else:
            print "Login failed on " + str(boardname) + " (DVF101)...!!!\n"
            tn.write("\n")
        print "\n**********DVF101 login**********\n"
    elif cset == 97:
        print "\n**********DVF97 login**********\n"
        read_buf = tn.read_until("root@dvf97:~#")
        if debug == 1:
            print read_buf
        if "root@dvf97:~#" in read_buf:
            print "Logged in successfully on " + str(boardname) + " (DVF97)....\n"
            tn.write("\n")
        else:
            print "Login failed on " + str(boardname) + " (DVF97)...!!!\n"
            tn.write("\n")
        print "\n**********DVF97 login**********\n"
    elif cset == 9919:
        read_buf = tn.read_until("root@dvf99:~#")
        if debug == 1:
            print read_buf
        if "root@dvf99:~#" in read_buf:
            print "Logged in successfully on " + str(boardname) + " (DVF9919)....\n"
            tn.write("\n")
        else:
            print "\n**********DVF9919 login**********\n"
            print "Log in failed on " + str(boardname) + " (DVF9919)...!!!\n"
            tn.write("\n")
        print "\n**********DVF9919 login**********\n"
    elif cset == 9918:
        read_buf = tn.read_until("root@dvf9918:~#")
        if debug == 1:
            print read_buf
        if "root@dvf9918:~#" in read_buf:
            print "Logged in successfully on " + str(boardname) + " (DVF9918)....\n"
            tn.write("\n")
        else:
            print "\n**********DVF9918 login**********\n"
            print "Log in failed on " + str(boardname) + " (DVF9918)...!!!\n"
            tn.write("\n")
        print "\n**********DVF9918 login**********\n"
    elif cset == 1100:
        print "\n**********DVF1100 login**********\n"
        read_buf = tn.read_until("root@dspg:~#")
        if debug == 1:
            print read_buf
        if ":~#" in read_buf:
            print "Logged in successfully on " + str(boardname) + " (DVF1100)....\n"
            print tn.write("\n")
        else:
            print "Login failed on " + str(boardname) + " (DVF1100)...!!!\n"
            tn.write("\n")
        print "\n**********DVF1100 login**********\n"

    else:
        print "\n**********Telnet login**********\n"
        print "Unsupported platform...."
        print "\n**********Telnet login**********\n"

    return cset
#*----------------------------------------------------------------------------------------------------------------------



if __name__ == '__main__':
    print "Global utility functions library...."

    result01 = checkkeywords([], [])
    print result01

    result02 = hexpad('4C')
    print result02

    result03 = dectohexmask(17)
    print result03

    result04 = dectohex(29)
    print result04

    result05 = bintohex(1011)
    print result05

    result06 = hextranslate(0x45)
    print result06

    result07 = makehexmask(5, 45)
    print result07

    result08 = hexbyte(0x6D)
    print result08

    result09 = extracthex()
    print result09

    result10 = applyhexmask()
    print result10

    result11 = nextpowerof2(3)
    print result11

    result12 = customroundoff(19)
    print result12

    result13 = findsubstringindex()
    print result13

    result14 = gethostname()
    print result14

    result15 = getusername()
    print result15

    result16 = gethost()
    print result16

    result17 = getfilename('/home/dsp/auto/help.doc')
    print result17

    result18 = getipv4(0, '')
    print result18
    ser = ""
    result18 = getipv4(1, ser)
    print result18
    tn = ""
    result18 = getipv4(2, tn)
    print result18

    result19 = start_udpreply('172.28.4.56', '/home/dsp/tools/')
    print result19

    result20 = logtofile('test.log', "Hello", 1, "****Message****")
    print result20
    result20 = logtofile('test.log', "World is cruel", 1, "****Thought****")
    print result20

    result21 = transfer_wav('172.28.4.57', '/home/dsp/wav_out/')
    print result21
    result21 = transferfiletoboard('172.28.4.57', 'wav', '/home/dsp/wav_out/', 'abc.wav')
    print result21

    result22 = tardir(0, '/home/dsp/', ['documents/'], 'example')
    print result22
    result22 = tardir(1, '/home/dsp/', ['documents/', 'downloads/'], 'example')
    print result22

    result23 = tarfiles(['/home/dsp/docs/help.txt', '/home/dsp/wave_out/abc.wav'], '/home/dsp/output/', 'test')
    print result23

    result24 = prepareserial(25)
    print result24

    result25 = telnet_login(tn, 'board1', 1)
    print result25
