


########################################################################################################################
########################################################################################################################
## File              :: lib/shunra/snwiemul.py
## Description       :: VoIP Automation Common API : Functions for executing the network emulation for Shunra, the
##                      network impairment device.
## Developer         :: Sreekanth S
## Version           :: v2.0
## Release Date      :: 11/04/2019
## Changes made      :: Initial version.
## Changes made Date :: 11/04/2019
## Changes made by   :: Sreekanth S
########################################################################################################################
########################################################################################################################



from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from lib.generic.globalutils import *



"""
These functions enable to run network impairment emulation on Shunra from a remote machine.
"""



# Press Submit button on the built emulation page.

def submit_cmd(cmd_html):
    l = os.getcwd().split('\\')
    cwd = ''
    for i in l:
        cwd = cwd + i + '/'
    source = 'file:///' + cwd + cmd_html
    driver = webdriver.Firefox()
    if '.html' in source:
        driver.get(source)
        time.sleep(3)
        driver.find_element_by_name("SUB_COM").click()
        time.sleep(2)
        # driver.find_element_by_xpath()
        driver.close()
    else:
        print "Wrong type of file...."
#*----------------------------------------------------------------------------------------------------------------------



# Click Stop Emulation button on Shunra's web control page.

def stop_emulation(toolipv4addr):
    url = "http://storm:storm@" + str(toolipv4addr) + "/emulation_control.shtml"
    driver = webdriver.Firefox()
    driver.get(url)
    driver.find_element_by_id("StopEmulation").click()
    time.sleep(2)
    driver.close()
#*----------------------------------------------------------------------------------------------------------------------



if __name__ == '__main__':
    print "Capturing...."
