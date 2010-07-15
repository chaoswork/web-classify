#coding=utf8
#extract.py 对外接口
# Usage:see main
# from mypack.web_content_extract.extract import Extractor
from scrape import Scraper

class Extractor:
    def __init__(self,url):
        sr = Scraper( url )
        (self.flag,self.title,self.content,self.content_with_format,self.imgs,self.confidence,self.detail) = sr.get_content()

    def is_content_page(self):
        return self.flag
    
    def get_title(self):
        return self.title
    
    def get_content(self):
        return self.content
    
    def get_content_with_format(self):
        return self.content_with_format
    
    def get_images(self):
        return self.imgs
    
    def get_confidence(self):
        return self.confidence
    
    def get_detail(self):
        return self.detail
    
if __name__=='__main__':
    url='http://hi.baidu.com/kissdev/blog/item/ec42e1cfca0cbc36f9dc6132.htm'
    extr = Extractor( url )
    print extr.get_content()
