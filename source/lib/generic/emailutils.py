


########################################################################################################################
########################################################################################################################
## File              :: lib/generic/emailutils.py
## Description       :: VoIP Automation Common API : Sends the report generated by the automation to a list of
##                      recipients.
## Developer         :: Sreekanth S
## Version           :: v1.2
## Release Date      :: 08/04/2019
## Changes made      :: Attachment format changed to .zip.
## Changes made Date :: 11/04/2019
## Changes made by   :: Sreekanth S
########################################################################################################################
########################################################################################################################



import smtplib
from email.encoders import encode_base64
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from mimetypes import guess_type
from email.mime.text import MIMEText
import os
import time

from globalutils import *



"""
Mailer functions sends email to a given set of recipients and attaches files to the mail if required.
"""



class Mailer:
    def __init__(self, debug=0):
        self.msg = MIMEMultipart()
        mailserverip = '172.20.110.222'
        self.msg['From'] = 'voip.automation@dspg.com'
        self.msg['Cc'] = "guruprasad.shanmukha@dspg.com, sreekanth.s@dspg.com, ramanathan.ramakrishnan@dspg.com"
        self.server = smtplib.SMTP(mailserverip, 25, local_hostname=None, timeout=90000)
        self.DEBUG = debug
#*----------------------------------------------------------------------------------------------------------------------

# Attach a file or a list of files to the mail.

    def attachfiles(self, attachment=[], message='DVF'):
        self.msg.attach(MIMEText(message, 'plain'))
        if self.DEBUG == 1:
            print "\n\n"+20*"#"
            print "Attachment(s) :\n", attachment
            print 20*"#"+"\n\n"
        for infile in attachment:
            try:
                mimetype, encoding = guess_type(infile)
                if self.DEBUG == 1:
                    print "mime type and encode=", mimetype, encoding
                mimetype = mimetype.split('/', 1)

                if (".html" in infile) or (".xlsx" in infile) or (".xls" in infile) or ("openxml" in infile):
                    print "Attaching file...."
                    att = open(infile, 'rb')
                    part = MIMEBase(mimetype[0], mimetype[1])
                    part.set_payload(att.read())
                    att.close()
                    encode_base64(part)
                    part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(infile))
                    self.msg.attach(part)
                else:
                    pass
            except:
                print "Unable to attach file....", infile
#*----------------------------------------------------------------------------------------------------------------------

# Send an email with (or without) attachments and a specific body, subject and recipients.

    def sendmail(self, to_list, message, totalcount, failcount, path):
        print "Send email called...."
        files = []
        mail_list = ""

        count = len(to_list) # Do something based on count.....To list one invalid entry going due to "."
        while count > 0:
            count -= 1
            mail_list += str(to_list[count])
            if count == 0:
                pass
            else:
                mail_list += ","

        if self.DEBUG == 1:
            print "List of recepients : ", mail_list
            print "To List (of recepients) : ", to_list

        r_dir = path
        sub = "DVF99/DVF101 Automation Result(s) : "
        for f in os.listdir(r_dir):
            if f.endswith(".html") or f.endswith(".xlsx"):
                files.append(f)
                subject = sub + f.split(".")[0] + " (run on the PC %s)" % gethostname()
                if self.DEBUG == 1:
                    print "Mail subject : ", subject
        if self.DEBUG == 1:
            print 20 * "#"
            print files
            print 20 * "#"

        self.msg['Subject'] = subject
        self.msg['To'] = mail_list

        line0 = "Hi,\n\n\nDVF Automation run has completed on the PC %s please find the attached Test Results \n " % get_hostname()
        if "crash" in str(totalcount):
            message = "Failed !!!! Please check the result...." + "\n" + message
        else:
            line1 = "\nSummary:\n"
            line2 = "\nTotal Tests (calls) = " + str(totalcount)
            line3 = "\nPassed = " + str(int(totalcount) - int(failcount))
            line4 = "\nFailed = " + str(failcount)
            line5 = "\n\n\nRegards,"
            line6 = "\nVoIP Automation Team"
            message = line0 + line1 + line2 + line3 + line4 + line5 + line6

        tar_name = tarfiles(files)
        self.attachfiles(tar_name, message)

        print "\nSending e-mail....\n"

        res = self.server.sendmail(self.msg['From'], self.msg['To'].split(",") + self.msg['Cc'].split(","), self.msg.as_string())
        time.sleep(5)

        print "\nEmail sent....\n"
        self.server.quit()
#*----------------------------------------------------------------------------------------------------------------------



if __name__ == '__main__':
    print "Capturing...."