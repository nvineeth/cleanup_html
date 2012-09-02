import sys, traceback
import os
import re
import logging
from html.parser import HTMLParser
from ParsingRules import *

class FootnoteHTMLParser(HTMLParser):
    """ ignores the tags, and puts the text content,
        so that it can be aggregated as a footnote easily.
        Also preservers the img"""
    def __init__(self, html_file ):
        HTMLParser.__init__(self)
        self.content = ''
        self.html_file = html_file
        self.ignore_data = 0

        
    def handle_starttag(self, tag, attrs):
        #logging.debug("{ %s " % tag)
        if tag == 'title':
            self.ignore_data = 1
        if tag == 'br':
            self.content += '<%s/>' % tag;
        if tag == 'img':
            attrs_filtered = []
            for (attrib,value) in attrs:
                if attrib in DTP_SUPPORTED_ATTRIBS[tag]:
                    attrs_filtered.append( (attrib,value) )
            strattrs = "".join([' %s="%s"' % (name, value) for name, value in attrs])
            self.content += '<img %s>' % strattrs

    def handle_endtag(self, tag):
        if tag == 'title':
            self.ignore_data = 0

    def handle_data(self, data):
        if self.ignore_data == 1:
            return;
        self.content += data;

    def handle_comment(self, data):
        #print ( 'comment: ' + data )
        self.content += '<!--' + data + '-->'

    def handle_charref(self, name):
        #print ('charref : ', name)
        self.content += '&#%s;' % name

    def handle_entityref(self, name):
        self.content += '&%s;' % name

    def pre_process_html(self, str):
        str = str.replace('start -->','>')
        return str

    def process_html(self):
        try:
            file = open( self.html_file )
        except :
            traceback.print_exc(file=sys.stdout)
            logging.warning(" Warning : Unresolved link to "+ self.html_file)
            return '',''
        html_contents = file.read()
        file.close()

        #rename the file
        #shutil.move(self.html_file, self.html_file+'~')

        html_contents = self.pre_process_html(html_contents)

        try:
            self.feed( html_contents )
        except Exception as err:
            msg = 'Error while parsing file %s : %s ' % (self.html_file, str(err))
            traceback.print_exc(file=sys.stdout)
            sys.stderr.write(msg+'\n')
            logging.critical(msg)
            sys.exit(-4)

        anchor = os.path.split(self.html_file)[-1].split('.')[0]

        self.content = self.content.strip()
        return self.content, anchor