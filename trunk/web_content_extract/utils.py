#coding=utf-8
import re
from math import sqrt

stop_words = ['i', 'a', 'about','and', 'an', 'are', 'as', 'at', 'be', 'by', 'com', 'de', 'en', 'for', 'from', 'how', 'in', 'is', 'it', 'la', 'of', 'on', 'or', 'that', 'the', 'this', 'to', 'was', 'what', 'when', 'where', 'who', 'will', 'with', 'und', 'the', 'www']
#stop_words = [unicode(w) for w in stop_words]

# 2-gram Chinese words segment, keep Connected English letters as a word
# return:
#      words [w1,w2,...]
def title_split( title ):
    if isinstance(title, str):
        title = title.decode('utf8')
        
    stop_words = ['http','www']
    # split
    regex = re.compile(ur"(?x) (?: [\w-]{2,} | [\u4e00-\u9fa5]{2} )")
    wds = regex.findall(title)
    
    # filter stop words
    wds = [w for w in wds if w not in stop_words]
    
    return wds

#html特殊字符转换
def html_char_transform( s ):
    s=s.replace('&nbsp;',' ')
    s=s.replace('&quot;','"')
    s=s.replace('&lt;','<')
    s=s.replace('&gt;','>')
    s=s.replace('&#124;','|')
    s=s.replace('&ldquo;','"')
    s=s.replace('&rdquo;','"')
    s=re.sub('&#?(\w)+;',' ',s)
    return s

# 将相对路径的img转换成绝对路径,url为网页的网址
def relative2absolute( url,path ):
    path = path.replace('//','/')
    if not url.startswith('http'):
        return ''
    # 截取路径尾部有效的字段
    match = re.search('[^./]',path)
    file = path[match.start():]
    
    if path.startswith('/'):
        pos = url.find('/',7)
    elif path.startswith('../'):
        n = path.count('../')
        pos = url.rfind('/',0,len(url))
        for i in range(n):
            pos = url.rfind('/',0,pos)
    else:
        pos = url.rfind('/')
    return url[:pos+1] + file

#求均值
def mean( li ):
    if len(li) == 0:
        return 0
    return float(sum(li))/len(li)

#求方差
def var( li ):
    m = mean(li)
    temp = [ (x-m)*(x-m) for x in li ]
    return sqrt( sum(temp)/len(li) )

class Myerror(Exception):
     def __init__(self, value):
         self.value = value
     def __str__(self):
         return repr(self.value)
