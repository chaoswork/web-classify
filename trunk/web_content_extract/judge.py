#coding=utf-8
from scorer import Scorer
from block import Block
from recorder import Recorder
from utils import var,title_split
from config import *

#裁判长:收集评分员的评分，然后判断网页是目录页，还是内容页；若是后者，选出正文块集
class Judge:
    def __init__(self,title,ns_list):
        self.tws = title_split(title)
        self.ns_list = ns_list
        self.scorer = Scorer('xh')
        self.score_li = []
        self.confidence_li = []
        self.sim_var = 0.0
        self.recorder = Recorder()
        self.block = []
        
    # 总计各块的最后得分
    def __summarize(self,blocks):
        ns_len = max([block.str_len() for block in blocks]) # 最长文本块的长度
        for block in blocks:
            self.score_li.append( self.scorer.score(block,self.tws,ns_len) )
        
        sim_li = [ score['sim_title'] for score in self.score_li ]
        self.sim_var = var( sim_li )
        if self.sim_var > SIM_TITLE_VAR:
            self.confidence_li = [ score['sim_title']*score['link_rate']*score['text_rate'] \
                                  for score in self.score_li ]
        else:
            # title相似度普遍低，说明title不具说明性，不计该指标
            self.confidence_li = [ score['link_rate']*score['text_rate'] for score in self.score_li ]
        return self.confidence_li

    # 构建详细分析信息
    def __construct_detail( self,blocks,pos ):
        detail = ("variance of title similarity:%f\n" % self.sim_var)
        for i in range(len(self.confidence_li)):
            detail += (150*'-'+"\n")
            score = self.score_li[i]
            conf = self.confidence_li[i]
            detail += ("block:%d\n%s\n\n" % (i+1,blocks[i].to_str()))
            if i==pos:
                detail += ("<font color='red'>sim_t:%f\tlink_rate:%f\ttext_rate:%f\tconfidence:%f\n</font>" % (score['sim_title'],score['link_rate'],score['text_rate'],conf))               
            else:
                detail += ("sim_t:%f\tlink_rate:%f\ttext_rate:%f\tconfidence:%f\n" % (score['sim_title'],score['link_rate'],score['text_rate'],conf))                       
        self.recorder.write( detail )
                
    # 上寻title，并做调整
    def __find_title(self,ns_list):
        for i in range( len(ns_list) ):
            if self.scorer.sim_title( ns_list[i]['node'].string,self.tws )> MIN_SIM_TITLE:
                return i
        return -1
    
    # 若未包含的title，包含进来
    def __adjust( self,block,ns_list ):
        nodes = [ ns['node'] for ns in ns_list ]
        # 如果上一个文本块和title非常相似，那么断定为标题
        p1 = nodes.index( block.text_list()[0] )

        pos_title = self.__find_title( ns_list )
        # 找到title
        if pos_title >=0:
            if pos_title < p1:
                # title没有包含进来
                block.push( ns_list[pos_title]['node'] )
            else:
                # title已在块内部
                block.pop(pos_title-p1)
                
        return block
    
    # 过滤正文当中的杂碎信息,如小广告，发表日期等
    def __filter( self,block):
        return block
    
    # 从blocks中提取置信度最大的作为正文块
    # 判断正文依据:title相似性,链接文本比例,文本密度
    def select(self,blocks,ns_list):
        self.__summarize( blocks )
        # 计算最大的confidence的块
        max_s = 0
        pos = 0
        for i in range(len(self.confidence_li)):
            cs = self.confidence_li[i]
            if cs > max_s:
                max_s = cs
                pos = i
        cblock = blocks[pos]
        # 第二道工艺：精雕细琢
        #cblock = self.__adjust( cblock,ns_list )
        #cblock = self.__filter( cblock )
        
        self.__construct_detail( blocks,pos )
        #if is_adjusted:
        #    confidence = self.confidence_li[pos]+self.confidence_li[pos-1]
        #else:
        confidence = self.confidence_li[pos]
        flag = max_s > MIN_CONFIGDENCE and self.score_li[pos]['link_rate'] >MIN_LINK_RATE
        return {'flag':flag,'block':cblock,'confidence':confidence,'detail':self.recorder.read()}
        
