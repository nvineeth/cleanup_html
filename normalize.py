import os
import sys
import re

TEST = 0

DOUBLE_SPACE_TAGS_START=[]
SINGLE_SPACE_TAGS_START=['html', 'head', 'body','br','div' ]
DOUBLE_SPACE_TAGS_END=['h1','h2','h3','h4','h5','p','div','html', 'head', 'body']
SINGLE_SPACE_TAGS_END=['style','link','br','table','td','tr','title']


def do_op(html):
    html_replaced = html
    html_replaced = re.sub('\s+',' ', html_replaced)

    html_replaced = html_replaced.replace('<!DOCTYPE html> ','<!DOCTYPE html>\n')
    html_replaced = html_replaced.replace('<!--','\n<!--')
    html_replaced = html_replaced.replace('--> ','-->\n')
    html_replaced = html_replaced.replace(' <link ','\n <link ')
    html_replaced = html_replaced.replace(' <title>','\n <title>')

    for t in DOUBLE_SPACE_TAGS_START:
        tag = '<%s>'%t
        html_replaced= html_replaced.replace( tag, tag+'\n\n')

    for t in SINGLE_SPACE_TAGS_START:
        tag = '<%s>'%t
        html_replaced= html_replaced.replace( tag, tag+'\n')
    for t in DOUBLE_SPACE_TAGS_END:
        tag = '</%s>'%t
        html_replaced= html_replaced.replace( tag, tag+'\n\n')

    for t in SINGLE_SPACE_TAGS_END:
        tag = '</%s>'%t
        html_replaced= html_replaced.replace( tag, tag+'\n')

    html_replaced = re.sub(r'\n{3,}',r'\n\n', html_replaced)

    if html_replaced != html:
        return html_replaced
    return None


for root, dirs, files in os.walk(sys.argv[1]):
    for f in files:
        if False == f.endswith('.htm'):
           continue 
        path = os.path.join(root, f)
        fp = open(path)
        html = fp.read();
        fp.close()

        html_rep = do_op(html)

        if html_rep != None:
            print('writing %s' % path)
            if TEST==1: continue
            fp = open(path, 'w')
            fp.write(html_rep)
            fp.close()

