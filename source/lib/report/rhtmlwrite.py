


########################################################################################################################
########################################################################################################################
## File              :: vaca_rhtml_write_routines.py
## Description       :: VoIP Automation Common API : HTML report test-case result data population.
## Developer         :: Sreekanth S
## Version           :: v2.0
## Release Date      :: 11/04/2019
## Changes made      :: Embedded relative paths for HTML hyperlinks, added CMBS test cases.
## Changes made Date :: 11/04/2019
## Changes made by   :: Sreekanth S
########################################################################################################################
########################################################################################################################



import htmldef as HTML
import time



class HTMLReport:
    def __init__(self, debug=0):
        self.path = ""
        self.version_number = ""
        self.chipset = ""
        self.suite_user_info = ""
        self.DEBUG = debug


    def image(self, text, url):
        return "<a href='%s'> <center>%s</center><img src='%s' height='30' width='50'></a>" % (url, text, url)


    def page(self, text, url):
        return "<a href='%s'> <center>%s</center></a>" % (url, text)


    def graph_html(self, test, url):
        # The hyperlinked target page showing all the directions (for HOLD_RESUME, CONF cases) - images contained in a tabular format,
        # a max of 2 centered images per row (with exactly 2 columns
        HTMLFILE = url + "graphs.html"
        f = open(HTMLFILE, 'a')
        table_data = [
                        ['b1_b2.png','b2_b1.png'],
                        ["<img src='%s' height='420' width='560'>" % (url + "RESULT_b1_b2.png"), "<img src='%s' height='420' width='560'>" % (url + "RESULT_b2_b1.png")]
                     ]
        htmlcode = HTML.table(table_data, col_width=['50%', '50%'], col_align=['center', 'center'], col_styles=['', ''])
        f.write(htmlcode)

        if test == 2:
            table_data = [
                            ['b1_b2_hold.png','b2_b1_hold.png'],
                            ["<img src='%s' height='420' width='560'>" % (url + "RESULT_b1_b2_hold.png"), "<img src='%s' height='420' width='560'>" % (url + "RESULT_b2_b1_hold.png")],
                            ['b1_b2_res.png','b2_b1_res.png'],
                            ["<img src='%s' height='420' width='560'>" % (url + "RESULT_b1_b2_res.png"), "<img src='%s' height='420' width='560'>" % (url + "RESULT_b2_b1_res.png")]
                         ]
            htmlcode = HTML.table(table_data, col_width=['50%', '50%'], col_align=['center', 'center'], col_styles=['', ''])
            f.write(htmlcode)
        elif test >= 3:
            table_data = [
                            ['b2_b3.png','b3_b2.png'],
                            ["<img src='%s' height='420' width='560'>" % (url + "RESULT_b2_b3.png"), "<img src='%s' height='420' width='560'>" % (url + "RESULT_b3_b2.png")],
                            ['b1_b3.png','b3_b1.png'],
                            ["<img src='%s' height='420' width='560'>" % (url + "RESULT_b1_b3.png"), "<img src='%s' height='420' width='560'>" % (url + "RESULT_b3_b1.png")]
                         ]
            htmlcode = HTML.table(table_data, col_width=['50%', '50%'], col_align=['center', 'center'], col_styles=['', ''])
            f.write(htmlcode)
            if test >= 4:
                table_data = [
                                ['b1_b4.png','b4_b1.png'],
                                ["<img src='%s' height='420' width='560'>" % (url + "RESULT_b2_b3.png"), "<img src='%s' height='420' width='560'>" % (url + "RESULT_b3_b2.png")],
                                ['b2_b4.png','b4_b2.png'],
                                ["<img src='%s' height='420' width='560'>" % (url + "RESULT_b1_b3.png"), "<img src='%s' height='420' width='560'>" % (url + "RESULT_b3_b1.png")],
                                ['b3_b4.png','b4_b3.png'],
                                ["<img src='%s' height='420' width='560'>" % (url + "RESULT_b3_b4.png"), "<img src='%s' height='420' width='560'>" % (url + "RESULT_b4_b3.png")]
                             ]
                htmlcode = HTML.table(table_data, col_width=['50%', '50%'], col_align=['center', 'center'], col_styles=['', ''])
                f.write(htmlcode)
                if test == 5:
                    table_data = [
                                    ['b1_b5.png','b5_b1.png'],
                                    ["<img src='%s' height='420' width='560'>" % (url + "RESULT_b1_b5.png"), "<img src='%s' height='420' width='560'>" % (url + "RESULT_b5_b1.png")],
                                    ['b2_b5.png','b5_b2.png'],
                                    ["<img src='%s' height='420' width='560'>" % (url + "RESULT_b2_b5.png"), "<img src='%s' height='420' width='560'>" % (url + "RESULT_b5_b2.png")],
                                    ['b3_b5.png','b5_b3.png'],
                                    ["<img src='%s' height='420' width='560'>" % (url + "RESULT_b3_b5.png"), "<img src='%s' height='420' width='560'>" % (url + "RESULT_b5_b3.png")],
                                    ['b4_b5.png','b5_b4.png'],
                                    ["<img src='%s' height='420' width='560'>" % (url + "RESULT_b4_b5.png"), "<img src='%s' height='420' width='560'>" % (url + "RESULT_b5_b4.png")]
                                 ]
                    htmlcode = HTML.table(table_data, col_width=['50%', '50%'], col_align=['center', 'center'], col_styles=['', ''])
                    f.write(htmlcode)

        f.close()


    def HTML_Create(self, test):
        start_time = time.strftime("%Y-%m-%d %H:%M:%S")
        self.html_file = self.path + "DVF" + str(self.chipset) + "_%s_%s.html" % (self.version_number, self.suite_user_info)
        f = open(self.html_file, 'a')
        print >> f, "<div align='Left'>"
        print >> f, "<table border='4' cellpadding='2' cellspacing='2' width='100%'>"
        print >> f, "<tr>"
        print >> f, '<th bgcolor="LightSalmon"><font size="5">DVF' + str(self.chipset) + ' AUTOMATION RESULTS</font></th>'

        table_data = [
            ['Board (DUT) Release Version ',      self.version_number],
            ['Starting Date',               start_time],
            ['Test Suite Info',             self.suite_user_info],
                     ]
        htmlcode = HTML.table(table_data, col_width=['50%', '50%'], col_align=['left','left'], col_styles=['background-color:Ivory', 'background-color:Ivory'])

        f.write(htmlcode)

        if test in [0, 1, 2]:
            htmlcode = HTML.table(header_row=['Case', 'Test Executed', 'Codec(s)', 'PTime(s)', 'Feature(s) Enabled', 'Call(s) On', 'Line IDs', 'Result', 'Observation(s)/Comment(s)', 'Iter'],
                        col_width=['7%', '12%', '6%', '5%', '11%', '5%', '9%', '10%', '30%', '5%'],
                        col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center'],
                        col_styles=['background-color:Aqua', 'background-color:Aqua', 'background-color:Aqua', 'background-color:Aqua', 'background-color:Aqua', 'background-color:Aqua', 'background-color:Aqua', 'background-color:Aqua', 'background-color:Aqua', 'background-color:Aqua']
                                  )
        elif test == 6:
            htmlcode = HTML.table(header_row=['Case', 'Test Executed', 'Codec(s)', 'PTime(s)', 'Feature(s)/Parameter(s) Enabled', 'Call(s) On', 'Line IDs', 'Result', 'Observation(s)/Comment(s)', 'Iter'],
                        col_width=['7%', '12%', '6%', '5%', '11%', '5%', '9%', '10%', '30%', '5%'],
                        col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center'],
                        col_styles=['background-color:Aqua', 'background-color:Aqua', 'background-color:Aqua', 'background-color:Aqua', 'background-color:Aqua', 'background-color:Aqua', 'background-color:Aqua', 'background-color:Aqua', 'background-color:Aqua', 'background-color:Aqua']
                                  )
        elif test in [7, 8]:
            htmlcode = HTML.table(header_row=['Case', 'Test Executed', 'Codec(s)', 'PTime', 'Feature', 'Line IDs', 'Result','Observation(s)/Comment(s)','Iter'],
                        col_width=['5%','11%', '5%', '5%', '9%', '8%','20%','32%','5%'],
                        col_align=['center','center','center','center','center','center', 'center', 'center','center'],
                        col_styles=['background-color:Aqua', 'background-color:Aqua', 'background-color:Aqua', 'background-color:Aqua','background-color:Aqua','background-color:Aqua','background-color:Aqua','background-color:Aqua','background-color:Aqua']
                                  )
        elif test == 9:
            htmlcode = HTML.table(header_row=['Test Number', 'Platform', 'Boot Observation/Result', 'IP (DHCP) Observation/Result'],
                col_width=['10%', '15%', '35%', '40%'],
                col_align=['center', 'center', 'center', 'center'],
                col_styles=['background-color:Aqua', 'background-color:Aqua', 'background-color:Aqua', 'background-color:Aqua']
                                  )
        elif test == -1:
    # for image load, build
            htmlcode = HTML.table(header_row=['Test Number', 'Platform', 'Boot Observation/Result', 'IP (DHCP) Observation/Result'],
                col_width=['10%', '15%', '35%', '40%'],
                col_align=['center', 'center', 'center', 'center'],
                col_styles=['background-color:Aqua ', 'background-color:Aqua', 'background-color:Aqua', 'background-color:Aqua']
                                  )
        if test not in [3, 4, 5]:
            f.write(htmlcode)

        f.close()


    def HTML_End(self):
        end_time = time.strftime("%Y-%m-%d %H:%M:%S")
        f = open(self.html_file, 'a')
        print >> f, "<div align='Left'>"
        print >> f, "<table border='4' cellpadding='2' cellspacing='2' width='100%'>"
        print >> f, "<tr>"
        print >> f, '<th bgcolor="LightSalmon"><font size="5">DVF' + str(self.chipset) + ' AUTOMATION RESULTS END</font></th>'

        table_data = ['Ending Date', end_time]

        htmlcode = HTML.table(table_data, col_width=['50%', '50%'], col_align=['left', 'left'], col_styles=['background-color:Ivory', 'background-color:Ivory'])

        f.write(htmlcode)


    def HTML_Write_Call(self, test_no, test, codec, ptime, features, call_unit, lineID, result1, result2, observation1, observation2, iteration, graph_path):
        if self.DEBUG == 1:
            print "##############HTML Write (Call) for %s ##############" % test_no
            print self.html_file

        f = open(self.html_file, 'a')

        pwd_tree = graph_path.split('/')
        l_path = len(pwd_tree)
        rel_path = './' + pwd_tree[l_path - 2] + '/'

        print "Folder : ",rel_path

        if test == "H/W_MUTE":
            url1 = rel_path + 'RESULT_b1_b2_mute.png'
            url2 = rel_path + 'RESULT_b2_b1_mute.png'
        elif test == "H/W_UNMUTE":
            url1 = rel_path + 'RESULT_b1_b2_unmute.png'
            url2 = rel_path + 'RESULT_b2_b1_unmute.png'
        elif test == 'DTMF_INBAND':
            url1 = rel_path + 'RESULT_graph.png'
            url2 = rel_path + 'RESULT_graph.png'
        else:
            url1 = rel_path + 'RESULT_b1_b2.png'
            url2 = rel_path + 'RESULT_b2_b1.png'

        HTML_COLORS = ['Black', 'Green', 'Silver', 'Lime', 'Gray', 'Olive', 'White', 'Orange', 'Navy', 'Red', 'Blue', 'Purple', 'Teal', 'Fuchsia', 'Aqua','Coral']

        if 'Pass' in result1 and 'Pass' in result2:
            table_data = [
                            [test_no, test, codec, ptime, features, call_unit, lineID, result1, result2, observation1, observation2, iteration]
                         ]
            htmlcode = HTML.table(table_data,['7%', '12%', '6%', '5%', '11%', '5%', '9%', '10%', '30%', '5%'],
                    col_width=['7%', '12%', '6%', '5%', '11%', '5%', '9%', '5%', '5%', '15%', '15%', '5%'],
                    col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center'],
                    col_styles=['', '', '', '', '', '', '', 'background-color:lime', 'background-color:lime', '', '', ''])
        elif 'Pass' in result1 and 'Fail' in result2:
            if 'RFC2833' in test:
                table_data = [
                                [test_no, test, codec, ptime, features, call_unit, lineID, result1, result2, observation1, observation2, iteration]
                             ]
            else:
                table_data = [
                                [test_no, test, codec, ptime, features, call_unit, lineID, result1, self.image(result2,url2), observation1, observation2, iteration]
                             ]
            htmlcode = HTML.table(table_data,
                    col_width=['7%', '12%', '6%', '5%', '11%', '5%', '9%', '5%', '5%', '15%', '15%', '5%'],
                    col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center'],
                    col_styles=['', '', '', '', '', '', '', 'background-color:lime', 'background-color:red', '', '', ''])
        elif 'Fail' in result1 and 'Pass' in result2:
            if 'RFC2833' in test:
                table_data = [
                                [test_no, test, codec, ptime, features, call_unit, lineID, result1, result2, observation1, observation2, iteration]
                             ]
            else:
                table_data = [
                                [test_no, test, codec, ptime, features, call_unit, lineID, self.image(result1,url1), result2, observation1, observation2, iteration]
                             ]
            htmlcode = HTML.table(table_data,
                    col_width=['7%', '12%', '6%', '5%', '11%', '5%', '9%', '5%', '5%', '15%', '15%', '5%'],
                    col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center'],
                    col_styles=['', '', '', '', '', '', '', 'background-color:red', 'background-color:lime', '', '', ''])
        elif 'Fail' in result1 and 'Fail' in result2:
            if 'RFC2833' in test:
                table_data = [
                                [test_no, test, codec, ptime, features, call_unit, lineID, result1, result2, observation1, observation2, iteration]
                             ]
            else:
                table_data = [
                                [test_no, test, codec, ptime, features, call_unit, lineID, self.image(result1,url1), self.image(result2,url2), observation1, observation2, iteration]
                             ]
            htmlcode = HTML.table(table_data,
                    col_width=['7%', '12%', '6%', '5%', '11%', '5%', '9%', '5%', '5%', '15%', '15%', '5%'],
                    col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center'],
                    col_styles=['', '', '', '', '', '', '', 'background-color:red', 'background-color:red', '', '', ''])
        elif 'Pass' in result1 and 'Error' in result2:
            if 'RFC2833' in test:
                table_data = [
                                [test_no, test, codec, ptime, features, call_unit, lineID, result1, result2, observation1, observation2, iteration]
                             ]
            else:
                table_data = [
                                [test_no, test, codec, ptime, features, call_unit, lineID, result1, self.image(result2,url2), observation1, observation2, iteration]
                             ]
            htmlcode = HTML.table(table_data,
                    col_width=['7%', '12%', '6%', '5%', '11%', '5%', '9%', '5%', '5%', '15%', '15%', '5%'],
                    col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center'],
                    col_styles=['', '', '', '', '', '', '', 'background-color:lime', 'background-color:Orange', '', '', ''])
        elif 'Error' in result1 and 'Pass' in result2:
            if 'RFC2833' in test:
                table_data = [
                                [test_no, test, codec, ptime, features, call_unit, lineID, result1, result2, observation1, observation2, iteration]
                             ]
            else:
                table_data = [
                                [test_no, test, codec, ptime, features, call_unit, lineID, self.image(result1,url1), result2, observation1, observation2, iteration]
                             ]
            htmlcode = HTML.table(table_data,
                    col_width=['7%', '12%', '6%', '5%', '11%', '5%', '9%', '5%', '5%', '15%', '15%', '5%'],
                    col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center'],
                    col_styles=['', '', '', '', '', '', '', 'background-color:Orange', 'background-color:lime', '', '', ''])
        elif 'Fail' in result1 and 'Error' in result2:
            if 'RFC2833' in test:
                table_data = [
                                [test_no, test, codec, ptime, features, call_unit, lineID, result1, result2, observation1, observation2, iteration]
                             ]
            else:
                table_data = [
                                [test_no, test, codec, ptime, features, call_unit, lineID, self.image(result1,url1), self.image(result2,url2), observation1, observation2, iteration]
                             ]
            htmlcode = HTML.table(table_data,
                    col_width=['7%', '12%', '6%', '5%', '11%', '5%', '9%', '5%', '5%', '15%', '15%', '5%'],
                    col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center'],
                    col_styles=['', '', '', '', '', '', '', 'background-color:red', 'background-color:Orange', '', '', ''])
        elif 'Error' in result1 and 'Fail' in result2:
            if 'RFC2833' in test:
                table_data = [
                                [test_no, test, codec, ptime, features, call_unit, lineID, result1, result2, observation1, observation2, iteration]
                             ]
            else:
                table_data = [
                                [test_no, test, codec, ptime, features, call_unit, lineID, self.image(result1,url1), self.image(result2,url2), observation1, observation2, iteration]
                             ]
            htmlcode = HTML.table(table_data,
                    col_width=['7%', '12%', '6%', '5%', '11%', '5%', '9%', '5%', '5%', '15%', '15%', '5%'],
                    col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center'],
                    col_styles=['', '', '', '', '', '', '', 'background-color:Orange', 'background-color:red', '', '', ''])
        elif 'Error' in result1 and 'Error' in result2:
            if 'RFC2833' in test:
                table_data = [
                                [test_no, test, codec, ptime, features, call_unit, lineID, result1, result2, observation1, observation2, iteration]
                             ]
            else:
                table_data = [
                                [test_no, test, codec, ptime, features, call_unit, lineID, self.image(result1,url1), self.image(result2,url2), observation1, observation2, iteration]
                             ]
            htmlcode = HTML.table(table_data,
                    col_width=['7%', '12%', '6%', '5%', '11%', '5%', '9%', '5%', '5%', '15%', '15%', '5%'],
                    col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center'],
                    col_styles=['', '', '', '', '', '', '', 'background-color:Orange', 'background-color:Orange', '', '', ''])
        else:
             table_data = [
                            [test_no, test, codec, ptime, features, call_unit, lineID, result1, result2, observation1, observation2, iteration]
                         ]
             htmlcode = HTML.table(table_data,
                    col_width=['7%', '12%', '6%', '5%', '11%', '5%', '9%', '5%', '5%', '15%', '15%', '5%'],
                    col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center'],
                    col_styles=['', '', '', '', '', '', '', 'background-color:#5599ff', 'background-color:#5599ff', '', '', ''])

        f.write(htmlcode)

        f.close()


    def HTML_Write_CallHoldResume(self, test_no, test, codec, ptime, features, call_unit, lineID, result1, result2, observation1, observation2, iteration, graph_path):
        if self.DEBUG == 1:
            print "##############HTML Write (Hold/Resume) for %s ##############" % test_no
            print self.html_file

        # Create a html file within the test case's output folder as a container to hold the image files

        abs_path = graph_path

        pwd_tree = graph_path.split('/')
        l_path = len(pwd_tree)
        rel_path = './' + pwd_tree[l_path - 2] + '/'

        self.graph_html(2, abs_path)

        f = open(self.html_file, 'a')

        if (observation1 == 'Voice detected during hold') or ('High power in silence zone' in observation1):
            url1 = rel_path + 'RESULT_b1_b2_hold.png'
        elif observation1 == 'Voice Quality not good during resume':
            url1 = rel_path + 'RESULT_b1_b2_res.png'
        else:#if (observation1 == 'Voice Quality not good') or (observation1 == 'No voice'):
            url1 = rel_path + 'RESULT_b1_b2.png'

        if (observation2 == 'Voice detected during hold') or ('High power in silence zone' in observation2):
            url2 = rel_path + 'RESULT_b2_b1_hold.png'
        elif observation2 == 'Voice Quality not good during resume':
            url2 = rel_path + 'RESULT_b2_b1_res.png'
        else:#if (observation2 == 'Voice Quality not good') or ( observation2 == 'No voice'):
            url2 = rel_path + 'RESULT_b2_b1.png'

        url = rel_path + 'graphs.html'

        HTML_COLORS = ['Black', 'Green', 'Silver', 'Lime', 'Gray', 'Olive', 'White', 'Orange', 'Navy', 'Red', 'Blue', 'Purple', 'Teal', 'Fuchsia', 'Aqua','Coral','Orange']

        if 'Pass' in result1 and 'Pass' in result2:
            table_data = [
                            [test_no, test, codec, ptime, features, call_unit, lineID, 'Pass', "B1->B2 : " + observation1 + "<BR>B1->B2 : " + observation2, iteration]
                         ]
            htmlcode = HTML.table(table_data,
                    col_width=['7%', '12%', '6%', '5%', '11%', '5%', '9%', '10%', '30%', '5%'],
                    col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center'],
                    col_styles=['', '', '', '', '', '', '', 'background-color:lime', '', ''])
        elif 'Pass' in result1  and 'Fail' in result2:
             table_data = [
                            [test_no, test, codec, ptime, features, call_unit, lineID, self.page(result2, url), "B1->B2 : " + observation1 + "<BR>B1->B2 : " + observation2, iteration]
                         ]
             htmlcode = HTML.table(table_data,
                    col_width=['7%', '12%', '6%', '5%', '11%', '5%', '9%', '10%', '30%', '5%'],
                    col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center'],
                    col_styles=['', '', '', '', '', '', '', 'background-color:orange', '', ''])
        elif 'Fail' in result1  and 'Pass' in result2:
             table_data = [
                            [test_no, test, codec, ptime, features, call_unit, lineID, self.page(result1, url), "B1->B2 : " + observation1 + "<BR>B1->B2 : " + observation2, iteration]
                         ]
             htmlcode = HTML.table(table_data,
                    col_width=['7%', '12%', '6%', '5%', '11%', '5%', '9%', '10%', '30%', '5%'],
                    col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center'],
                    col_styles=['', '', '', '', '', '', '', 'background-color:orange', '', ''])
        elif 'Fail' in result1  and 'Fail' in result2:
             table_data = [
                            [test_no, test, codec, ptime, features, call_unit, lineID, self.page(result1, url), "B1->B2 : " + observation1 + "<BR>B1->B2 : " + observation2, iteration]
                         ]
             htmlcode = HTML.table(table_data,
                    col_width=['7%', '12%', '6%', '5%', '11%', '5%', '9%', '10%', '30%', '5%'],
                    col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center'],
                    col_styles=['', '', '', '', '', '', '', 'background-color:red', '', ''])
        elif 'Pass' in result1  and 'Error' in result2:
             table_data = [
                            [test_no, test, codec, ptime, features, call_unit, lineID, 'Error occurred', "B1->B2 : " + observation1 + "<BR>B1->B2 : " + observation2, iteration]
                         ]
             htmlcode = HTML.table(table_data,
                    col_width=['7%', '12%', '6%', '5%', '11%', '5%', '9%', '10%', '30%', '5%'],
                    col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center'],
                    col_styles=['', '', '', '', '', '', '', 'background-color:gray', '', ''])
        elif 'Error' in result1  and 'Pass' in result2:
             table_data = [
                            [test_no, test, codec, ptime, features, call_unit, lineID, 'Error occurred', "B1->B2 : " + observation1 + "<BR>B1->B2 : " + observation2, iteration]
                         ]
             htmlcode = HTML.table(table_data,
                    col_width=['7%', '12%', '6%', '5%', '11%', '5%', '9%', '10%', '30%', '5%'],
                    col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center'],
                    col_styles=['', '', '', '', '', '', '', 'background-color:gray', '', ''])
        elif 'Fail' in result1  and 'Error' in result2:
             table_data = [
                            [test_no, test, codec, ptime, features, call_unit, lineID, 'Error occurred', "B1->B2 : " + observation1 + "<BR>B1->B2 : " + observation2, iteration]
                         ]
             htmlcode = HTML.table(table_data,
                    col_width=['7%', '12%', '6%', '5%', '11%', '5%', '9%', '10%', '30%', '5%'],
                    col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center'],
                    col_styles=['', '', '', '', '', '', '', 'background-color:gray', '', ''])
        elif 'Error' in result1  and 'Fail' in result2:
             table_data = [
                            [test_no,test,codec,ptime,features,call_unit,lineID,'Error occurred', "B1->B2 : " + observation1 + "<BR>B1->B2 : " + observation2, iteration]
                         ]
             htmlcode = HTML.table(table_data,
                    col_width=['7%', '12%', '6%', '5%', '11%', '5%', '9%', '10%', '30%', '5%'],
                    col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center'],
                    col_styles=['', '', '', '', '', '', '', 'background-color:gray', '', ''])
        elif 'Error' in result1  and 'Error' in result2:
             table_data = [
                            [test_no, test, codec, ptime, features, call_unit, lineID, 'Error occurred', "B1->B2 : " + observation1 + "<BR>B1->B2 : " + observation2, iteration]
                         ]
             htmlcode = HTML.table(table_data,
                    col_width=['7%', '12%', '6%', '5%', '11%', '5%', '9%', '10%', '30%', '5%'],
                    col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center'],
                    col_styles=['', '', '', '', '', '', '', 'background-color:gray', '', ''])
        else :
             table_data = [
                            [test_no, test, codec, ptime, features, call_unit, lineID, 'Unknown', "B1->B2 : " + observation1 + "<BR>B1->B2 : " + observation2, iteration]
                         ]
             htmlcode = HTML.table(table_data,
                    col_width=['7%', '12%', '6%', '5%', '11%', '5%', '9%', '10%', '30%', '5%'],
                    col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center'],
                    col_styles=['', '', '', '', '', '', '', 'background-color:#5599ff', '', ''])

        f.write(htmlcode)

        f.close()


    def HTML_Write_ConfCall(self, conf_type, test_no, test, codec, ptime, features, call_unit, lineID, result, observation, details, iteration, graph_path):
        if self.DEBUG == 1:
            print "##############HTML Write (Conference) for %s ##############" % test_no
            print self.html_file

        abs_path = graph_path

        pwd_tree = graph_path.split('/')
        l_path = len(pwd_tree)
        rel_path = './' + pwd_tree[l_path - 2] + '/'

        self.graph_html(conf_type, abs_path)
        # Create a html file within the test case's output folder as a container to hold the image files, use the Number parameter to pass it to
        # the

        f = open(self.html_file, 'a')

        if observation == details:
            obs_field = observation
        else:
            obs_field = observation + details

        url = rel_path + "graphs.html"

        HTML_COLORS = ['Black', 'Green', 'Silver', 'Lime', 'Gray', 'Olive', 'White', 'Orange', 'Navy', 'Red', 'Blue', 'Purple', 'Teal', 'Fuchsia', 'Aqua','Coral','Orange']

        if 'Pass' in result:
            table_data = [
                            [test_no, test, codec, ptime, features, call_unit, lineID, result, obs_field, iteration]
                         ]
            htmlcode = HTML.table(table_data,
                    col_width=['7%', '12%', '6%', '5%', '11%', '5%', '9%', '10%', '30%', '5%'],
                    col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center'],
                    col_styles=['', '', '', '', '', '', '', 'background-color:lime', '', ''])
        elif 'Fail' in result:
             table_data = [
                            [test_no, test, codec, ptime, features, call_unit, lineID, self.page(result, url), obs_field, iteration]
                         ]
             htmlcode = HTML.table(table_data,
                    col_width=['7%', '12%', '6%', '5%', '11%', '5%', '9%', '10%', '30%', '5%'],
                    col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center'],
                    col_styles=['', '', '', '', '', '', '', 'background-color:red', '', ''])
        else:
             table_data = [
                            [test_no, test, codec, ptime, features, call_unit, lineID, result, obs_field, iteration]
                         ]
             htmlcode = HTML.table(table_data,
                    col_width=['7%', '12%', '6%', '5%', '11%', '5%', '9%', '10%', '30%', '5%'],
                    col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center'],
                    col_styles=['', '', '', '', '', '', '', 'background-color:gray', '', ''])

        f.write(htmlcode)

        f.close()


    def HTML_Write_CMBS_Call(self, test_no, test_case, unit, iteration, call_info_dict):
    #call_type, call, codec, ptime, feature, result1, result2, observation1, observation2, graph1_list, graph2_list
        call_nos = len(call_info_dict)
        if self.DEBUG == 1:
            print "##############HTML Write (CMBS) for %s ##############" % test_no
            print self.html_file

        f = open(self.html_file, 'a')

        if self.DEBUG == 1:
            print "Updating test case Info...."

        test_case_data = [
            ["Test Case Number : ", test_no],
            ["Test Executed : ", test_case],
            ["Unit Used : ", unit],
            ["Iteration : ", iteration]
        ]

        htmlcode = HTML.table(test_case_data,
                              col_width=['25%', '75%'],
                              col_align=['left', 'left',],
                              col_styles=['background-color:#808080', ''])

        f.write(htmlcode)

        if self.DEBUG == 1:
            print "Updating call Info...."

        htmlcode = HTML.table(header_row=['Call', 'Call Type', 'codec', 'PTime', 'Feature(s) Enabled', 'Result', 'Observation(s)/Comment(s)'],
                    col_width=['10%', '15%', '9%', '6%', '10%', '20%', '30%'],
                    col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center'],
                    col_styles=['background-color:#00FFFF', 'background-color:#00FFFF', 'background-color:#00FFFF', 'background-color:#00FFFF', 'background-color:#00FFFF', 'background-color:#00FFFF', 'background-color:#00FFFF']
                              )

        f.write(htmlcode)

        if self.DEBUG == 1:
            print "call_dict : \n", call_info_dict
            print "keys : \n",call_info_dict.keys()

        if call_nos > 0:
            for i in range(0, call_nos):
                call = call_info_dict.keys()[i]

                if 'HOLD_RESUME' in test_case:
                    result1 = call_info_dict[call][4]
                    result2 = call_info_dict[call][5]
                    graph1 = call_info_dict[call][8]
                    graph2 = call_info_dict[call][9]
                    if 'Hold' in call:
                        if 'Fail' in result1 and 'Fail' in result2:
                            call_data = [
                                            [call] + call_info_dict[call][:8]
                                         ]
                            htmlcode = HTML.table(call_data, ['10%', '15%', '9%', '6%', '10%', '10%', '10%', '15%', '15%'],
                                    col_width=['10%', '15%', '9%', '6%', '10%', '10%', '10%', '15%', '15%'],
                                    col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center'],
                                    col_styles=['', '', '', '', '', 'background-color:lime', 'background-color:lime', '', ''])
                        else:
                            call_data = [
                                            [call] + call_info_dict[call][:4] + [self.image(result1, graph1)] + [self.image(result2, graph2)] + call_info_dict[call][6:8]
                                         ]
                            htmlcode = HTML.table(call_data, ['10%', '15%', '9%', '6%', '10%', '10%', '10%', '15%', '15%'],
                                    col_width=['10%', '15%', '9%', '6%', '10%', '10%', '10%', '15%', '15%'],
                                    col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center'],
                                    col_styles=['', '', '', '', '', 'background-color:red', 'background-color:red', '', ''])
                    else:
                        if 'Pass' in result1 and 'Pass' in result2:
                            call_data = [
                                [call] + call_info_dict[call][:8]
                            ]
                            htmlcode = HTML.table(call_data, ['10%', '15%', '9%', '6%', '10%', '10%', '10%', '15%', '15%'],
                                    col_width=['10%', '15%', '9%', '6%', '10%', '10%', '10%', '15%', '15%'],
                                    col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center'],
                                    col_styles=['', '', '', '', '', 'background-color:lime', 'background-color:lime', '', ''])
                        elif 'Pass' in result1 and 'Fail' in result2:
                            call_data = [
                                            [call] + call_info_dict[call][:5] + [self.image(result2, graph2)] + call_info_dict[call][6:8]
                                         ]
                            htmlcode = HTML.table(call_data, ['10%', '15%', '9%', '6%', '10%', '10%', '10%', '15%', '15%'],
                                    col_width=['10%', '15%', '9%', '6%', '10%', '10%', '10%', '15%', '15%'],
                                    col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center'],
                                    col_styles=['', '', '', '', '', 'background-color:lime', 'background-color:red', '', ''])
                        elif 'Fail' in result1 and 'Pass' in result2:
                            call_data = [
                                            [call] + call_info_dict[call][:4] + [self.image(result1, graph1)] + call_info_dict[call][5:8]
                                         ]
                            htmlcode = HTML.table(call_data, ['10%', '15%', '9%', '6%', '10%', '10%', '10%', '15%', '15%'],
                                    col_width=['10%', '15%', '9%', '6%', '10%', '10%', '10%', '15%', '15%'],
                                    col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center'],
                                    col_styles=['', '', '', '', '', 'background-color:red', 'background-color:lime', '', ''])
                        elif 'Fail' in result1 and 'Fail' in result2:
                            call_data = [
                                            [call] + call_info_dict[call][:4] + [self.image(result1, graph1)] + [self.image(result2, graph2)] + call_info_dict[call][6:8]
                                         ]
                            htmlcode = HTML.table(call_data, ['10%', '15%', '9%', '6%', '10%', '10%', '10%', '15%', '15%'],
                                    col_width=['10%', '15%', '9%', '6%', '10%', '10%', '10%', '15%', '15%'],
                                    col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center'],
                                    col_styles=['', '', '', '', '', 'background-color:red', 'background-color:red', '', ''])
                        elif 'Pass' in result1 and 'Error' in result2:
                            call_data = [
                                            [call] + call_info_dict[call][:5] + [self.image(result2, graph2)] + call_info_dict[call][6:8]
                                         ]
                            htmlcode = HTML.table(call_data, ['10%', '15%', '9%', '6%', '10%', '10%', '10%', '15%', '15%'],
                                    col_width=['10%', '15%', '9%', '6%', '10%', '10%', '10%', '15%', '15%'],
                                    col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center'],
                                    col_styles=['', '', '', '', '', 'background-color:lime', 'background-color:orange', '', ''])
                        elif 'Error' in result1 and 'Pass' in result2:
                            call_data = [
                                            [call] + call_info_dict[call][:4] + [self.image(result1, graph1)] + call_info_dict[call][5:8]
                                         ]
                            htmlcode = HTML.table(call_data, ['10%', '15%', '9%', '6%', '10%', '10%', '10%', '15%', '15%'],
                                    col_width=['10%', '15%', '9%', '6%', '10%', '10%', '10%', '15%', '15%'],
                                    col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center'],
                                    col_styles=['', '', '', '', '', 'background-color:orange', 'background-color:lime', '', ''])
                        elif 'Fail' in result1 and 'Error' in result2:
                            call_data = [
                                            [call] + call_info_dict[call][:4] + [self.image(result1, graph1)] + [self.image(result2, graph2)] + call_info_dict[call][6:8]
                                         ]
                            htmlcode = HTML.table(call_data, ['10%', '15%', '9%', '6%', '10%', '10%', '10%', '15%', '15%'],
                                    col_width=['10%', '15%', '9%', '6%', '10%', '10%', '10%', '15%', '15%'],
                                    col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center'],
                                    col_styles=['', '', '', '', '', 'background-color:red', 'background-color:orange', '', ''])
                        elif 'Error' in result1 and 'Fail' in result2:
                            call_data = [
                                            [call] + call_info_dict[call][:4] + [self.image(result1, graph1)] + [self.image(result2, graph2)] + call_info_dict[call][6:8]
                                         ]
                            htmlcode = HTML.table(call_data, ['10%', '15%', '9%', '6%', '10%', '10%', '10%', '15%', '15%'],
                                    col_width=['10%', '15%', '9%', '6%', '10%', '10%', '10%', '15%', '15%'],
                                    col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center'],
                                    col_styles=['', '', '', '', '', 'background-color:orange', 'background-color:red', '', ''])
                        elif 'Error' in result1 and 'Error' in result2:
                            call_data = [
                                            [call] + call_info_dict[call][:4] + [self.image(result1, graph1)] + [self.image(result2, graph2)] + call_info_dict[call][6:8]
                                         ]
                            htmlcode = HTML.table(call_data, ['10%', '15%', '9%', '6%', '10%', '10%', '10%', '15%', '15%'],
                                    col_width=['10%', '15%', '9%', '6%', '10%', '10%', '10%', '15%', '15%'],
                                    col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center'],
                                    col_styles=['', '', '', '', '', 'background-color:orange', 'background-color:orange', '', ''])
                        else:
                            call_data = [
                                [call] + call_info_dict[call]
                                        ]
                            htmlcode = HTML.table(call_data, ['10%', '15%', '9%', '6%', '10%', '10%', '10%', '15%', '15%'],
                                    col_width=['10%', '15%', '9%', '6%', '10%', '10%', '10%', '15%', '15%'],
                                    col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center'],
                                    col_styles=['', '', '', '', '', 'background-color:#5599ff', 'background-color:#5599ff', '', ''])

                elif test_case == 'INTER_CONF':

                    result = call_info_dict[call][4]
                    graph = call_info_dict[call][6]
                    line_ver = int(call_info_dict[call][7])
                    pwd_tree = graph.split('/')
                    l_path = len(pwd_tree)
                    rel_path = './' + pwd_tree[l_path - 2] + '/'
                    url = graph + "graphs.html"
                    f_sub = open(url, 'a')
                    table_data = [
                                    ['h1_h2.png','h2_h1.png'],
                                    ["<img src='%s' height='420' width='560'>" % (graph + "RESULT_h1_h2.png"), "<img src='%s' height='420' width='560'>" % (graph + "RESULT_h2_h1.png")]
                                 ]
                    htmlcode = HTML.table(table_data, col_width=['50%', '50%'], col_align=['center', 'center'], col_styles=['', ''])
                    f_sub.write(htmlcode)
                    if line_ver:
                        table_data = [
                                        ['h1_h2_l1.png','h2_h1_l1.png'],
                                        ["<img src='%s' height='420' width='560'>" % (graph + "RESULT_h1_h2_l1.png"), "<img src='%s' height='420' width='560'>" % (graph + "RESULT_h1_h2_l1.png")]
                                     ]
                        htmlcode = HTML.table(table_data, col_width=['50%', '50%'], col_align=['center', 'center'], col_styles=['', ''])
                        f_sub.write(htmlcode)
                        table_data = [
                                        ['h1_h2_l2.png','h2_h1_l2.png'],
                                        ["<img src='%s' height='420' width='560'>" % (graph + "RESULT_h1_h2_l2.png"), "<img src='%s' height='420' width='560'>" % (graph + "RESULT_h1_h2_l2.png")]
                                     ]
                        htmlcode = HTML.table(table_data, col_width=['50%', '50%'], col_align=['center', 'center'], col_styles=['', ''])
                        f_sub.write(htmlcode)
                    table_data = [
                                    ['h1_h3.png','h3_h1.png'],
                                    ["<img src='%s' height='420' width='560'>" % (graph + "RESULT_h1_h3.png"), "<img src='%s' height='420' width='560'>" % (graph + "RESULT_h3_h1.png")]
                                 ]
                    htmlcode = HTML.table(table_data, col_width=['50%', '50%'], col_align=['center', 'center'], col_styles=['', ''])
                    f_sub.write(htmlcode)
                    table_data = [
                                    ['h2_h3.png','h3_h2.png'],
                                    ["<img src='%s' height='420' width='560'>" % (graph + "RESULT_h2_h3.png"), "<img src='%s' height='420' width='560'>" % (graph + "RESULT_h3_h2.png")]
                                 ]
                    htmlcode = HTML.table(table_data, col_width=['50%', '50%'], col_align=['center', 'center'], col_styles=['', ''])
                    f_sub.write(htmlcode)
                    HTML_COLORS = ['Black', 'Green', 'Silver', 'Lime', 'Gray', 'Olive', 'White', 'Orange', 'Navy', 'Red', 'Blue', 'Purple', 'Teal', 'Fuchsia', 'Aqua','Coral','Orange']
                    if 'Pass' in result:
                        call_data = [
                                        [call] + call_info_dict[call][:6]
                                     ]
                        htmlcode = HTML.table(call_data, ['10%', '15%', '9%', '6%', '10%', '20%', '30%'],
                                col_width=['10%', '15%', '9%', '6%', '10%', '20%', '30%'],
                                col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center'],
                                col_styles=['', '', '', '', '', 'background-color:lime', ''])
                    else:
                        call_data = [
                                        [call] + call_info_dict[call][:4] + [self.page(result, url)] + [call_info_dict[call][5]]
                                     ]
                        htmlcode = HTML.table(call_data, ['10%', '15%', '9%', '6%', '10%', '20%', '30%'],
                                col_width=['10%', '15%', '9%', '6%', '10%', '20%', '30%'],
                                col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center'],
                                col_styles=['', '', '', '', '', 'background-color:red', ''])

                elif test_case == 'CALL_TOGGLE_IN':

                    result = call_info_dict[call][4]
                    graph = call_info_dict[call][6]
                    pwd_tree = graph.split('/')
                    l_path = len(pwd_tree)
                    rel_path = './' + pwd_tree[l_path - 2] + '/'
                    url = graph + "graphs.html"
                    f_sub = open(url, 'a')
                    table_data = [
                                    ['h1_b1_incoming.png','b1_h1_incoming.png'],
                                    ["<img src='%s' height='420' width='560'>" % (graph + "RESULT_h1_b1_incoming.png"), "<img src='%s' height='420' width='560'>" % (graph + "RESULT_b1_h1_incoming.png")]
                                 ]
                    htmlcode = HTML.table(table_data, col_width=['50%', '50%'], col_align=['center', 'center'], col_styles=['', ''])
                    f_sub.write(htmlcode)
                    table_data = [
                                    ['h1_b2_incoming.png','b2_h1_incoming.png'],
                                    ["<img src='%s' height='420' width='560'>" % (graph + "RESULT_h1_b2_incoming.png"), "<img src='%s' height='420' width='560'>" % (graph + "RESULT_b2_h1_incoming.png")]
                                 ]
                    htmlcode = HTML.table(table_data, col_width=['50%', '50%'], col_align=['center', 'center'], col_styles=['', ''])
                    f_sub.write(htmlcode)
                    table_data = [
                                    ['h1_b1_in_tog0.png','b1_h1_in_tog0.png'],
                                    ["<img src='%s' height='420' width='560'>" % (graph + "RESULT_h1_b1_in_tog0.png"), "<img src='%s' height='420' width='560'>" % (graph + "RESULT_b1_h1_in_tog0.png")]
                                 ]
                    htmlcode = HTML.table(table_data, col_width=['50%', '50%'], col_align=['center', 'center'], col_styles=['', ''])
                    f_sub.write(htmlcode)
                    table_data = [
                                    ['h1_b2_in_tog0.png','b2_h1_in_tog0.png'],
                                    ["<img src='%s' height='420' width='560'>" % (graph + "RESULT_h1_b2_in_tog0.png"), "<img src='%s' height='420' width='560'>" % (graph + "RESULT_b2_h1_in_tog0.png")]
                                 ]
                    htmlcode = HTML.table(table_data, col_width=['50%', '50%'], col_align=['center', 'center'], col_styles=['', ''])
                    f_sub.write(htmlcode)
                    table_data = [
                                    ['h1_b1_in_tog1.png','b1_h1_in_tog1.png'],
                                    ["<img src='%s' height='420' width='560'>" % (graph + "RESULT_h1_b1_in_tog1.png"), "<img src='%s' height='420' width='560'>" % (graph + "RESULT_b1_h1_in_tog1.png")]
                                 ]
                    htmlcode = HTML.table(table_data, col_width=['50%', '50%'], col_align=['center', 'center'], col_styles=['', ''])
                    f_sub.write(htmlcode)
                    table_data = [
                                    ['h1_b2_in_tog1.png','b2_h1_in_tog1.png'],
                                    ["<img src='%s' height='420' width='560'>" % (graph + "RESULT_h1_b2_in_tog1.png"), "<img src='%s' height='420' width='560'>" % (graph + "RESULT_b2_h1_in_tog1.png")]
                                 ]
                    htmlcode = HTML.table(table_data, col_width=['50%', '50%'], col_align=['center', 'center'], col_styles=['', ''])
                    f_sub.write(htmlcode)
                    HTML_COLORS = ['Black', 'Green', 'Silver', 'Lime', 'Gray', 'Olive', 'White', 'Orange', 'Navy', 'Red', 'Blue', 'Purple', 'Teal', 'Fuchsia', 'Aqua','Coral','Orange']
                    if 'Pass' in result:
                        call_data = [
                                        [call] + call_info_dict[call][:6]
                                     ]
                        htmlcode = HTML.table(call_data, ['10%', '15%', '9%', '6%', '10%', '20%', '30%'],
                                col_width=['10%', '15%', '9%', '6%', '10%', '20%', '30%'],
                                col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center'],
                                col_styles=['', '', '', '', '', 'background-color:lime', ''])
                    else:
                        call_data = [
                                        [call] + call_info_dict[call][:4] + [self.page(result, url)] + [call_info_dict[call][5]]
                                     ]
                        htmlcode = HTML.table(call_data, ['10%', '15%', '9%', '6%', '10%', '20%', '30%'],
                                col_width=['10%', '15%', '9%', '6%', '10%', '20%', '30%'],
                                col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center'],
                                col_styles=['', '', '', '', '', 'background-color:red', ''])

                elif test_case == 'CALL_TOGGLE_OUT':

                    result = call_info_dict[call][4]
                    graph = call_info_dict[call][6]
                    pwd_tree = graph.split('/')
                    l_path = len(pwd_tree)
                    rel_path = './' + pwd_tree[l_path - 2] + '/'
                    url = graph + "graphs.html"
                    f_sub = open(url, 'a')
                    table_data = [
                                    ['h1_b1_outgoing.png','b1_h1_outgoing.png'],
                                    ["<img src='%s' height='420' width='560'>" % (graph + "RESULT_h1_b1_outgoing.png"), "<img src='%s' height='420' width='560'>" % (graph + "RESULT_b1_h1_outgoing.png")]
                                 ]
                    htmlcode = HTML.table(table_data, col_width=['50%', '50%'], col_align=['center', 'center'], col_styles=['', ''])
                    f_sub.write(htmlcode)
                    table_data = [
                                    ['h1_b2_outgoing.png','b2_h1_outgoing.png'],
                                    ["<img src='%s' height='420' width='560'>" % (graph + "RESULT_h1_b2_outgoing.png"), "<img src='%s' height='420' width='560'>" % (graph + "RESULT_b2_h1_outgoing.png")]
                                 ]
                    htmlcode = HTML.table(table_data, col_width=['50%', '50%'], col_align=['center', 'center'], col_styles=['', ''])
                    f_sub.write(htmlcode)
                    table_data = [
                                    ['h1_b1_out_tog0.png','b1_h1_out_tog0.png'],
                                    ["<img src='%s' height='420' width='560'>" % (graph + "RESULT_h1_b1_out_tog0.png"), "<img src='%s' height='420' width='560'>" % (graph + "RESULT_b1_h1_out_tog0.png")]
                                 ]
                    htmlcode = HTML.table(table_data, col_width=['50%', '50%'], col_align=['center', 'center'], col_styles=['', ''])
                    f_sub.write(htmlcode)
                    table_data = [
                                    ['h1_b2_out_tog0.png','b2_h1_out_tog0.png'],
                                    ["<img src='%s' height='420' width='560'>" % (graph + "RESULT_h1_b2_out_tog0.png"), "<img src='%s' height='420' width='560'>" % (graph + "RESULT_b2_h1_out_tog0.png")]
                                 ]
                    htmlcode = HTML.table(table_data, col_width=['50%', '50%'], col_align=['center', 'center'], col_styles=['', ''])
                    f_sub.write(htmlcode)
                    table_data = [
                                    ['h1_b1_out_tog1.png','b1_h1_out_tog1.png'],
                                    ["<img src='%s' height='420' width='560'>" % (graph + "RESULT_h1_b1_out_tog1.png"), "<img src='%s' height='420' width='560'>" % (graph + "RESULT_b1_h1_out_tog1.png")]
                                 ]
                    htmlcode = HTML.table(table_data, col_width=['50%', '50%'], col_align=['center', 'center'], col_styles=['', ''])
                    f_sub.write(htmlcode)
                    table_data = [
                                    ['h1_b2_out_tog1.png','b2_h1_out_tog1.png'],
                                    ["<img src='%s' height='420' width='560'>" % (graph + "RESULT_h1_b2_out_tog1.png"), "<img src='%s' height='420' width='560'>" % (graph + "RESULT_b2_h1_out_tog1.png")]
                                 ]
                    htmlcode = HTML.table(table_data, col_width=['50%', '50%'], col_align=['center', 'center'], col_styles=['', ''])
                    f_sub.write(htmlcode)
                    HTML_COLORS = ['Black', 'Green', 'Silver', 'Lime', 'Gray', 'Olive', 'White', 'Orange', 'Navy', 'Red', 'Blue', 'Purple', 'Teal', 'Fuchsia', 'Aqua','Coral','Orange']
                    if 'Pass' in result:
                        call_data = [
                                        [call] + call_info_dict[call][:6]
                                     ]
                        htmlcode = HTML.table(call_data, ['10%', '15%', '9%', '6%', '10%', '20%', '30%'],
                                col_width=['10%', '15%', '9%', '6%', '10%', '20%', '30%'],
                                col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center'],
                                col_styles=['', '', '', '', '', 'background-color:lime', ''])
                    else:
                        call_data = [
                                        [call] + call_info_dict[call][:4] + [self.page(result, url)] + [call_info_dict[call][5]]
                                     ]
                        htmlcode = HTML.table(call_data, ['10%', '15%', '9%', '6%', '10%', '20%', '30%'],
                                col_width=['10%', '15%', '9%', '6%', '10%', '20%', '30%'],
                                col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center'],
                                col_styles=['', '', '', '', '', 'background-color:red', ''])

                elif test_case == 'CALL_TOGGLE_INOUT':

                    result = call_info_dict[call][4]
                    graph = call_info_dict[call][6]
                    pwd_tree = graph.split('/')
                    l_path = len(pwd_tree)
                    rel_path = './' + pwd_tree[l_path - 2] + '/'
                    url = graph + "graphs.html"
                    f_sub = open(url, 'a')
                    table_data = [
                                    ['h1_b1_incoming.png','b1_h1_incoming.png'],
                                    ["<img src='%s' height='420' width='560'>" % (graph + "RESULT_h1_b1_incoming.png"), "<img src='%s' height='420' width='560'>" % (graph + "RESULT_b1_h1_incoming.png")]
                                 ]
                    htmlcode = HTML.table(table_data, col_width=['50%', '50%'], col_align=['center', 'center'], col_styles=['', ''])
                    f_sub.write(htmlcode)
                    table_data = [
                                    ['h1_b2_outgoing.png','b2_h1_outgoing.png'],
                                    ["<img src='%s' height='420' width='560'>" % (graph + "RESULT_h1_b2_outgoing.png"), "<img src='%s' height='420' width='560'>" % (graph + "RESULT_b2_h1_outgoing.png")]
                                 ]
                    htmlcode = HTML.table(table_data, col_width=['50%', '50%'], col_align=['center', 'center'], col_styles=['', ''])
                    f_sub.write(htmlcode)
                    table_data = [
                                    ['h1_b1_in_tog0.png','b1_h1_in_tog0.png'],
                                    ["<img src='%s' height='420' width='560'>" % (graph + "RESULT_h1_b1_in_tog0.png"), "<img src='%s' height='420' width='560'>" % (graph + "RESULT_b1_h1_in_tog0.png")]
                                 ]
                    htmlcode = HTML.table(table_data, col_width=['50%', '50%'], col_align=['center', 'center'], col_styles=['', ''])
                    f_sub.write(htmlcode)
                    table_data = [
                                    ['h1_b2_out_tog0.png','b2_h1_out_tog0.png'],
                                    ["<img src='%s' height='420' width='560'>" % (graph + "RESULT_h1_b2_out_tog0.png"), "<img src='%s' height='420' width='560'>" % (graph + "RESULT_b2_h1_out_tog0.png")]
                                 ]
                    htmlcode = HTML.table(table_data, col_width=['50%', '50%'], col_align=['center', 'center'], col_styles=['', ''])
                    f_sub.write(htmlcode)
                    table_data = [
                                    ['h1_b1_in_tog1.png','b1_h1_in_tog1.png'],
                                    ["<img src='%s' height='420' width='560'>" % (graph + "RESULT_h1_b1_in_tog1.png"), "<img src='%s' height='420' width='560'>" % (graph + "RESULT_b1_h1_in_tog1.png")]
                                 ]
                    htmlcode = HTML.table(table_data, col_width=['50%', '50%'], col_align=['center', 'center'], col_styles=['', ''])
                    f_sub.write(htmlcode)
                    table_data = [
                                    ['h1_b2_out_tog1.png','b2_h1_out_tog1.png'],
                                    ["<img src='%s' height='420' width='560'>" % (graph + "RESULT_h1_b2_out_tog1.png"), "<img src='%s' height='420' width='560'>" % (graph + "RESULT_b2_h1_out_tog1.png")]
                                 ]
                    htmlcode = HTML.table(table_data, col_width=['50%', '50%'], col_align=['center', 'center'], col_styles=['', ''])
                    f_sub.write(htmlcode)
                    HTML_COLORS = ['Black', 'Green', 'Silver', 'Lime', 'Gray', 'Olive', 'White', 'Orange', 'Navy', 'Red', 'Blue', 'Purple', 'Teal', 'Fuchsia', 'Aqua','Coral','Orange']
                    if 'Pass' in result:
                        call_data = [
                                        [call] + call_info_dict[call][:6]
                                     ]
                        htmlcode = HTML.table(call_data,['10%', '15%', '9%', '6%', '10%', '20%', '30%'],
                                col_width=['10%', '15%', '9%', '6%', '10%', '20%', '30%'],
                                col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center'],
                                col_styles=['', '', '', '', '', 'background-color:lime', ''])
                    else:
                        call_data = [
                                        [call] + call_info_dict[call][:4] + [self.page(result, url)] + [call_info_dict[call][5]]
                                     ]
                        htmlcode = HTML.table(call_data,['10%', '15%', '9%', '6%', '10%', '20%', '30%'],
                                col_width=['10%', '15%', '9%', '6%', '10%', '20%', '30%'],
                                col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center'],
                                col_styles=['', '', '', '', '', 'background-color:red', ''])

                elif test_case == 'CALL_TOGGLE_OUTIN':

                    result = call_info_dict[call][4]
                    graph = call_info_dict[call][6]
                    pwd_tree = graph.split('/')
                    l_path = len(pwd_tree)
                    rel_path = './' + pwd_tree[l_path - 2] + '/'
                    url = graph + "graphs.html"
                    f_sub = open(url, 'a')
                    table_data = [
                                    ['h1_b1_outgoing.png','b1_h1_outgoing.png'],
                                    ["<img src='%s' height='420' width='560'>" % (graph + "RESULT_h1_b1_outgoing.png"), "<img src='%s' height='420' width='560'>" % (graph + "RESULT_b1_h1_outgoing.png")]
                                 ]
                    htmlcode = HTML.table(table_data, col_width=['50%', '50%'], col_align=['center', 'center'], col_styles=['', ''])
                    f_sub.write(htmlcode)
                    table_data = [
                                    ['h1_b2_incoming.png','b2_h1_incoming.png'],
                                    ["<img src='%s' height='420' width='560'>" % (graph + "RESULT_h1_b2_incoming.png"), "<img src='%s' height='420' width='560'>" % (graph + "RESULT_b2_h1_incoming.png")]
                                 ]
                    htmlcode = HTML.table(table_data, col_width=['50%', '50%'], col_align=['center', 'center'], col_styles=['', ''])
                    f_sub.write(htmlcode)
                    table_data = [
                                    ['h1_b1_out_tog0.png','b1_h1_out_tog0.png'],
                                    ["<img src='%s' height='420' width='560'>" % (graph + "RESULT_h1_b1_out_tog0.png"), "<img src='%s' height='420' width='560'>" % (graph + "RESULT_b1_h1_out_tog0.png")]
                                 ]
                    htmlcode = HTML.table(table_data, col_width=['50%', '50%'], col_align=['center', 'center'], col_styles=['', ''])
                    f_sub.write(htmlcode)
                    table_data = [
                                    ['h1_b2_in_tog0.png','b2_h1_in_tog0.png'],
                                    ["<img src='%s' height='420' width='560'>" % (graph + "RESULT_h1_b2_in_tog0.png"), "<img src='%s' height='420' width='560'>" % (graph + "RESULT_b2_h1_in_tog0.png")]
                                 ]
                    htmlcode = HTML.table(table_data, col_width=['50%', '50%'], col_align=['center', 'center'], col_styles=['', ''])
                    f_sub.write(htmlcode)
                    table_data = [
                                    ['h1_b1_out_tog1.png','b1_h1_out_tog1.png'],
                                    ["<img src='%s' height='420' width='560'>" % (graph + "RESULT_h1_b1_out_tog1.png"), "<img src='%s' height='420' width='560'>" % (graph + "RESULT_b1_h1_out_tog1.png")]
                                 ]
                    htmlcode = HTML.table(table_data, col_width=['50%', '50%'], col_align=['center', 'center'], col_styles=['', ''])
                    f_sub.write(htmlcode)
                    table_data = [
                                    ['h1_b2_in_tog1.png','b2_h1_in_tog1.png'],
                                    ["<img src='%s' height='420' width='560'>" % (graph + "RESULT_h1_b2_in_tog1.png"), "<img src='%s' height='420' width='560'>" % (graph + "RESULT_b2_h1_in_tog1.png")]
                                 ]
                    htmlcode = HTML.table(table_data, col_width=['50%', '50%'], col_align=['center', 'center'], col_styles=['', ''])
                    f_sub.write(htmlcode)
                    HTML_COLORS = ['Black', 'Green', 'Silver', 'Lime', 'Gray', 'Olive', 'White', 'Orange', 'Navy', 'Red', 'Blue', 'Purple', 'Teal', 'Fuchsia', 'Aqua','Coral','Orange']
                    if 'Pass' in result:
                        call_data = [
                                        [call] + call_info_dict[call][:6]
                                     ]
                        htmlcode = HTML.table(call_data, ['10%', '15%', '9%', '6%', '10%', '20%', '30%'],
                                col_width=['10%', '15%', '9%', '6%', '10%', '20%', '30%'],
                                col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center'],
                                col_styles=['', '', '', '', '', 'background-color:lime', ''])
                    else:
                        call_data = [
                                        [call] + call_info_dict[call][:4] + [self.page(result, url)] + [call_info_dict[call][5]]
                                     ]
                        htmlcode = HTML.table(call_data, ['10%', '15%', '9%', '6%', '10%', '20%', '30%'],
                                col_width=['10%', '15%', '9%', '6%', '10%', '20%', '30%'],
                                col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center'],
                                col_styles=['', '', '', '', '', 'background-color:red', ''])

                else:

                    result1 = call_info_dict[call][4]
                    result2 = call_info_dict[call][5]
                    graph1 = call_info_dict[call][8]
                    graph2 = call_info_dict[call][9]
                    if 'Pass' in result1 and 'Pass' in result2:
                        call_data = [
                            [call] + call_info_dict[call][:8]
                                    ]
                        htmlcode = HTML.table(call_data, ['10%', '15%', '9%', '6%', '10%', '10%', '10%', '15%', '15%'],
                                col_width=['10%', '15%', '9%', '6%', '10%', '10%', '10%', '15%', '15%'],
                                col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center'],
                                col_styles=['', '', '', '', '', 'background-color:lime', 'background-color:lime', '', ''])
                    elif 'Pass' in result1 and 'Fail' in result2:
                        call_data = [
                                        [call] + call_info_dict[call][:5] + [self.image(result2, graph2)] + call_info_dict[call][6:8]
                                     ]
                        htmlcode = HTML.table(call_data, ['10%', '15%', '9%', '6%', '10%', '10%', '10%', '15%', '15%'],
                                col_width=['10%', '15%', '9%', '6%', '10%', '10%', '10%', '15%', '15%'],
                                col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center'],
                                col_styles=['', '', '', '', '', 'background-color:lime', 'background-color:red', '', ''])
                    elif 'Fail' in result1 and 'Pass' in result2:
                        call_data = [
                                        [call] + call_info_dict[call][:4] + [self.image(result1, graph1)] + call_info_dict[call][5:8]
                                     ]
                        htmlcode = HTML.table(call_data, ['10%', '15%', '9%', '6%', '10%', '10%', '10%', '15%', '15%'],
                                col_width=['10%', '15%', '9%', '6%', '10%', '10%', '10%', '15%', '15%'],
                                col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center'],
                                col_styles=['', '', '', '', '', 'background-color:red', 'background-color:lime', '', ''])
                    elif 'Fail' in result1 and 'Fail' in result2:
                        call_data = [
                                        [call] + call_info_dict[call][:4] + [self.image(result1, graph1)] + [self.image(result2, graph2)] + call_info_dict[call][6:8]
                                     ]
                        htmlcode = HTML.table(call_data, ['10%', '15%', '9%', '6%', '10%', '10%', '10%', '15%', '15%'],
                                col_width=['10%', '15%', '9%', '6%', '10%', '10%', '10%', '15%', '15%'],
                                col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center'],
                                col_styles=['', '', '', '', '', 'background-color:red', 'background-color:red', '', ''])
                    elif 'Pass' in result1 and 'Error' in result2:
                        call_data = [
                                        [call] + call_info_dict[call][:5] + [self.image(result2, graph2)] + call_info_dict[call][6:8]
                                     ]
                        htmlcode = HTML.table(call_data, ['10%', '15%', '9%', '6%', '10%', '10%', '10%', '15%', '15%'],
                                col_width=['10%', '15%', '9%', '6%', '10%', '10%', '10%', '15%', '15%'],
                                col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center'],
                                col_styles=['', '', '', '', '', 'background-color:lime', 'background-color:orange', '', ''])
                    elif 'Error' in result1 and 'Pass' in result2:
                        call_data = [
                                        [call] + call_info_dict[call][:4] + [self.image(result1, graph1)] + call_info_dict[call][5:8]
                                     ]
                        htmlcode = HTML.table(call_data, ['10%', '15%', '9%', '6%', '10%', '10%', '10%', '15%', '15%'],
                                col_width=['10%', '15%', '9%', '6%', '10%', '10%', '10%', '15%', '15%'],
                                col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center'],
                                col_styles=['', '', '', '', '', 'background-color:orange', 'background-color:lime', '', ''])
                    elif 'Fail' in result1 and 'Error' in result2:
                        call_data = [
                                        [call] + call_info_dict[call][:4] + [self.image(result1, graph1)] + [self.image(result2, graph2)] + call_info_dict[call][6:8]
                                     ]
                        htmlcode = HTML.table(call_data, ['10%', '15%', '9%', '6%', '10%', '10%', '10%', '15%', '15%'],
                                col_width=['10%', '15%', '9%', '6%', '10%', '10%', '10%', '15%', '15%'],
                                col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center'],
                                col_styles=['', '', '', '', '', 'background-color:red', 'background-color:orange', '', ''])
                    elif 'Error' in result1 and 'Fail' in result2:
                        call_data = [
                                        [call] + call_info_dict[call][:4] + [self.image(result1, graph1)] + [self.image(result2, graph2)] + call_info_dict[call][6:8]
                                     ]
                        htmlcode = HTML.table(call_data, ['10%', '15%', '9%', '6%', '10%', '10%', '10%', '15%', '15%'],
                                col_width=['10%', '15%', '9%', '6%', '10%', '10%', '10%', '15%', '15%'],
                                col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center'],
                                col_styles=['', '', '', '', '', 'background-color:orange', 'background-color:red', '', ''])
                    elif 'Error' in result1 and 'Error' in result2:
                        call_data = [
                                        [call] + call_info_dict[call][:4] + [self.image(result1, graph1)] + [self.image(result2, graph2)] + call_info_dict[call][6:8]
                                     ]
                        htmlcode = HTML.table(call_data, ['10%', '15%', '9%', '6%', '10%', '10%', '10%', '15%', '15%'],
                                col_width=['10%', '15%', '9%', '6%', '10%', '10%', '10%', '15%', '15%'],
                                col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center'],
                                col_styles=['', '', '', '', '', 'background-color:orange', 'background-color:orange', '', ''])
                    else:
                        call_data = [
                            [call] + call_info_dict[call][:8]
                        ]
                        htmlcode = HTML.table(call_data, ['10%', '15%', '9%', '6%', '10%', '10%', '10%', '15%', '15%'],
                                col_width=['10%', '15%', '9%', '6%', '10%', '10%', '10%', '15%', '15%'],
                                col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center'],
                                col_styles=['', '', '', '', '', 'background-color:#5599ff', 'background-color:#5599ff', '', ''])

                f.write(htmlcode)

        f.close()


    def HTML_Write_iperf(self, count, test_case, result, test_detail):
        print self.html_file
        f = open(self.html_file, 'a')

        table_data = [
            [count, test_case, result, test_detail]
        ]

        if "pass" in result.lower():
            htmlcode = HTML.table(table_data,
                                  col_width=['10%', '15%', '35%', '40%'],
                                  col_align=['center', 'left', 'center', 'left'],
                                  col_styles=['', '', 'background-color:lime', ''])
        else:
            htmlcode = HTML.table(table_data,
                                  col_width=['10%', '15%', '35%', '40%'],
                                  col_align=['center', 'left', 'center', 'left'],
                                  col_styles=['', '', 'background-color:Red', ''])

        f.write(htmlcode)

        f.close()


    def HTML_perf_write(self, ram_free, looper, css_mhz, test_detail):
        if self.DEBUG == 1:
            print self.html_file

        f = open(self.html_file, 'a')

        table_data = [
            [test_detail, "RAM Available = " + str(ram_free), "AP MHz Free = " + str(looper), "CSS MHz Free = " + str(css_mhz)]
        ]
        htmlcode = HTML.table(table_data,
                              col_width=['20%', '30%', '25%', '25%'],
                              col_align=['center', 'center', 'center', 'center'],
                              col_styles=['background-color:yellow', 'background-color:yellow', 'background-color:yellow', 'background-color:yellow'])

        f.write(htmlcode)

        f.close()


    def HTML_Write_Boot_Result(self, count, boot_result, dhcp_result):
        if self.DEBUG == 1:
            print self.html_file
        f = open(self.html_file, 'a')

        HTML_COLORS = ['Black', 'Green', 'Silver', 'Lime', 'Gray', 'Olive', 'White',
                       'Orange', 'Navy', 'Red', 'Blue', 'Purple', 'Teal', 'Fuchsia', 'Aqua']

        table_data = [
            [count, self.chipset, boot_result, dhcp_result]
        ]

        if "pass" in dhcp_result.lower() or "success" in  dhcp_result.lower():
            htmlcode = HTML.table(table_data,
                                  col_width=['10%', '15%', '35%', '40%'],
                                  col_align=['center', 'center', 'center', 'center'],
                                  col_styles=['', '', 'background-color:lime', 'background-color:lime'])
        else:
            htmlcode = HTML.table(table_data,
                                  col_width=['10%', '15%', '35%', '40%'],
                                  col_align=['center', 'center', 'center', 'center'],
                                  col_styles=['', '', 'background-color:Red', 'background-color:Red'])

        f.write(htmlcode)

        f.close()


    def HTML_Write_USB(self, test_case_num):
        if self.DEBUG == 1:
            print "##############%s : USB Call ##############" % test_case_num


    def HTML_Write_correction(self):
        if self.DEBUG == 1:
            print self.html_file

        f = open(self.html_file, 'a')

        table_data = [
            ["####################### Going for board correction ####################### "]
        ]

        htmlcode = HTML.table(table_data,
                              col_width=['100%'],
                              col_align=['center'],
                              col_styles=['background-color:red'])

        f.write(htmlcode)

        f.close()


    def HTML_Write_invalid_case(self, test_no, test, codec, ptime, features, fail_num):
        if self.DEBUG == 1:
            print self.html_file

        f = open(self.html_file, 'a')

        if fail_num == 1:
            table_data = [
                ["####################### Invalid test case(s) found in suite ####################### "]
            ]

            htmlcode = HTML.table(table_data,
                                  col_width=['100%'],
                                  col_align=['center'],
                                  col_styles=['background-color:red'])

            f.write(htmlcode)

        table_data = [
                        [test_no, test, codec, ptime, features, "This particular test is not valid on DVF" + str(self.chipset)]
                     ]

        htmlcode = HTML.table(table_data,
                col_width=['5%','11%', '5%', '5%','9%','65%'],
                col_align=['center','center','center','center','center', 'center'],
                col_styles=['','','','','','background-color:red'])

        f.write(htmlcode)

        f.close()


    def HTML_Write_Default(self, test_no, test, result):
        if self.DEBUG == 1:
            print "##############HTML Write Default for %s ##############" % test
        print self.html_file

        f = open(self.html_file, 'a')

        table_data = [
                        [test_no, test, result]
                     ]

        if "pass" in result.lower():
            htmlcode = HTML.table(table_data,
                    col_width=['5%','70%', '25%'],
                    col_align=['center','center','center'],
                    col_styles=['','','background-color:green'])
        else:
            htmlcode = HTML.table(table_data,
                    col_width=['5%','70%', '25%'],
                    col_align=['center','center','center'],
                    col_styles=['','','background-color:red'])

        f.write(htmlcode)

        f.close()


    def HTML_Write_Error(self, reason):
        if self.DEBUG == 1:
            print "##############HTML Write Default for Error ##############"
            print self.html_file

        f = open(self.html_file, 'a')
        table_data = [
                ["#######################" + str(reason) + "####################### "]
            ]

        htmlcode = HTML.table(table_data,
                              col_width=['100%'],
                              col_align=['center'],
                              col_styles=['background-color:red'])

        f.write(htmlcode)

        f.close()


    def HTML_Creat_incoming(self):
        f = open(self.html_file, 'a')
        print >> f,"<div align='Left'>"
        print >> f,"<table border='2' cellpadding='2' cellspacing='2' width='100%'>"
        print >> f,"<tr>"
        print >> f,'<th bgcolor="Silver"><font size="3">Incoming call</font></th>'
        f.close()


    def HTML_Creat_Outgoing_Call_HR(self):
        f = open(self.html_file, 'a')
        print >> f,"<div align='Left'>"
        print >> f,"<table border='2' cellpadding='2' cellspacing='2' width='100%'>"
        print >> f,"<tr>"
        print >> f,'<th bgcolor="Silver"><font size="3">Outgoing call Hold Resume</font></th>'
        f.close()


    def HTML_Creat_Incoming_Call_HR(self):
        f = open(self.html_file, 'a')
        print >> f,"<div align='Left'>"
        print >> f,"<table border='2' cellpadding='2' cellspacing='2' width='100%'>"
        print >> f,"<tr>"
        print >> f,'<th bgcolor="Silver"><font size="3">Incoming call Hold Resume</font></th>'
        f.close()


    def HTML_Creat_outgoing(self):
        f = open(self.html_file, 'a')
        print >> f,"<div align='Left'>"
        print >> f,"<table border='2' cellpadding='2' cellspacing='2' width='100%'>"
        print >> f,"<tr>"
        print >> f,'<th bgcolor="Silver"><font size="3">Outgoing call</font></th>'
        f.close()


    def HTML_Creat_Incoming_Call_CH(self):
        f = open(self.html_file, 'a')
        print >> f,"<div align='Left'>"
        print >> f,"<table border='2' cellpadding='2' cellspacing='2' width='100%'>"
        print >> f,"<tr>"
        print >> f,'<th bgcolor="Silver"><font size="3">Conference test CH_TEST</font></th>'
        f.close()


    def HTML_SEP(self):
        f = open(self.html_file, 'a')
        print >> f,"<div align='Left'>"
        print >> f,"<table border='2' cellpadding='2' cellspacing='2' width='100%'>"
        print >> f,"<tr>"
        htmlcode = HTML.table(" ", col_width=['100%'], col_align=['center'], col_styles=[''])
        f.write(htmlcode)
        f.close()



if __name__ == '__main__':
    print "Capturing...."
