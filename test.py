# coding=utf-8
import os
import sys
import re

roman_re = re.compile('^[IVXLCDM]{2,}$')
caps_re = re.compile(u'[a-zA-Z\u00C0-\u00DD]{2,}')

def do_op(html):
    html_replaced = html

    matches = caps_re.findall( html_replaced )
    print( matches )
    for match in matches:
        # avoid roman
        if roman_re.match(match) != None or match in ['DOCTYPE', 'PS', 'PPS']: 
            continue
        print('%s -> %s'% (match, match.title()))
        #html_replaced = html_replaced.replace( match[0], match[0].title() )

    if html_replaced != html:
        return html_replaced
    return None


html = """
<h2>XXIV</h2></p>

<p class="center"><i>To the Hale
Sisters</i></p>
<p class="right">SWAMPSCOTT, <br>
<i>26th July, 1894</i>.</p>
MÂRÂJ
"""

do_op(html)
