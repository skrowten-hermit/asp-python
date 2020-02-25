


########################################################################################################################
########################################################################################################################
## File              :: lib/generic/isicutils.py
## Description       :: VoIP Automation Common API : Functions for IP Stack Integrity Checker tool.
## Developer         :: Sreekanth S
## Version           :: v1.0
## Release Date      :: 11/04/2019
## Changes made      :: Initial version.
## Changes made Date :: 11/04/2019
## Changes made by   :: Sreekanth S
########################################################################################################################
########################################################################################################################



from lib.generic.globalutils import *



"""
The following functions uses IP Stack Integrity Checker (ISIC) to run on-board integrity tests on the IP Stack.
"""



class ISIC:
    def __init__(self):
        self.target_ip = ""
        self.path = ""
#*----------------------------------------------------------------------------------------------------------------------


    def tcpv4_checker(self):
        print "Test TCP (over IPv6) integrity...."
#*----------------------------------------------------------------------------------------------------------------------


    def udpv4_checker(self):
        print "Test UDP (over IPv4) integrity...."
#*----------------------------------------------------------------------------------------------------------------------


    def ethernetv4_checker(self):
        print "Test Ethernet (over IPv4) Integrity...."
#*----------------------------------------------------------------------------------------------------------------------


    def icmpv4_checker(self):
        print "Test ICMP (over IPv4) Integrity...."
#*----------------------------------------------------------------------------------------------------------------------


    def tcpv6_checker(self):
        print "Test TCP (over IPv6) integrity...."
#*----------------------------------------------------------------------------------------------------------------------


    def udpv6_checker(self):
        print "Test UDP (over IPv6) integrity...."
#*----------------------------------------------------------------------------------------------------------------------


    def ethernetv6_checker(self):
        print "Test Ethernet (over IPv6) Integrity...."
#*----------------------------------------------------------------------------------------------------------------------


    def icmpv6_checker(self):
        print "Test ICMP (over IPv6) Integrity...."
#*----------------------------------------------------------------------------------------------------------------------



if __name__ == '__main__':
    print "Capturing...."
