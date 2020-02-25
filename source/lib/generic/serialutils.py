


########################################################################################################################
########################################################################################################################
## File              :: lib/generic/serialutils.py
## Description       :: VoIP Automation Common API : Serial port functions that does operations over a serial port.
## Developer         :: Sreekanth S
## Version           :: v1.0
## Release Date      :: 08/04/2019
## Changes made      :: Initial version.
## Changes made Date :: 11/04/2019
## Changes made by   :: Sreekanth S
########################################################################################################################
########################################################################################################################



import time
import glob
import serial

from globalutils import *



"""
SerialConnect functions would be used to connect to a DVF board using the serial interface and perform 
network-independent operations on them.
"""



class SerialConnect:
    def __init__(self, port, board_num, debug=0):
        self.serialport = port
        self.sercon = serial.Serial(self.serialport)
        if 'ttyMI' in self.serialport:
            self.serialnum = int(self.serialport.split('ttyMI')[1])
        elif 'ttySX' in self.serialport:
            self.serialnum = int(self.serialport.split('ttySX')[1])
        elif 'ttyS' in self.serialport:
            self.serialnum = int(self.serialport.split('ttyS')[1])
        elif 'ttyUSB' in self.serialport:
            self.serialnum = int(self.serialport.split('ttyUSB')[1])
        self.serialnum = 0
        self.board_num = board_num
        self.IPAddr = ""
        self.chipset = 0
        self.lpr_type = 0
        self.baudrate = 115200
        self.timeout = 1
        self.relay_bin = ""
        self.relayID = ""
        self.powerRelaynum = ""
        self.USBRelaynum = ""
        self.USBHubRelaynum = ""
        self.ethRelay_num = ""
        self.relay = 0
        self.chipset = 0
        self.boot_result = ""
        self.wifi = 0
        self.scriptpath = os.environ['PYTHONPATH'] + '/scr/login/'
        self.DEBUG = debug
#*----------------------------------------------------------------------------------------------------------------------

# Login to a DVF board on serial interface.

    def dvflogin(self):
        time.sleep(2)
        self.sercon.write("\n")
        self.sercon.write("root\n")
        self.sercon.write("\n")
        time.sleep(1)
#*----------------------------------------------------------------------------------------------------------------------

# Determine the DVF platform connected to a given serial port.

    def getPlatform(self):
        read_buffer = ""
        time.sleep(1)
        self.sercon.flushInput()
        self.sercon.flushOutput()
        for i in range(1,5):
            self.sercon.write("\n")
            read_buffer += self.sercon.read(500)
        if "@dvf99:~#" in read_buffer:
            self.chipset = 9919
        elif "@dvf9918:~#" in read_buffer:
            self.chipset = 9918
        elif "@dvf9928:~#" in read_buffer:
            self.chipset = 9928
        elif "@dvf101:~#" in read_buffer:
            self.chipset = 101
        elif "@dvf1100:~#" in read_buffer:
            self.chipset = 1100
        if self.DEBUG == 1:
            print "Detected Chipset = " + self.chipset + "\n"
        return self.chipset
#*----------------------------------------------------------------------------------------------------------------------

# Reboot a board using the serial interface.

    def rebootboard(self, relayconn):
        print 50 * "." + "\nBoard Number : " + str(self.board_num) + "\nSerial Port/Device : " + self.serialport + "\n" + 50 * "."
        print "\n"
        result = "NULL"
        ip_set = "none"
        self.relay = relayconn
        time.sleep(1)
        self.sercon.flushInput()
        self.sercon.flushOutput()
        self.sercon.write("\n")
        init_buffer = self.sercon.read(500)
        file = ""
        if self.DEBUG == 1:
            print 20*"#" + " Buffer contents on board " + str(self.board_num) + " START " + 20*"#"
            print init_buffer
            print 20*"#" + " Buffer contents on board " + str(self.board_num) + " END " + 20*"#"
        if "Exit" in init_buffer or "Menu" in init_buffer or "Call" in init_buffer:
            if self.DEBUG == 1:
                print "callManager running on " + str(self.board_num) + "....."
            self.sercon.write("q\n")
            time.sleep(6)
        elif "q: not found" in init_buffer:
            pass
        elif "Password:" in init_buffer:
            time.sleep(3)
            self.sercon.write("root\n")
            time.sleep(3)
            self.dvflogin()
            self.getPlatform()
        else:
            self.dvflogin()
            self.getPlatform()

        if self.relay and self.board_num == 1 :
            os.system("sudo " + self.relay_bin + " " + self.relayID + "_" + str(self.powerRelaynum) + "=0")
            time.sleep(0.5)
            os.system("sudo " + self.relay_bin + " " + self.relayID + "_" + str(self.powerRelaynum) + "=1")
            time.sleep(1)
            os.system("sudo " + self.relay_bin + " " + self.relayID + "_" + str(self.USBRelaynum) + "=0")
            time.sleep(0.5)
            os.system("sudo " + self.relay_bin + " " + self.relayID + "_" + str(self.USBRelaynum) + "=1")
            time.sleep(1)
            os.system("sudo " + self.relay_bin + " " + self.relayID + "_" + str(self.USBHubRelaynum) + "=0")
            time.sleep(0.5)
            os.system("sudo " + self.relay_bin + " " + self.relayID + "_" + str(self.USBHubRelaynum) + "=1")
            time.sleep(1)
            os.system("sudo " + self.relay_bin + " " + self.relayID + "_" + str(self.ethRelay_num) + "=0")
            time.sleep(0.5)
            os.system("sudo " + self.relay_bin + " " + self.relayID + "_" + str(self.ethRelay_num) + "=1")
            time.sleep(1)
        else:
            self.sercon.write("reboot\n")

        time.sleep(1)
        self.sercon.flushInput()
        self.sercon.flushOutput()
        self.sercon.write("\n")
        time.sleep(1)

        i = 0
        while True:
            if i > 1999:
                result = "NULL"
                break
            else:
                line = self.sercon.readline()
                print i, line
                if 'Sending select' in line:
                    self.boot_result = "Booted successfully...."
                    if self.DEBUG == 1:
                        print "IP grep line = ", line
                    ip = line.split()
                    if self.DEBUG == 1:
                        print ip
                    result = ip[3][:-3]
                    if self.DEBUG == 1:
                        print result
                    break
                # elif "dspg login:" in line or ("login" in line or self.board_num==1):
                elif "login:" in line:
                    self.boot_result = "Booted successfully...."
                    self.chipset = int((line.split(' login:')[0]).split('dvf')[1])
                    self.dvflogin()
                    lines = self.sercon.read(500)
                    time.sleep(3)
                    if ":~#" in line or "command not found" in lines:
                        print "Login Success...."
                    break
                elif "Password:" in line:
                    self.dvflogin()
                    time.sleep(3)
                    self.dvflogin()
                    lines = self.sercon.read(500)
                    time.sleep(3)
                    if ":~#" in line or "command not found" in lines:
                        print "Login Success...."
                    print lines
                    break
                elif "Overcurrent change detected" in line:
                    print "Overcurrent change detected....Can't boot/login...."
                    result = "NULL"
                    break
            i += 1

        if self.wifi and self.board_num == 1:
            print "Wifi is enabled... Need to connect to wifi network to get IP...."
            self.sercon.write("root\n")
            self.sercon.write("\n")
            print 20 * "@"
            print "Inside Wifi Enable"
            print 20 * "@"
            os.system("scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -r " + self.scriptpath + "configure/cfg_wlan root@" + result + "://home//root/\n")
            self.sercon.write("\n")
            time.sleep(2)
            self.sercon.write("chmod +x cfg_wlan\n")
            self.sercon.write("./cfg_wlan\n")
            time.sleep(10)
            line = self.sercon.read(10000)
            if self.DEBUG == 1:
                print "line=", line
            if "Firmware up: " in line:
                self.sercon.flushInput()
                self.sercon.flushOutput()
                self.sercon.write("udhcpc -i wlan0\n")
                self.sercon.write("\n")
                time.sleep(6)
                line = self.sercon.read(10000)
                if self.DEBUG == 1:
                    print "line=", line
                if "Sending select for " in line:
                    result = line.split('Sending select for ')[1].split("...")[0]
                    if self.DEBUG == 1:
                        print "result=", result
                    if "172." in result:
                        pass
                else:
                    print "IP failed from WLAN enabler...."
                    result = "NULL"
            else:
                print "Wifi activate script failed...."
                result = "NULL"

        # print "Result=", result
        if "172." not in result:
            result = "NULL"

        if "NULL" in str(result):
            print "IP not retrieved from boot, using \"ifconfig\"...."
            self.IPAddr = getipv4(1, self.sercon)
            time.sleep(2)
            ip_set = "ifconfig"
        elif "NULL" not in str(result):
            self.IPAddr = result
            ip_set = "boot"

        if 'ttyMI' in self.serialport:
            file = self.scriptpath + "login/pmpci"
        elif 'ttySX' in self.serialport:
            file = self.scriptpath + "login/pspci"
        if 'ttyS' in self.serialport:
            file = self.scriptpath + "login/pspc"
        elif 'ttyUSB' in self.serialport:
            file = self.scriptpath + "login/pusb"

        # string = "gnome-terminal -e 'bash -c \"kermit -l "+str(self.serialport)+" -b 115200 -c\"'"
        string = "gnome-terminal -e 'bash -c \"./" + str(file) + " " + str(self.serialnum) + "\"'"
        print "String = ", string

        try:
            print "Running script to activate telnet on Board" + str(self.board_num) + "...."
            p = subprocess.Popen(string, shell=True)
            time.sleep(1)
            p.terminate()
            print "Telnet activated on Board" + str(self.board_num) + "...."
        except Exception, exc:
            print "Couldn't activate telnet on Board" + str(self.board_num) + "...."
            time.sleep(3)

        if ip_set in ['ifconfig', 'boot']:
            print "IP retrieved successfully...."
        else:
            print "Board IP is null...."
            print "Please check the cable/connection...."

        self.serialClose()

        print "Exiting reboot procedure...."
        return self.chipset, self.IPAddr
#*----------------------------------------------------------------------------------------------------------------------

# Retrieve the IPv4 address of a DVF board through serial connection.

    def getipv4addr(self):
        self.sercon.write("ifconfig\n")
        time.sleep(0.5)
        read_buf = self.sercon.read(500)
        if self.DEBUG == 1:
            print read_buf
        ipv4str = read_buf.split('inet addr:')[1]
        ipv4board = ipv4str.split('  Bcast:')[0]
        return ipv4board
#*----------------------------------------------------------------------------------------------------------------------

# Close the serial connection to a DVF board.

    def serialClose(self):
        print "Closing the serial connection to  " + str(self.serialport) + "...."
        self.sercon.close()
#*----------------------------------------------------------------------------------------------------------------------



"""
listserialports function returns a list of the serial ports available on the system.
"""



def listserialports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result
#*----------------------------------------------------------------------------------------------------------------------



if __name__ == '__main__':
    print "Available/used Serial Ports : ", listserialports()
