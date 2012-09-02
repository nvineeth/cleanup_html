CSS_REPLACEMENTS = [ 
        ('vivekananda_biography.css', '../main.css'), 
        ('gospel.css', '../main.css'),
        ("reminiscences_of_sv.css", '../main.css'),
        ('vol_1.css', '../../main.css'),('vol_2.css', '../../main.css'),
        ('vol_3.css', '../../main.css'),('vol_4.css', '../../main.css'),
        ('vol_5.css', '../../main.css'),('vol_6.css', '../../main.css'),
        ('vol_7.css', '../../main.css'),('vol_8.css', '../../main.css'),
        ('vol_9.css', '../../main.css'),('appendices.css', '../../main.css')
        ]


DTP_SUPPORTED_ATTRIBS = {
        'a':[	'href', 'id', 'name' ],
        'b':['id'],
        'big':[],
        'blockquote':['id'],
        'body':	[],
        'br':['id'],
        'center':[],	
        'cite':[],
        'dd':[ 'id', 'title'],
        'del':[],
        'dfn':[],	
        'div':['__align',	'id', 'bgcolor'],
        'em': ['id', 'title'],
        #'font':['color','face','id','size'],
        'head':[],
        #'h1':[],
        'h2':[],'h3':[],'h4':[],'h5':[],'h6':[],
        'hr':['color', 'id', 'width'],
        'html':	[],
        'i':['class','id'],
        'img':[	'align','border','height','id','src','width'],
        'li':[	'class','id','title'],
        #'link': [ 'rel', 'type', 'href'],
        #meta has unnecessary stuff, so ignore and manuall add later.
        #'meta': [ 'http-equiv', 'content'],
        'ol':[ 'id'],
        'p':[	'__align','id','title'],
        's':[	'id','style','title'],
        'small':[	'id' ],
        #'span':[	'bgcolor','title'],
        'strike':[	'class','id'],
        'strong':	['class','id'],
        'table':[], 'tr':[], 'td':[],
        'title': [],
        'sub':	['id'],
        'sup':[	'class','id'],
        'u':[	'id'],
        'ul':[	'class','id']
        }

IGNORE_TAGS = ['style']
