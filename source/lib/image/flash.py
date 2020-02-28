


########################################################################################################################
########################################################################################################################
## File              :: vaca_image_flash.py
## Description       :: VoIP Automation Common API : Functions for flashing the DVF EVBs with images from a TFTP server.
## Developer         :: Sreekanth S
## Version           :: v2.0
## Release Date      :: 11/04/2019
## Changes made      :: Initial version.
## Changes made Date :: 11/04/2019
## Changes made by   :: Sreekanth S
########################################################################################################################
########################################################################################################################



import subprocess
import time
import os
##import serial.tools.list_ports
import serial
import sys
import vaca_serial_routines



class ImageBurn:
    def __init__(self, tftp_server, debug=0):
        self.com_ports=[]
##        com_list=list(serial.tools.list_ports.comports())
##        print com_list
##        for n in com_list:
##            j=n[1].split()
##            if 'MOXA' in j:
##                com=j[4]
##                com=int(com)
##            else:
##                com=0
##            self.com_ports.append(com)
##

        try:  # self.telnet
            os.system("sudo fuser -v -k /dev/ttyUSB* \n")
            time.sleep(2)
        except:
            pass

        #
        # self.com_ports=com_return.serial_ports()
        # print self.com_ports

        dot_count=0
        board_ip=[]
        gate_ip=[]
        self.tftp_server_ip=tftp_server
        i=0
        for n in self.tftp_server_ip:
            board_ip.append(n)
            gate_ip.append(n)
            if n=='.':
                dot_count+=1
            if dot_count==3:
              board_ip.append("209")
              gate_ip.append("254")
              break
        print "Comp:", self.com_ports
        self.final_board_ip=str(''.join(board_ip))
        self.gatway_ip=str(''.join(gate_ip))
        print "Board   ip   =", self.final_board_ip
        print "Gateway ip   =", self.gatway_ip
        print "Com ports    =", self.com_ports
        self.DEBUG = debug


    def image_copy(self):
        print 20*"#"
        print "Copiying Images from Nightly....."
        print 20 * "#"
        cmd="sudo cp -rf /var/lib/jenkins/workspace/Images/* //var/lib/tftpboot/DVF1100/"
        os.system(cmd+"\n")
        time.sleep(5)
        cmd = "sync"
        os.system(cmd+"\n")
        time.sleep(2)
        print "Images copied..."

    def flash_call(self, image_name):
        i, j, k = 0, 0, 0
        if "devtree" in image_name:
            ln = "tftp DVF1100/dvf1100-bidir-TDM-audio-adaptor.dtb \n"
        elif "kernel" in image_name:
            ln = "tftp DVF1100/uImage \n"
        else:
            ln = 'tftp DVF1100/'+image_name+'\n'
        self.sb.write(ln)

        if "ubifs" in image_name:
            while i < 500:
                line=self.sb.readline()
                print "i=", i, line
                if "Bytes transferred" in line:
                    print image_name+" load success..."
                    time.sleep(2)
                    ln = "run dfu_manifest_system \n"
                    self.sb.write(ln)
                    while j < 100:
                        line=self.sb.readline()
                        print "J=",j,line
                        if "Hit Esc key to stop autoboot:" in line:
                            time.sleep(2)
                            print "Image load success...."
                            return "pass"
                        else:
                            j+=1
                            time.sleep(1)
                            if j==100:
                                print image_name+" flash failed"
                                return "fail"
                else:
                    i+=1
                    time.sleep(1)
                    if i==500:
                        print image_name+" tftp failed"
                        return "fail"

        else:
            while i< 100:
                line=self.sb.readline()
                print "i=",i,line
                if "Bytes transferred" in line:
                    print image_name+" load success..."
                    time.sleep(2)
                    ln = 'nand erase.part ' + image_name + '\n'
                    self.sb.write(ln)

                    while j < 100:
                        line=self.sb.readline()
                        print "J=",j,line
                        if "OK" in line:
                            time.sleep(2)
                            ln="nand write 0x40000000 "+image_name+"\n"
                            self.sb.write(ln)

                            while k < 100:
                                line = self.sb.readline()
                                print "k=", k, line
                                if "written: OK" in line:
                                    time.sleep(2)
                                    print "Board load success....."
                                    return "pass"
                                else:
                                    k+=1
                                    time.sleep(1)
                                    if k==100:
                                        print image_name+" flashing failed"
                                        return "fail"
                        else:
                            j+=1
                            time.sleep(1)
                            if j==100:
                                print image_name+" erase failed"
                                return "fail"
                else:
                    i+=1
                    time.sleep(1)
                    if i==100:
                        print image_name+" tftp failed"
                        return "fail"



    def load_image_board(self, board_id):
        print "Board Com port is %s....." %(board_id)
        self.sb=serial.Serial(board_id)
        self.sb.baudrate = 115200
        self.sb.timeout=1
        self.sb.flushInput()
        self.sb.flushOutput()
        self.sb.write("\n")
        self.sb.write("root\n")
        time.sleep(1)
        self.sb.write("\n")
        self.sb.write("root\n")

        self.sb.write("reset\n")
        self.sb.write("reboot\n")

        for i in range(2000):
            line=self.sb.readline()
            print "autoboot:", i,line
            if ("stop autoboot:" in line) or ("stmac-1" in line):
                print "Found autoboot...."
                char="\x1b"
                self.sb.write(char)
                print self.sb.readline()
                i=2001
                break


        for i in range(10):
            self.sb.write("\r\n")
            line=self.sb.readline()
            print "Hash prompt:",i, line
            if ("DVF99 #" in line) or ("EVB1100" in line):
                print "Board is stopped at bootloader for loading the image"
                i=11
                break
            else:
                if i==9:
                    print "Autoboot fail"
                    self.sb.close()
                    return "fail"
            i+=1


        self.sb.write('setenv ipaddr '+str(self.final_board_ip)+'\r\n')
        self.sb.write('\n')
        time.sleep(1)
        self.sb.write('setenv serverip '+str(self.tftp_server_ip)+'\r\n')
        self.sb.write('\n')
        time.sleep(1)
        self.sb.write('setenv gatewayip '+str(self.gatway_ip)+'\r\n')
        self.sb.write('\n')
        time.sleep(1)
        self.sb.write('setenv loadaddr 0x40000000 \r\n')
        self.sb.write('\n')
        time.sleep(1)
        self.sb.write('saveenv \r\n')
        self.sb.write('\n')
        time.sleep(1)
        res=self.flash_call("kernel")
        if "pass" in res:
            res = self.flash_call("devtree")
            if "pass" in res:
                res = self.flash_call("dspg-mm-qt5-image-dspg.ubifs")

        self.sb.close()
        return res


    def oop_image_load_board(self, com_num, ser_ip, m5t):
        print "board_no.....................=",com_num
        result="pass"
        base_comp=self.com_ports[com_num]

        sb=serial.Serial(base_comp)
        sb.baudrate = 115200
        sb.timeout=3
        sb.flushInput()
        sb.flushOutput()

        sb.write("\n")
        sb.write("root\n")
        sb.write("\n")
        time.sleep(1)

        sb.write("root")
        sb.write("\n")
        time.sleep(1)


        cmd="mv /lib/firmware/css-loader /lib/firmware/css-loader-orig \n"
        print cmd
        sb.write(cmd)
        sb.write("\n")
        time.sleep(2)

        cmd="mv /usr/bin/app_dsp /usr/bin/app_dsp_orig \n"
        print cmd
        sb.write(cmd)
        sb.write("\n")
        time.sleep(2)

        cmd="mv /usr/bin/callManager /usr/bin/callManager_orig \n"
        print cmd
        sb.write(cmd)
        sb.write("\n")
        time.sleep(2)

        cmd="mv /boot/uImage /boot/uImage_orig \n"
        print cmd
        sb.write(cmd)
        sb.write("\n")
        time.sleep(2)


        cmd="mv /boot/dvf99-evb.dtb /boot/dvf99-evb.dtb_orig \n"
        print cmd
        sb.write(cmd)
        sb.write("\n")
        time.sleep(2)
        ##################################################################

        if "172.28.3.150" in ser_ip:
            cmd="tftp -gr guru/DVF99_Automation/css-loader 172.28.3.150 \n"
        else:
            cmd="tftp -gr css-loader "+str(ser_ip)+" \n"
        print cmd
        sb.write(cmd)
        time.sleep(10)

        if "172.28.3.150" in ser_ip:
            cmd="tftp -gr guru/DVF99_Automation/app_dsp 172.28.3.150 \n"
        else:
            cmd="tftp -gr app_dsp "+str(ser_ip)+" \n"

        print cmd
        sb.write(cmd)
        time.sleep(10)


        if "172.28.3.150" in ser_ip:
            cmd="tftp -gr guru/DVF99_Automation/callManager 172.28.3.150 \n"
        else:
            cmd="tftp -gr callManager "+str(ser_ip)+" \n"

        print cmd
        sb.write(cmd)
        time.sleep(10)



        if "172.28.3.150" in ser_ip:
            cmd="tftp -gr guru/DVF99_Automation/uImage 172.28.3.150 \n"
        else:
            cmd="tftp -gr uImage "+str(ser_ip)+" \n"
        print cmd
        sb.write(cmd)
        time.sleep(10)


        if "172.28.3.150" in ser_ip:
            cmd="tftp -gr guru/DVF99_Automation/dvf99-evb.dtb 172.28.3.150 \n"
        else:
            cmd="tftp -gr dvf99-evb.dtb "+str(ser_ip)+" \n"

        print cmd
        sb.write(cmd)
        time.sleep(10)

        ################################################################

        if not "fail" in result:
            sb.write("\n")
            cmd="mv css-loader /lib/firmware/ \n"
            print cmd
            sb.write(cmd)
            sb.write("\n")
            time.sleep(2)

            cmd="mv app_dsp /usr/bin/ \n"
            print cmd
            sb.write(cmd)
            sb.write("\n")
            time.sleep(2)

            cmd="mv callManager /usr/bin/ \n"
            print cmd
            sb.write(cmd)
            sb.write("\n")
            time.sleep(2)

            cmd="mv uImage /boot/ \n"
            print cmd
            sb.write(cmd)
            sb.write("\n")
            time.sleep(2)

            cmd="mv dvf99-evb.dtb /boot/ \n"
            print cmd
            sb.write(cmd)
            sb.write("\n")
            time.sleep(2)

            cmd="chmod +x /usr/bin/* \n"
            sb.write(cmd)
            sb.write("sync \n")
            time.sleep(2)

            cmd="chmod +x /boot/* \n"
            sb.write(cmd)
            sb.write("sync \n")
            time.sleep(2)

            cmd="chmod +x /lib/firmware/* \n"
            sb.write(cmd)
            sb.write("sync \n")
            time.sleep(2)
            
##            if int(m5t):
##                cmd="cd /usr/lib/ \n"
##                print cmd
##                sb.write(cmd)
##                sb.write("\n")
##                time.sleep(2)
##
##                cmd="tftp -gr libexpat.so.1.5.2 \n"
##                print cmd
##                sb.write(cmd)
##                sb.write("\n")
##                time.sleep(2)
##
##                cmd="ln -s libexpat.so.1.5.2 libexpat.so \n"
##                sb.write(cmd)
##                sb.write("sync \n")
##                time.sleep(2)
##
##                cmd="ln -s libexpat.so.1.5.2 libexpat.so.1 \n"
##                sb.write(cmd)
##                sb.write("sync \n")
##                time.sleep(2)
##                

        sb.write("q \n")
        sb.write("q \n")
        sb.write("\n")
        sb.write("\n")
        sb.write("reboot \n")
        sb.write("\n")

        time.sleep(1)
        sb.close()
        return result


    def burn(self, com_num):
        print "board_no.....................=",com_num
        result="NULL"
        sb=serial.Serial(com_num)
        sb.baudrate = 115200
        sb.timeout=1
        sb.flushInput()
        sb.flushOutput()
        time.sleep(1)

        sb.write("q\n")

        sb.write("q\n")

        time.sleep(2)
        sb.write("3\n")
        sb.write("3\n")
        time.sleep(3)
        sb.write("root\n")

        time.sleep(1)
        sb.write("root\n")

        sb.write("reset\n")
        time.sleep(1)
        sb.write("reboot\n")
        time.sleep(1)
        sb.write("\n")
        time.sleep(1)

        for i in range(2000):
            line = sb.readline()
            print i, line
            if 'Sending select' in line:
                print "IP grep line = ",line
                ip=line.split()
                print ip
                result=ip[3][:-3]
                print result
                break
            elif "dspg login:" in line:
                print "DVF1100 Board - Use ifconfig"
                sb.write("root\n")
                line=sb.read(500)
                while "dbmd2.service" not in line:
                    print "line=", line
                    if "login:" in line:
                        sb.write("root\n")
                        line = sb.read(500)
                    elif "Password:" in line:
                        sb.write("\n")
                        time.sleep(4)
                        sb.write("root\n")
                        line = sb.read(500)
                    elif ":~#" in line or "command not found" in line:
                        print "Login Success..."
                        line="dbmd2.service"
                    else:
                        sb.write("reboot\n")
                        line = sb.readline()
                    print line

                sb.flushInput()
                sb.flushOutput()
                time.sleep(10)
                sb.write("\n")
                sb.write("\n")
                sb.write("\n")
                sb.write("ifconfig\n")
                time.sleep(0.5)
                read_buf = sb.read(3000)
                print "read_buf=", read_buf
                result = read_buf.split('inet addr:')[1].split('  Bcast:')[0]
                if "172" in result:
                    pass
                else:
                    sb.flushInput()
                    sb.flushOutput()
                    time.sleep(5)
                    sb.write("\n")
                    sb.write("\n")
                    sb.write("\n")
                    sb.write("ifconfig\n")
                    time.sleep(0.5)
                    read_buf = sb.read(3000)
                    print "read_buf=", read_buf
                    result = read_buf.split('inet addr:')[1].split('  Bcast:')[0]
                print result
                break
            elif i==4999:
                result="NULL"
                break

        print "Closing serial port..."
        sb.close()


        # if "NULL" not in str(result):
        #     num=base_comp.split("M")[1]
        #     print "num=",num
        #     string = "ttermpro.exe /C="+str(int(num))+" /BAUD=115200 /M=C://automation/DVF99_Automation/scripts/sunBurn.TTL; exit 0"
        #     print "String = ",string
        #     try:
        #         p=subprocess.Popen(string, shell=True)
        #         time.sleep(1)
        #         p.terminate()
        #         return result
        #     except Exception, exc:
        #         return "NULL"
        #     time.sleep(3)
        #
        # else:
        #     print "Board ip is null... please check cable connections"

        return result





#
#
# board_number="/dev/ttyUSB0"
# tftp="172.28.3.17"
# s=image_burn(tftp)
# s.image_copy()
# s.load_image_board(board_number)
# s.burn(board_number)



