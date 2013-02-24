import os
import sys
import re

TEST = 1

def do_op(html):
    html_replaced = html
    html_replaced = re.sub('\s*<br>\s*(&nbsp;)*\s*</p>','</p>', html_replaced)
    #html_replaced = re.sub('(([^;])&nbsp;([^&]))',' ', html_replaced)
    #html_replaced = html_replaced.replace('<p></p>','')
    if html_replaced != html:
        return html_replaced
    return None

def do_op_todo_1(html):
    html_replaced = html

    html_replaced = re.sub('<h2>.*<a id', '', html_replaced)

    if html_replaced != html:
        return html_replaced
    return None

def do_op_todo_2(html):
    html_replaced = html

    html_replaced = re.sub('\n\s+\n', '\n\n', html_replaced)

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



def do_op_1(html):
    html_replaced = html

    while True:
        matches = re.findall('<p class="right">((.*?)</p>\s*<p class="right">)\s*[^<]', html_replaced )
        print( matches )
        if len(matches)==0:
            break
        for match in matches:
            html_replaced = html_replaced.replace( match[0], match[1] + '<br>' )

    while True:
        matches = re.findall('(<br>(.))', html_replaced )
        #print( matches )
        if len(matches)==0:
            break
        for match in matches:
            html_replaced = html_replaced.replace( match[0], '<br>' + '\n' + match[1] )

    if html_replaced != html:
        return html_replaced
    return None
