#coding=utf8
#parser.py:析取html(自动识别，转换为utf8编码),获取文本串
# Usage:
# from mypack.uitl.htmlproc.parser import Parser
# pr = Parser()
# if pr.parser( url ):
#      pr.get_text():获取一个上的文本信息
from urllib import FancyURLopener
import sys
import re
from BeautifulSoup import BeautifulSoup,NavigableString,Comment
import chardet
#from crawl import crawl_url

class MyOpener(FancyURLopener):
     version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'

class Parser:
     def __init__(self):
          self.html = ''
          self.url = ''
          
     def parse( self,url ):
          self.url = url
          try:
               # 编码检测与转换
               myopener = MyOpener()
               #self.html = crawl_url( url ) #晕，速度反而比urllib直接爬更慢!
               self.html = myopener.open(url).read()
               if not self.html:                    
                    print "[W]cannot read the page:%s" % url
                    return False
               else:
                    return True
          except IOError:
               print "[W]cannot open url:%s" % url
               return False

     def get_html(self):
          return self.html
     
     def _load(self):
          assert( self.html )
          '''load html to BeautifulSoup and auto detect charset.'''
          encoding = chardet.detect(self.html)['encoding'] 
          
          if not encoding:
               print "[W]cannot detect encoding of the page!"
               return False
          self.html = self.html.decode(encoding,'ignore').encode('utf-8','ignore')
          self.soup = BeautifulSoup( self.html )
          if not self.soup.html:
               print "[W]Not a html:%s" % self.url
               return False
          else:
               return True
     
     def _clear(self):
        # 去除comment
        comments = self.soup.findAll(text=lambda text:isinstance(text, Comment))
        [comment.extract() for comment in comments]
          # 去除style,script
        trivals = self.soup.findAll(['script','style'])
        [trival.extract() for trival in trivals]
        # 清楚display:none或文字或font-size: 0px
        trivals = self.soup.findAll(style=re.compile(".*((display\s*:\s*none)|(font-size\s*:\s*0)).*"))
        [trival.extract() for trival in trivals]

     # 返回一个网页内所有的文本,unicode
     def get_text( self ):
          doc = ''
          if self._load():
               self._clear()
               ns_list = self.soup.html.findAll(text=True)
               for ns in ns_list:
                    ns_str = ns.string.strip()
                    if ns_str and not re.match(ur"^(\s|&nbsp;)*$",ns_str):
                         doc += ' %s' % ns_str
                         pass
                    pass
          return doc 

if __name__ == "__main__":
     url = 'http://tech.sina.com.cn/'
     print "parser page:%s" % url
     pr = Parser()
     if pr.parse( url ):
          #print pr.get_html()
          print pr.get_text().encode('utf-8')
