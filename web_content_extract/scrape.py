#coding=utf-8
#import chardet
import sys,codecs
from mypack.util.htmlproc.BeautifulSoup import NavigableString
from judge import Judge
from block import Block
from recorder import Recorder
from partitioner import Partitioner
from parser import Parser
from utils import relative2absolute
from urllib import urlopen
from config import *

# html分析器(主类):执行流程,输出正文和图像
class Scraper:
    def __init__(self,url):
        self.url = url          # 要分析的url
        self.block_li = []      # 网页所包含的文本块列表
        self.title = ''
        #重置记录
        self.recorder = Recorder()
        self.recorder.reset()
        
    # 从正文前后和其中中提取图片，只取第一个
    # 只取图片大小足够大的
    def get_images(self,block):
        imgs = []
        
        # 设定image搜索起点
        if self.title != self.parser.soup.title:
            start = self.title
        else:
            # title不在正文中,向上扩展image搜索范围
            # 向下扩展image搜索范围
            start = block.text_list()[0]        
            while start.previous:
                start = start.previous
                if not isinstance(start,NavigableString) and start.name in BLOCK_TAGS:
                    break
                
        # 设定image搜索终点
        end = block.text_list()[-1]
        while end.next:
            end = end.next
            if not isinstance(end,NavigableString) and end.name in BLOCK_TAGS:
                break

        while start!=end:
            if not isinstance(start,NavigableString) and start.name=='img':
                imgs.append( start ) 
            start = start.next
        return self.filter_images( imgs )

    def filter_images( self,imgs ):
        srcs = []
        images = []
        for img in imgs:
            if img.has_key('src'):
                src = img['src']
                if not src.lower().startswith('http://'):
                    src = relative2absolute( self.url,src )
                    # 判断图片大小,太小不要
                try:
                    im = urlopen( src ).read()
                    if len(im)>MIN_IMG_SIZE:
                        srcs.append( src )
                        #img['src'] = src
                        images.append( img )
                except IOError:
                    pass
        return (srcs,images)
    # 如果图像出现在block中，则添加图像和图像p内的ns
    def insert_images(self,block,images):
        start = self.title
        end = block.text_list()[-1]
        behind_img = False
        #block.print_ns()

        i = 0                   # 记录block中文本编号
        while start!=end:
            if not isinstance(start,NavigableString) :
                if start.name=='img' and start in images:
                    src = start['src']
                    if not src.lower().startswith('http://'):
                        start['src'] = relative2absolute( self.url,src )
                    #print i,":",str(start),"[]"
                    block.insert( i,start ) 
                    #block.print_ns()
                    i += 1
                    behind_img = True
                elif start.name=='br':
                    #print i,":",str(start),"[]"
                    # 加入换行符
                    block.insert( i,start ) 
                    #block.print_ns()
                    i += 1
                elif start.name in BLOCK_TAGS:
                    behind_img = False
            # NavigableString
            elif start.string.strip():
                # 已经在正文块中
                if start in block.text_list():
                    #print i,":",start.string
                    i += 1 
                    behind_img = False
                # 不在正文块中，在图片后的兄弟文本
                elif behind_img:
                    #print i,":",start.string,"[]"
                    block.insert( i,start )
                    #block.print_ns()
                    i += 1
            start = start.next
    
        return block
    # 执行流程，返回提取到的正文
    def get_content(self):
         # 1.提取基本文本块
        self.parser = Parser(self.url)
        ns_list = self.parser.ns()
        self.title = self.parser.get_title()
        # 2.文本串分块
        self.partitioner = Partitioner()
        blocks = self.partitioner.partition(ns_list) 

        # 3.抽取正文块,副产品为分析信息
        self.judge = Judge( self.title.string,ns_list )
        res = self.judge.select( blocks,ns_list )   

        flag = res['flag']
        cblock = res['block']
        confidence = res['confidence']
        detail = res['detail']
        #if flag:
        content = cblock.to_str()
        (srcs,images) = self.get_images( cblock )
        cblock = self.insert_images(cblock,images)
        content_with_format = cblock.to_str_with_format()
        #else:
        #    content = ""
        #    content_with_format = ""
        #    srcs = None
        return (flag,self.title.string.strip(),content,content_with_format,srcs,confidence,detail)
       

if __name__=='__main__':
    url='http://hi.baidu.com/kissdev/blog/item/ec42e1cfca0cbc36f9dc6132.htm'
    if len(sys.argv)>1:
        url = sys.argv[1]
    sr = Scraper( url )
    (flag,title,content,content_with_format,imgs,confidence,detail) = sr.get_content()
    
    print flag
    if imgs:
        print imgs[0]
    else:
        print
    #print 50*'='+" Content :"+str(confidence)+50*'='
    print title
    print content
    #print 50*'='+' Images '+50*'='
    #if imgs:
    #     for img in imgs:
    #         print img
    #print 50*'='+' Detail '+50*'='
    #print detail
