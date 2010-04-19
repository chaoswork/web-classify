#coding=utf8
#crawl.py:
#get_text():获取一个上的文本信息
from urllib import FancyURLopener
import sys
import re
from BeautifulSoup import BeautifulSoup,NavigableString,Comment
import chardet

class MyOpener(FancyURLopener):
     version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'

class Parser:
     def parse( self,url ):
          try:
               # 编码检测与转换
               myopener = MyOpener()
               html = myopener.open(url).read()
               encoding = chardet.detect(html)['encoding'] 
               
               if not encoding:
                    print "[W]cannot detect encoding of the page!"
                    return False
               html = html.decode(encoding,'ignore').encode('utf-8','ignore')
               self.soup = BeautifulSoup( html )
               if not self.soup.html:
                    print "[W]Not a html:%s" % url
                    return False
               else:
                    return True
          except IOError:
               print "[W]cannot open url:%s" % url
               return False

     def __clear(self):
        # 去除comment
        comments = self.soup.findAll(text=lambda text:isinstance(text, Comment))
        [comment.extract() for comment in comments]
          # 去除style,script
        trivals = self.soup.findAll(['script','style'])
        [trival.extract() for trival in trivals]
        # 清楚display:none或文字或font-size: 0px
        trivals = self.soup.findAll(style=re.compile(".*((display\s*:\s*none)|(font-size\s*:\s*0)).*"))
        [trival.extract() for trival in trivals]

     # 返回一个网页内所有的文本
     def get_text( self ):
          self.__clear()
          doc = ''
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
          print pr.get_text().encode('utf-8')
