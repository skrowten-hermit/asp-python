


########################################################################################################################
########################################################################################################################
## File              :: vaca_image_build.py
## Description       :: VoIP Automation Common API : Functions for image build.
## Developer         :: Sreekanth S
## Version           :: v2.0
## Release Date      :: 11/04/2019
## Changes made      :: Initial version.
## Changes made Date :: 11/04/2019
## Changes made by   :: Sreekanth S
########################################################################################################################
########################################################################################################################



import os
import time



class ImageBuild:
    def __init__(self, debug=0):
        print "Deleting old build ststistics...."
        string="plink guru@172.28.3.150 -pw 123456 rm -rf  /home/guru/DVF99_Automation/final_result.txt"
        print string
        os.system(string)
        string="del /F C:\\automation\DVF99_Automation\Output\\final_result.txt"
        print string
        os.system(string)
        self.DEBUG = debug

    def binary_build(self, split, nda, opus, tag, css, tool, uboot, bootastic, kernel):
        count=0
        string="plink guru@172.28.3.150 -pw 123456 /home/guru/DVF99_Automation//auto_150.sh "+str(split)+" "+str(nda)+" "+str(opus)+" "\
                +str(tag)+" "+str(css)+" "+str(tool)+" "+str(uboot)+" "+str(bootastic)+" "+str(kernel)
        print string
        os.system(string)
        string="C:\\automation\DVF99_Automation\Output\\final_result.txt"
        print string

        copy="pscp -pw 123456 guru@172.28.3.150:/home/guru/DVF99_Automation/final_result.txt C:\\automation\DVF99_Automation\Output\\"
        print copy        
        while (not (os.path.isfile(string))):
            try:
                os.system(copy)
            except:
                pass
            count+=1
            time.sleep(1)
            print "Build in progress....."
            if count==10:
                result="fail"
                break            
        if 'css build error' in open(string).read():
            print "css build error"
            print open(string).read()
            result="fail"
            copy="pscp -pw 123456 guru@172.28.3.150:/home/guru/DVF99-CSS-Git/delivery/build/error_log.txt C:\\automation\DVF99_Automation\Output\\"
            
        elif 'uboot build error' in open(string).read():
            print "uboot build error"
            print open(string).read()
            result="fail"
            copy="pscp -pw 123456 guru@172.28.3.150:/home/guru/u-boot/error_log.txt C:\\automation\DVF99_Automation\Output\\"

        elif 'bootastic build error' in open(string).read():
            print "uboot build error"
            print open(string).read()
            result="fail"
            copy="pscp -pw 123456 guru@172.28.3.150:/home/guru/bootastic/error_log.txt C:\\automation\DVF99_Automation\Output\\"
            
        elif 'kernel build error' in open(string).read():
            print "uboot build error"
            print open(string).read()
            result="fail"            
            copy="pscp -pw 123456 guru@172.28.3.150:/home/guru/linux/error_log.txt C:\\automation\DVF99_Automation\Output\\"
            
        elif 'tools build error' in open(string).read():
            print "uboot build error"
            print open(string).read()
            result="fail"            
            copy="pscp -pw 123456 guru@172.28.3.150:/home/guru/tools/error_log.txt C:\\automation\DVF99_Automation\Output\\"

        else:
            copy="ls -l"
            print "Build completed....."
            result="pass"
            
        os.system(copy)        
        return result



##split_voip=1
##nda_codec=1
##opus_enable=0
##tag_flag=0
##css_tag_id="CSS_DVF99_1.3.4_rc4"
##tools_tag_id="dvf-v1.3.4-rc4"
##uboot_tag_id="dvf-v1.3.4-rc4"
##bootastic_tag_id="dvf-v1.3.4-rc4"
##kernel_tag_id="dvf-v1.3.4-rc4"
##
##suji=git_build()
##suji.binary_build(split_voip, nda_codec, opus_enable, tag_flag, css_tag_id, tools_tag_id, uboot_tag_id, bootastic_tag_id, kernel_tag_id)


