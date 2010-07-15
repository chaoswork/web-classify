#coding=utf-8
import re
from urllib import FancyURLopener
from mypack.util.htmlproc.BeautifulSoup import BeautifulSoup,NavigableString,Comment
from utils import title_split,Myerror,html_char_transform
from config import *
from text import Text
from mypack.util.htmlproc import chardet

class MyOpener(FancyURLopener):
   version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'
   
# 网页预处理员:根据url提取网页，html清理，生成文本串
class Parser:
    def __init__(self,url):
        self.ns_li = []
        self.ns_len = 0         # 所有的文本块长度
                
        try:
            # 编码检测与转换
            myopener = MyOpener()
            html = myopener.open(url).read()
            #html = urlopen(url).read()
            encoding = chardet.detect(html)['encoding'] 
            
            if not encoding:
                raise Myerror("Sorry,cannot recognize encoding of the page!")
            html = html.decode(encoding,'ignore').encode('utf-8','ignore')
            # BeautifulSoup不能析取，alt为中文
            html = re.sub('alt=(("[^"]*")|(\'[^\']*\')|([^"\'\s]+))','',html)
            self.soup = BeautifulSoup(html)
            self.__clear()
        except IOError:
            raise Myerror("Sorry,cannot open this page!")
            print "Faild to open:"+url

    def __clear(self):
        # 去除comment
        comments = self.soup.findAll(text=lambda text:isinstance(text, Comment))
        [comment.extract() for comment in comments]
          # 去除style,script
        trivals = self.soup.findAll(['script','style'])
        [trival.extract() for trival in trivals]
        # 清楚display:none或文字或font-size: 0px
        # ToDo style="font-size: 0px; 
        trivals = self.soup.findAll(style=re.compile(".*((display\s*:\s*none)|(font-size\s*:\s*0)).*"))
        [trival.extract() for trival in trivals]

    # 获取title，取正文中与<title>最匹配的
    def get_title(self):
        try:
            t = self.soup.title
            tag_t = t.string.strip()
            
            title = None
            # 从正文中寻找title
            for ns in self.ns_li:
                s = ns.string.strip()
                if s!='' and tag_t.find( s )!=-1 :
                   if title==None or 3<len(s)-len(title.string):
                      title = ns
            if not title:
               title = t
        except AttributeError:
            raise Myerror("Sorry,cannot access this page for host limitation!")
          #对title进行分词
          #tws = title_split( title )
        #return html_char_transform(title)
        return title
    
    def text_len(self):
        return self.ns_len    
    # 抽取基本文本块
    def ns(self):
        cur = self.soup.body
        ns_list = []
        offset = 0              # 记录与上一个NavigableString之间的Tag距离
        while cur.next:
            if isinstance(cur,NavigableString):
                # 过滤单纯空格
                if not re.match(ur"^(\s|&nbsp;)*$",cur.string):                    
                    ns_list.append( {'node':cur,'offset':offset} )
                    self.ns_li.append( cur )
                    self.ns_len += len(cur.string) # 计算总的ns串长度
                    offset = 0
            #elif cur.name not in ['br','a','img','span','font','b','strong','li','tr','td']:
            elif cur.name.lower() in BLOCK_TAGS:
                offset +=1
            cur = cur.next
        #debug
        # print "DEBUG"+100*"#"
        # for ns in ns_list:
        #     print ns['node'].string
        return ns_list
