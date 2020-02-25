


########################################################################################################################
########################################################################################################################
## File              :: vaca_htmldef.py
## Description       :: VoIP Automation Common API : HTML report format definition.
## Developer         :: Guruprasad K S
## Version           :: v1.0
## Release Date      :: 13/03/2010
## Changes made      :: Initial version.
## Changes made Date :: 11/04/2019
## Changes made by   :: Sreekanth S
########################################################################################################################
########################################################################################################################



TABLE_STYLE_THINBORDER = "border: 1px solid #000000;"



class TableCell (object):
    def __init__(self, text="", bgcolor=None, header=False, width=None,
                align=None, char=None, charoff=None, valign=None, style=None,
                attribs=None):
        self.text    = text
        self.bgcolor = bgcolor
        self.header  = header
        self.width   = width
        self.align   = align
        self.char    = char
        self.charoff = charoff
        self.valign  = valign
        self.style   = style
        self.attribs = attribs
        if attribs==None:
            self.attribs = {}


    def __str__(self):
        attribs_str = ""
        if self.bgcolor: self.attribs['bgcolor'] = self.bgcolor
        if self.width:   self.attribs['width']   = self.width
        if self.align:   self.attribs['align']   = self.align
        if self.char:    self.attribs['char']    = self.char
        if self.charoff: self.attribs['charoff'] = self.charoff
        if self.valign:  self.attribs['valign']  = self.valign
        if self.style:   self.attribs['style']   = self.style
        for attr in self.attribs:
            attribs_str += ' %s="%s"' % (attr, self.attribs[attr])
        if self.text:
            text = str(self.text)
        else:
            text = '&nbsp;'
        if self.header:
            return '  <TH%s>%s</TH>\n' % (attribs_str, text)
        else:
            return '  <TD%s>%s</TD>\n' % (attribs_str, text)

#-------------------------------------------------------------------------------


class TableRow (object):
    def __init__(self, cells=None, bgcolor=None, header=False, attribs=None,
                col_align=None, col_valign=None, col_char=None,
                col_charoff=None, col_styles=None):
        self.bgcolor     = bgcolor
        self.cells       = cells
        self.header      = header
        self.col_align   = col_align
        self.col_valign  = col_valign
        self.col_char    = col_char
        self.col_charoff = col_charoff
        self.col_styles  = col_styles
        self.attribs     = attribs
        if attribs==None:
            self.attribs = {}


    def __str__(self):
        attribs_str = ""
        if self.bgcolor: self.attribs['bgcolor'] = self.bgcolor
        for attr in self.attribs:
            attribs_str += ' %s="%s"' % (attr, self.attribs[attr])
        result = ' <TR%s>\n' % attribs_str
        for cell in self.cells:
            col = self.cells.index(cell)   
            if not isinstance(cell, TableCell):
                cell = TableCell(cell, header=self.header)
            if self.col_align and cell.align==None:
                cell.align = self.col_align[col]
            if self.col_char and cell.char==None:
                cell.char = self.col_char[col]
            if self.col_charoff and cell.charoff==None:
                cell.charoff = self.col_charoff[col]
            if self.col_valign and cell.valign==None:
                cell.valign = self.col_valign[col]
            if self.col_styles and cell.style==None:
                cell.style = self.col_styles[col]
            result += str(cell)
        result += ' </TR>\n'
        return result

#-------------------------------------------------------------------------------


class Table (object):
    def __init__(self, rows=None, border='1', style=None, width='100%',
                cellspacing=None, cellpadding=4, attribs=None, header_row=None,
                col_width=None, col_align=None, col_valign=None,
                col_char=None, col_charoff=None, col_styles=None):
        self.border = border
        self.style = style
        if style == None: self.style = TABLE_STYLE_THINBORDER
        self.width       = width
        self.cellspacing = cellspacing
        self.cellpadding = cellpadding
        self.header_row  = header_row
        self.rows        = rows
        if not rows: self.rows = []
        self.attribs     = attribs
        if not attribs: self.attribs = {}
        self.col_width   = col_width
        self.col_align   = col_align
        self.col_char    = col_char
        self.col_charoff = col_charoff
        self.col_valign  = col_valign
        self.col_styles  = col_styles


    def __str__(self):
        attribs_str = ""
        if self.border: self.attribs['border'] = self.border
        if self.style:  self.attribs['style'] = self.style
        if self.width:  self.attribs['width'] = self.width
        if self.cellspacing:  self.attribs['cellspacing'] = self.cellspacing
        if self.cellpadding:  self.attribs['cellpadding'] = self.cellpadding
        for attr in self.attribs:
            attribs_str += ' %s="%s"' % (attr, self.attribs[attr])
        result = '<TABLE%s>\n' % attribs_str
        if self.col_width:
            for width in self.col_width:
                result += '  <COL width="%s">\n' % width
        if self.header_row:
            if not isinstance(self.header_row, TableRow):
                result += str(TableRow(self.header_row, header=True))
            else:
                result += str(self.header_row)
        for row in self.rows:
            if not isinstance(row, TableRow):
                row = TableRow(row)
            if self.col_align and not row.col_align:
                row.col_align = self.col_align
            if self.col_char and not row.col_char:
                row.col_char = self.col_char
            if self.col_charoff and not row.col_charoff:
                row.col_charoff = self.col_charoff
            if self.col_valign and not row.col_valign:
                row.col_valign = self.col_valign
            if self.col_styles and not row.col_styles:
                row.col_styles = self.col_styles
            result += str(row)
        result += '</TABLE>'
        return result

#-------------------------------------------------------------------------------


class List (object):
    def __init__(self, lines=None, ordered=False, start=None, attribs=None):
        if lines:
            self.lines = lines
        else:
            self.lines = []
        self.ordered = ordered
        self.start = start
        if attribs:
            self.attribs = attribs
        else:
            self.attribs = {}


    def __str__(self):
        attribs_str = ""
        if self.start:  self.attribs['start'] = self.start
        for attr in self.attribs:
            attribs_str += ' %s="%s"' % (attr, self.attribs[attr])
        if self.ordered: tag = 'OL'
        else:            tag = 'UL'
        result = '<%s%s>\n' % (tag, attribs_str)
        for line in self.lines:
            result += ' <LI>%s\n' % str(line)
        result += '</%s>\n' % tag
        return result

#-------------------------------------------------------------------------------



def Link(text, url):
    return '<a href="%s">%s</a>' % (url, text)



def link(text, url):
    return '<a href="%s">%s</a>' % (url, text)



def table(*args, **kwargs):
    'return HTML code for a table as a string. See Table class for parameters.'
    return str(Table(*args, **kwargs))



def list(*args, **kwargs):
    'return HTML code for a list as a string. See List class for parameters.'
    return str(List(*args, **kwargs))


#=== MAIN =====================================================================

if __name__ == '__main__':
    f = open('test.html', 'w')

    t = Table()
    t.rows.append(TableRow(['A', 'B', 'C'], header=True))
    t.rows.append(TableRow(['D', 'E', 'F']))
    t.rows.append(('i', 'j', 'k'))
    f.write(str(t) + '<p>\n')
    print str(t)
    print '-'*79

    t2 = Table([
            ('1', '2'),
            ['3', '4']
        ], width='100%', header_row=('col1', 'col2'),
        col_width=('', '75%'))
    f.write(str(t2) + '<p>\n')
    print t2
    print '-'*79

    t2.rows.append(['5', '6'])
    t2.rows[1][1] = TableCell('new', bgcolor='red')
    t2.rows.append(TableRow(['7', '8'], attribs={'align': 'center'}))
    f.write(str(t2) + '<p>\n')
    print t2
    print '-'*79

    table_data = [
            ['Smith',       'John',         30,    4.5],
            ['Carpenter',   'Jack',         47,    7],
            ['Johnson',     'Paul',         62,    10.55],
        ]
    htmlcode = HTML.table(table_data,
        header_row = ['Last name',   'First name',   'Age', 'Score'],
        col_width=['', '20%', '10%', '10%'],
        col_align=['left', 'center', 'right', 'char'],
        col_styles=['font-size: large', '', 'font-size: small', 'background-color:yellow'])
    f.write(htmlcode + '<p>\n')
    print htmlcode
    print '-'*79

    def gen_table_squares(n):

        for x in range(1, n+1):
            yield (x, x*x)

    t = Table(rows=gen_table_squares(10), header_row=('x', 'square(x)'))
    f.write(str(t) + '<p>\n')

    print '-'*79
    l = List(['aaa', 'bbb', 'ccc'])
    f.write(str(l) + '<p>\n')
    l.ordered = True
    f.write(str(l) + '<p>\n')
    l.start=10
    f.write(str(l) + '<p>\n')

    f.close()
