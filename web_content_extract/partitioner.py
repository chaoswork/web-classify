#coding=utf-8
from mypack.util.htmlproc.BeautifulSoup import NavigableString,Tag,Comment
from block import Block
from recorder import Recorder
from config import *
from utils import mean,var

# 网页分块员:将文本串列表根据间距分块
class Partitioner:
    def __init__(self):
        self.recorder = Recorder()
    # 文本块对象：由多个NavigableString对象构成
    # 计算分块的ns间距阈值:去除第一个offset,再去掉一个最大者，再取平均值
    # 小于该阈值才将分块合并
    # 间距阈值越大，噪声越大，取1即可
    # def __threshold(self,off_list):
    #     # 关于offset的一些统计信息
    #     n_off = 0
    #     sum_off = 0
    #     max_off = 0
    #     # 去除第一个
    #     if len(off_list) >1:
    #         off_list[0] = 0
    #         #off_list[-1] = 0
        
    #     off_list.remove( max_off )
    #     off_list = filter(lambda x:x>0,off_list)
    #     thr = mean(off_list)
    #     # #debug
    #     # print m
    #     # print v
    #     # exit()
    #     #self.detail +=( 'n_off:%d\tsum_off:%d\tmean_off:%f\n' % (n_off,sum_off,mean_off))
    #     self.recorder.write("Threshold of block:"+str(thr)+"\n")
    #     return thr

    # 将间距小于阈值的文本串合并成块Todo:title补
    def __merge(self,ns_list):
        block_li = []                 # 文本块列表
        block = Block()               # 文本块
        for i in range(len(ns_list)):
            if ns_list[i]['offset'] >= 1:#thr:                
                # 大于或等于阈值,保存上一个块，划给新块
                if not block.is_empty():
                    block_li.append( block )
                    block = Block()               # 新增文本块
            if ns_list[i]['node'] and ns_list[i]['node'].string.strip():
                block.append( ns_list[i]['node'] )
        return block_li
    
    #Todo 二次合并：根据块间相似性
    def __re_merge(self,blocks):
        return blocks

    def partition(self,ns_list):
        offsets = []
        for ns in ns_list:
            offsets.append( ns['offset'] )

        #thr = self. __threshold( offsets )
        blocks = self.__merge( ns_list )
        
        return blocks
