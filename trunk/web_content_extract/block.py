#coding=utf-8
from mypack.util.htmlproc.BeautifulSoup import NavigableString
from utils import html_char_transform

# 文本块对象：由多个NavigableString对象构成
class Block:
    def __init__(self):
        self.ns_li = []
        
    def p_parent(self,ns):
        while ns.parent:
            if ns.parent.name == 'p':
                return ns.parent
            else:
                ns = ns.parent
        return None
    
    # 将文本块转换成字符串
    def to_str( self ):
        s = ''.join( [str(tb).decode('utf8') for tb in self.ns_li if tb ] )        
        return html_char_transform(s)

    # 将文本块转换成字符串
    def to_str_with_format( self ):
        s = ''
        cur_p = None            # 如果当前文本处于p标签中，记录p
        i = 0
        for tb in self.ns_li:
            p = self.p_parent(tb)
            # 一个新段落
            if p:
                if p != cur_p:
                    cur_p = p
                    s += str(p)
                # 已包含在上个p中，不做处理
            else:
                # 没有在p中，直接加
                # 图片居中
                if not isinstance(tb,NavigableString) and tb.name == 'img':                    
                    s += ("<center>"+str(tb)+"</center>")
                else:
                    s += str( tb )
        return html_char_transform(s)
    # 添加一个文本,也是唯一的块构建方法
    def append( self,ns ):
        self.ns_li.append( ns )
        
    def insert( self,i,ns ):
        #print i,":",str(ns)
        self.ns_li.insert( i,ns )

    # 在头部插入元素
    def push( self,ns ):
        self.ns_li.insert( 0,ns )
        
    def len( self ):
        return len( self.ns_li )

    def str_len( self ):
        l = 0
        for ns in self.ns_li:
            l += len(ns.string)
        return l

    def text_list(self):
        return self.ns_li

    def is_empty( self ):
        return self.len()==0

    # 扩展ns节点
    def extend( self,nss ):
        self.ns_li.extend( nss )

    # 去掉头部的num个ns
    def pop( self,num ):
        self.ns_li = self.ns_li[num:]

    # for debug,print all ns in it
    def print_ns(self):
        print 100*"-"
        for ns in self.ns_li:
            print str(ns)
