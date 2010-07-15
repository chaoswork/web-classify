#coding=utf-8
import re
from utils import *
from block import Block

#评分员:对文本块（多个文本对象合并而来）进行单项评分（好比高考，先算单科阅卷，最后再总分排名）
class Scorer:
    def __init__(self,name):
        self.name = name   
    
    #计算字符串s和t之间的相似度:相似度为title出现在文本块中的词数,
    #暂不考虑次数,以防高频词
    # para:[s:文本块的文本，tws:title分词后的词组]
    def sim_title(self,s,tws):
        n = 0
        for tw in tws:
            if tw not in stop_words and s.find(tw)!=-1: # 若统计次数，用count()
                n += 1
        return float(n)/len(tws)
    
    def __link_rate(self,block):
        all_len = 0
        link_len = 0
        for ns in block.text_list():
            all_len += len(ns.string)
            if ns.parent.name == 'a' or ns.parent.parent.name == 'a':
                link_len += len(ns.string)
        if all_len>0:
            return float( all_len-link_len )/( all_len+link_len )
        else:
            print "####[Error]:Has no text in this block."
            return 0
    
    #计算块block的文字占网页的比例
    def __text_rate(self,block,ns_len):
        all_len = 0
        for tb in block.text_list():
            all_len += len(tb.string)
        
        if ns_len > 0:
            return float(all_len)/ns_len
        else:
            print "####[Error]:Has no text in this webpage."
            return 0
    
    #对一个大块计算其为正文的三项指标值,confidence最后总计
    def score( self,block,tws,ns_len ):
        score = {}
        #Todo:判断tws长度是否为0
        score['sim_title'] = float( self.sim_title( block.to_str(),tws) )
        score['link_rate'] = self.__link_rate(block)
        score['text_rate'] = self.__text_rate(block,ns_len)
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        return score
