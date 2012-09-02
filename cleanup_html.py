#Script to clean up html files..experimental
from html.parser import HTMLParser
import sys, traceback
import os
import re
import logging
import shutil
import glob
import urllib
import urllib.parse
from FootnoteParser import *
from ParsingRules import * 

def get_contents_href(html_file, href_link):
    "Opens the _frame.htm file and returns the contents file."
    href_path = os.path.normpath(os.path.join( os.path.split(html_file)[0], href_link))
    href_file = open(href_path)
    href_contents = href_file.read()
    m = re.search('frame SRC=["]*((\w|-)+.htm)["]* NAME=["]*side["]*',href_contents, re.I)
    if m is not None:
        new_link = href_link.replace( os.path.split(href_path)[-1], m.group(1)) # os.path.join( os.path.split(href_link)[0], m.group(1) )
        print('    **Using %s for %s' % (new_link, href_link) )
        return new_link
    print( 'cannot find replacement for %s' % href_link ) # stop processing and warn.
    sys.exit(-3)
    return href_link # could not fine contents.

class CWHTMLParser(HTMLParser):
    "complete works html parser, combines the files to produce a single one, ideal for amazon book reader"
    
    def __init__(self, html_file ):
        HTMLParser.__init__(self)
        self.content = ''
        self.html_file = html_file
        self.ignore_data = 0
        self.footnotes = []
        self.nav_added = 0

    def handle_startendtag( self, tag, attrs ):
        strattrs = "".join([' %s="%s"' % (key, value) for key, value in attrs])
        self.content += '<%s %s />' % ( tag, strattrs )

    def process_footnote(self, attrs):
        for (name,value) in attrs:
            if name=='onclick':
                match_obj = re.search('[a-zA-Z0-9_]+.htm',value)
                if match_obj == None:
                    logging.critical('footnote htm not found')
                    return
                footnote_file = match_obj.group(0)

        footnote_file_path = os.path.split(self.html_file)[0]
        footnote_file_path = os.path.join( footnote_file_path, footnote_file)
        foonote_parser = FootnoteHTMLParser(footnote_file_path)
        (fnote,anchor) = foonote_parser.process_html( )
        if len(fnote) == 0: return
        anchor = 'fn%d'%(len(self.footnotes)+1) # use a shorter anchor
        self.footnotes.append( (fnote, anchor) )
        self.content += '<a id="%s"></a>' % (anchor+'_1')
        self.content += '<a class="fnote" href="#%s">%d' % (anchor, len(self.footnotes) )
        self.ignore_data = 1

    
    def handle_starttag(self, tag, attrs):
        #logging.debug("{ %s " % tag)

        if tag in IGNORE_TAGS:
            self.ignore_data = 1;
            return;
        
        # skip unsupported html tags by amazon DTP
        if tag not in DTP_SUPPORTED_ATTRIBS:
            logging.debug(" ignoring %s " % tag );
            return;
        
        onMouseOver = 0
        onMouseOut = 0
        href_present = 0
        page_info = ''
        if tag == 'a':
            for (name,value) in attrs:
                if name=='href' and value=='#blank':
                    self.process_footnote(attrs)
                    return
                # page no js processing
                
                if name=='onmouseover':
                    onMouseOver = 1
                    page_info=value.replace('window.status','').replace('=','').replace(';return true','')
                if name=='onmouseout': onMouseOut = 1
                if name=='href': href_present = 1
        # fix the imporperly placed a tag, which is closed by a p
        if onMouseOver==1 and onMouseOut==1 and href_present==0:
            self.content += '<!--' + page_info + '-->'
            return
            
                   
        # remove the attributes that are not necessary
        attrs_ori = attrs
        attrs_filtered = []
        htmlClasses = ''
        for (attrib,value) in attrs:
            if attrib in DTP_SUPPORTED_ATTRIBS[tag]:
                # preprocess href of a tag, which point to _frame pages
                if tag=='a' and attrib=='href':
                    if value.endswith('_frame.htm'):
                        value = get_contents_href(self.html_file, value)
                    elif value.endswith('complete_works_contents.htm'):
                        value = value.replace('complete_works_contents.htm','complete_works.htm')
                attrs_filtered.append( (attrib,value) )
            # retain small class for p tags, they are the nav on top
            elif tag=='p' and attrib=='class' and value.lower()=='small' and self.nav_added==0: 
                htmlClasses += ' nav '
                self.nav_added = 1
            elif attrib=='style' and value.find('margin')!=-1 and tag!='table':
                htmlClasses += ' poem '
            elif attrib=='align' and tag != 'img': #w3c validator
                if value=='center' or value=='centre':
                    htmlClasses += ' center '
                elif value=='right':
                    htmlClasses += ' right '
                else:
                    pass

            
        if len(htmlClasses.strip()) : 
            htmlClasses = htmlClasses.replace('  ',' ')
            attrs_filtered.append( ('class', htmlClasses.strip()) )

        attrs = attrs_filtered

        # append the attributes and tag to the content.
        strattrs = "".join([' %s="%s"' % (name, value) for name, value in attrs])
        if len(strattrs):
            self.content += '<%s%s>' % ( tag, strattrs )
        else:
            self.content += '<%s>' %  tag

    def handle_endtag(self, tag):

        if tag in IGNORE_TAGS:
            self.ignore_data = 0;
            return;

        if tag == 'a':
            self.ignore_data = 0


        # skip unsupported html tags by amazon DTP
        if tag not in DTP_SUPPORTED_ATTRIBS:
            return

        # Insert the footnote
        if tag == 'body' and len(self.footnotes):
            self.content += '<ol class="fnote">\n'
            for (f,a) in self.footnotes:
                self.content += '<li>' + ('<a id="%s"></a>' % a) + ('<a href="#%s">^' % (a+'_1') ) + '</a>' + f  + '</li>\n'
            self.content += '</ol>\n'

        self.content += '</%s>' % tag;

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

    def post_process_html(self,str):
        str = str.replace('start -->','>')
        str = re.sub(">\s*<<\s*<", ' class="arrow"> &larr; <', str);
        str = re.sub(">\s*>>\s*", ' class="arrow"> &rarr;', str);
        str = re.sub(">\s*&lt;\s*&lt;\s*<", ' class="arrow"> &larr; <', str);
        str = re.sub(">\s*&gt;\s*&gt;\s*", ' class="arrow"> &rarr;', str);


        #rm noindex.
        str = str.replace('<meta content="NOINDEX">','')

        #w3c validator errors.
        str = str.replace("&#151;", "&mdash;")
        str = str.replace("&#133;", "&hellip;")

        # rm extra line breaks b/w paras.
        str = re.sub("p>\s*<br>\s*<p", "p>\n<p", str);

        # make the first occurances of b to h2.
        #str = str.replace('<b>','<h2>', 1)
        #str = str.replace('</b>','</h2>', 1)

        str = re.sub('<p( class="\w+")*>\s*<h2>','<h2>', str)
        str = re.sub('</h2>\s*</p>','</h2>', str)
        if str.find('<head') == -1:
            str = str.replace('<html>', '<html>\n<head></head>')
            print('|---no head in this file.')
        #Add the style if absent.
        if str.find('<link')==-1 and str.find('rel="stylesheet"')==-1:
            main_css_path = ('../' * self.html_file.count('\\'))+'main.css'
            str = str.replace('<head>', \
                    '<head>\n<link rel="stylesheet" type="text/css" href="%s">' % main_css_path)
            
            
        # manually add meta tag.
        if str.find('<meta') == -1:
            str = str.replace('<head>','<head>\n<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">')
            
        # replace the css with main css
        for (a,b) in CSS_REPLACEMENTS:
            str = str.replace( a, b)
        
        return '<!DOCTYPE html>\n' + str;

    def process_html(self):
        try:
            file = open( self.html_file )
        except :
            traceback.print_exc(file=sys.stdout)
            logging.warning(" Warning : Unresolved link to "+ self.html_file)
            return ''
        html_contents = file.read()
        file.close()

        html_contents = self.pre_process_html(html_contents)

        try:
            self.feed( html_contents )
        except Exception as err:
            msg = 'Error while parsing file %s : %s ' % (self.html_file, str(err))
            traceback.print_exc(file=sys.stdout)
            sys.stderr.write(msg+'\n')
            logging.critical(msg)
            sys.exit(-2)
        
        return  self.post_process_html(self.content)

def copy_files( src, dst, filter):
    files = glob.glob(os.path.join(src, filter))
    for f in files:
        shutil.copy( f, os.path.join(dst,os.path.split(f)[-1]) )

def main():
    logging.basicConfig( filename=sys.argv[0]+'.log', level=logging.DEBUG )
    # the main code goes here
    if len( sys.argv ) != 3:
        print( " usage : %s <html_dir> <output dir>" % sys.argv[0]);
        sys.exit(-1)

    out_dir = sys.argv[2]
    if os.path.exists(out_dir)==False:
        logging.debug('creating dir %s' % out_dir )
        os.makedirs( out_dir )

    if ( False==os.path.isdir(out_dir) ):
        print( "%s not a directory" % sys.argv[2] )
        sys.exit(-1)

    for root, dirs, files in os.walk(sys.argv[1]):
        #also create the output dir
        out_dir = os.path.normpath(root.replace(sys.argv[1],sys.argv[2]+'\\',1))
        try:
            os.makedirs(out_dir)
        except:
            print( 'outdir %s already exists' % out_dir)

        #process the html files in this dir
        htm_files = glob.glob(os.path.join(root, '*.htm'))
        for htm_file in htm_files:
            if os.path.isfile(htm_file) == False: 
                print( htm_file + " is not a file : ERROR")
                continue
            if ( re.search('_[a-zA-Z].htm$',htm_file) != None and \
                    os.path.exists(re.sub('_[a-zA-Z].htm$','.htm',htm_file)) ) or \
                    htm_file.find('picosearch.htm')!=-1 or htm_file.endswith('_frame.htm'):
                print('     avoid %s' % htm_file )
                continue
            print( "Processing %s ..." % htm_file )
            out_filename = os.path.normpath( os.path.join( out_dir, os.path.split(htm_file)[-1] ) )
            out_fp = open( out_filename,'w')
            cwparser = CWHTMLParser( htm_file )
            out_fp.write( cwparser.process_html() )
            cwparser.reset()
            cwparser.close()
            out_fp.close()

        copy_files( root, out_dir, '*.jpg')
        copy_files( root, out_dir, '*.pdf')

if __name__ == "__main__":
    main()
        
