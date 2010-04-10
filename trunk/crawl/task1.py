#coding=utf8
#Task1.py:task for step 1,爬取，分词，局部去低频词
from gearman.task import Task
from config import *
import time

# 返回的result词频格式：word:cate1_num,cate2_num,...,all_num
class Task1( Task ):
    words = {}
    cates = [0]*NUM_CATES
    def __init__(self,func,arg,uniq=None):
        Task.__init__(self,func,arg,uniq)
    
    def complete( self,result ):
        t = time.strftime( '%Y-%m-%d %X', time.localtime() )
        print "[Complete]task uniq:%s ,handle:%s ,size:%s [%s]" % (self.uniq,self.handle,len(result),t)
        print "collect result..."
        Task1.collect_result( result )
        t = time.strftime( '%Y-%m-%d %X', time.localtime() )
        print "collect result finished.[%s]\n" % t
        self._finished()

    @staticmethod
    def collect_result( result ):
        lines = result.split('\n')
        # 第一行为各分类的文档数目统计,汇总
        tmp_cates = map( int,lines[0].split(',') )
        Task1.cates = map( add,Task1.cates,tmp_cates )
        # 汇总各类中的文档频率
        for line in lines[1:]:
            word,cates_str = line.split()
            cate_nums = map( int,cates_str.split(',') )
            # 判断是否该词已经存在
            if Task1.words.has_key( word ):
                Task1.words[word] = map( add,cate_nums,Task1.words[word] )
            else:
                Task1.words[word] = cate_nums
                
    def status( self,numerator,denominator ):
        t = time.strftime( '%Y-%m-%d %X', time.localtime() )
        print "[Status]task uniq:%s ,status:%d/%d [%s]" % (self.uniq,numerator,denominator,t)

    def retrying( self ):
        print "[Retry]task handle:%s" % self.handle 

    def fail( self ):
        t = time.strftime( '%Y-%m-%d %X', time.localtime() )
        print "[Failed]task uniq:%s ,handle:%s [%s]" % (self.uniq,self.handle,t)
        #self._finished()        
        

