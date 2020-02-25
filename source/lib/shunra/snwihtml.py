


########################################################################################################################
########################################################################################################################
## File              :: vaca_snwi_htmlroutines.py
## Description       :: VoIP Automation Common API : Functions for building emulation HTML file for Shunra, the network
##                      impairment device.
## Developer         :: Sreekanth S
## Version           :: v2.0
## Release Date      :: 11/04/2019
## Changes made      :: Initial version.
## Changes made Date :: 11/04/2019
## Changes made by   :: Sreekanth S
########################################################################################################################
########################################################################################################################



from lib.generic.globalutils import *



"""
BuildEmulHTML is a class with functions to create a HTML file with emulation parameters for Shunra to run from a remote
machine.
"""



class BuildEmulHTML:
    def __init__(self, ipS, pagename, debug=0):
        try:
            os.remove(pagename)
        except OSError:
            print "File already removed!"

        self.reorder = 0
        self.DEBUG = debug

        self.hostname = gethostname()
        self.username = getusername()

        self.htmlfile = open(pagename, "w+")
        self.htmlfile.write("<HTML>\n")
        self.htmlfile.write("<HEAD>\n")
        self.htmlfile.write("<TITLE>Shunra Software Ltd.</TITLE>\n")
        self.htmlfile.write("<BODY>\n")
        self.htmlfile.write("<FORM ACTION=\"http://" + str(ipS) + "/cgi-bin/http_control.cgi\" METHOD=\"POST\">\n")
        self.htmlfile.write("<TEXTAREA NAME=\"XML_COM\" COLS='160' ROWS='40' WRAP='none'>\n")
        self.htmlfile.write("<?xml version='1.0'?>\n\n")

        self.htmlfile.write("<!DOCTYPE STORM_MSG SYSTEM 'StormProtocol_1_9.dtd'>\n")
        self.htmlfile.write("<STORM_MSG STORM_PROTOCOL_VERSION='1.9' CLIENT_HOST='Visio'>\n")
        self.htmlfile.write("<STORM_COMMAND CLIENT_NAME='NetworX' COMMAND_TIMESTAMP='111'>\n")
#*----------------------------------------------------------------------------------------------------------------------

# Write PLAY initialization parameters to Shunra emulation HTML file.

    def playemulinit(self):
        self.htmlfile.write("<STORM_CMD_PLAY>\n\n")

        self.htmlfile.write("<NETWOR_X ID=\"NetworX_Document\" NAME=\"DrawingMOS\" ORIGIN=\"" + self.hostname + "\" "
                            "USER_ID=\"" + self.hostname + "\" USER_DATA=\"DrawingMOS\" CREATED_BY=\"" + self.username +
                            "\" DESCRIPTION=\"NetworX_Document\" CREATED_ON_DATE=\"2018-03-19 17:22:07\" "
                            "NETWOR_X_VERSION=\"1.9\" CREATED_ON_HOST_NAME=\"" + self.hostname + "\">\n")
        self.htmlfile.write("<NET_OBJECTS>\n")
        self.htmlfile.write("<PORT ID=\"STORM_Port_117_1521459788\" NAME=\"Port A4\" CARD_POSITION=\"A\" "
                            "PORT_POSITION=\"4\"/>\n")
        self.htmlfile.write("<PORT ID=\"STORM_Port_116_1521459773\" NAME=\"Port A3\" CARD_POSITION=\"A\" "
                            "PORT_POSITION=\"3\"/>\n")
        self.htmlfile.write("<WAN_CLOUD ID=\"STORM_WAN_Cloud_118_1521459804\" NAME=\"WAN Cloud 1\" "
                            "DESCRIPTION=\"na\">\n")
#*----------------------------------------------------------------------------------------------------------------------

# Write PLAY closing parameters to Shunra emulation HTML file.

    def playemulclose(self):
        self.htmlfile.write("</WAN_CLOUD>\n")
        self.htmlfile.write("</NET_OBJECTS>\n")
        self.htmlfile.write("<LINKS>\n")
        self.htmlfile.write("<LINK LINK_ID=\"STORM_Link_119_1521459807\" TO_OBJECT=\"STORM_WAN_Cloud_118_1521459804\" "
                            "FROM_OBJECT=\"STORM_Port_116_1521459773\" UNIDIRECTIONAL=\"false\"/>\n")
        self.htmlfile.write("<LINK LINK_ID=\"STORM_Link_120_1521459819\" TO_OBJECT=\"STORM_Port_117_1521459788\" "
                            "FROM_OBJECT=\"STORM_WAN_Cloud_118_1521459804\" UNIDIRECTIONAL=\"false\"/>\n")
        self.htmlfile.write("</LINKS>\n")
        self.htmlfile.write("</NETWOR_X>\n")
        self.htmlfile.write("</STORM_CMD_PLAY>\n")
#*----------------------------------------------------------------------------------------------------------------------

# Write LATENCY parameters to Shunra emulation HTML file.

    def playemullatency(self, latencytype, latencydict):
        if latencytype == 'Fixed':
            print "Setting Fixed latency parameters...."
            self.htmlfile.write("<FIXED_LATENCY LATENCY=\"" + str(latencydict['delay']) + "\"/>\n")
        elif latencytype == 'Uniform_Distributed':
            print "Setting Uniform Distributed latency parameters...."
            if self.reorder == 1:
                self.htmlfile.write("<UNIFORM_LATENCY MAX=\"" + str(latencydict['delay_max']) + "\" MIN=\"" +
                                    str(latencydict['delay_min']) + "\" LIMIT_CHANGE=\"no\" ENABLE_REORDER=\"yes\" "
                                                                    "LIMIT_CHANGE_VALUE=\"0\"/>\n")
            else:
                self.htmlfile.write("<UNIFORM_LATENCY MAX=\"" + str(latencydict['delay_max']) + "\" MIN=\"" +
                                    str(latencydict['delay_min']) + "\" LIMIT_CHANGE=\"no\" ENABLE_REORDER=\"no\" "
                                                                    "LIMIT_CHANGE_VALUE=\"0\"/>\n")
        elif latencytype == 'Normal_Distributed':
            print "Setting Normal Distributed latency parameters...."
            if self.reorder == 1:
                self.htmlfile.write("<NORMAL_LATENCY AVERAGE=\"" + str(latencydict['delay_avg']) + "\" STD_DEVIATION=\""
                                    + str(latencydict['delay_sd']) + "\" ENABLE_REORDER=\"yes\"/>\n")
            else:
                self.htmlfile.write("<NORMAL_LATENCY AVERAGE=\"" + str(latencydict['delay_avg']) + "\" STD_DEVIATION=\""
                                    + str(latencydict['delay_sd']) + "\" ENABLE_REORDER=\"no\"/>\n")
        elif latencytype == 'Linear':
            print "Setting Linear latency parameters...."
            if self.reorder == 1:
                self.htmlfile.write("<LINEAR_LATENCY MAX=\"" + str(latencydict['delay_max']) + "\" MIN=\"" +
                                    str(latencydict['delay_min'])+"\" DURATION=\"" + str(latencydict['graph_duration'])
                                    + "\" ENABLE_REORDER=\"yes\"/>\n")
            else:
                self.htmlfile.write("<LINEAR_LATENCY MAX=\"" + str(latencydict['delay_max']) + "\" MIN=\"" +
                                    str(latencydict['delay_min'])+"\" DURATION=\"" + str(latencydict['graph_duration'])
                                    + "\" ENABLE_REORDER=\"no\"/>\n")
#*----------------------------------------------------------------------------------------------------------------------

# Write PACKET LOSS parameters to Shunra emulation HTML file.

    def playemulpktloss(self, pktlosstype, pktlossdict):
        if pktlosstype == 'Periodic':
            print "Setting Periodic loss parameters...."
            self.htmlfile.write("<PERIODIC_LOSS PACKET_COUNT=\"" + str(pktlossdict['frequency']) + "\"/>\n")
        elif pktlosstype == 'Random':
            print "Setting Random loss parameters...."
            self.htmlfile.write("<RANDOM_LOSS CHANCE=\"" + str(pktlossdict['probability']) + "\"/>\n")
        elif pktlosstype == 'Burst':
            print "Setting Burst loss parameters...."
            self.htmlfile.write("<BURST_LOSS BURST_CHANCE=\"" + str(pktlossdict['burst_probability']) +
                                "\" MAX_PACKET_LOSS=\"" + str(pktlossdict['burst_max_size']) + "\" MIN_PACKET_LOSS=\""
                                + str(pktlossdict['burst_min_size']) + "\"/>\n")
        elif pktlosstype == 'Gilbert-Elliot':
            print "Setting Gilbert-Elliot loss parameters...."
            self.htmlfile.write("<GILBERT_ELLIOT_LOSS>\n")
            self.htmlfile.write("<GOOD_STATE_LOSS CHANGE_TO_BAD_CHANCE=\"" + str(pktlossdict['good_state_change'])
                                + "\">\n")
            self.htmlfile.write("<RANDOM_LOSS CHANCE=\"" + str(pktlossdict['good_state_loss']) + "\"/>\n")
            self.htmlfile.write("</GOOD_STATE_LOSS>\n")
            self.htmlfile.write("<BAD_STATE_LOSS CHANGE_TO_GOOD_CHANCE=\"" + str(pktlossdict['bad_state_change'])
                                + "\">\n")
            self.htmlfile.write("<RANDOM_LOSS CHANCE=\"" + str(pktlossdict['bad_state_loss']) + "\"/>\n")
            self.htmlfile.write("</BAD_STATE_LOSS>\n")
            self.htmlfile.write("</GILBERT_ELLIOT_LOSS>\n")
#*----------------------------------------------------------------------------------------------------------------------

# Write PACKET EFFECTS parameters to Shunra emulation HTML file.

    def playemulpkteffect(self, pktefftype, pkteffdict):
        if pktefftype == 'Out_of_Order':
            print "Setting Out-of-Order parameters...."
            self.htmlfile.write("<OUT_OF_ORDER CHANCE=\"" + str(pkteffdict['ooo_probability']) + "\" MAX_OFFSET=\"" +
                                str(pkteffdict['ooo_max_offset']) + "\" MIN_OFFSET=\"" +
                                str(pkteffdict['ooo_min_offset']) + "\"/>\n")
        elif pktefftype == 'Duplicate_Packets':
            print "Setting Duplicate packets parameters...."
            self.htmlfile.write("<DUPLICATE_PACKETS CHANCE=\"" + str(pkteffdict['dup_probability']) +
                                "\" MAX_DUPLICATION=\"" + str(pkteffdict['dup_maximum']) + "\" MIN_DUPLICATION=\"" +
                                str(pkteffdict['dup_minimum']) + "\"/>\n")
#*----------------------------------------------------------------------------------------------------------------------

# Write STOP EMULATION parameters to Shunra emulation HTML file.

    def stopemul(self):
        self.htmlfile.write("<STORM_CMD_STOP>\n")
        self.htmlfile.write("</STORM_CMD_STOP>\n")
#*----------------------------------------------------------------------------------------------------------------------

# Write closing tags to Shunra emulation HTML file.

    def htmlclose(self):
        self.htmlfile.write("</STORM_COMMAND>\n")
        self.htmlfile.write("</STORM_MSG>\n")
        self.htmlfile.write("</TEXTAREA>\n")
        self.htmlfile.write("<INPUT TYPE=\"SUBMIT\" NAME = \"SUB_COM\" VALUE=\"Send Command\">\n")
        self.htmlfile.write("</FORM>\n")
        self.htmlfile.write("</BODY>\n")
        self.htmlfile.write("</HTML>\n")
        self.htmlfile.close()
#*----------------------------------------------------------------------------------------------------------------------



if __name__ == '__main__':
    print "Capturing...."
