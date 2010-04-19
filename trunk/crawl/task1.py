#coding=utf8
#Task1.py:task for step 1,爬取，分词，局部去低频词
# 最终汇总后的结果存到sqlite中
from gearman.task import Task
from pysqlite2 import dbapi2 as sqlite3
from config import *
from util import *
import time

# 返回的result词频格式：word:cate1_num,cate2_num,...,all_num
class Task1( Task ):
    words = {}
    cates = [0]*NUM_CATES
    def __init__(self,func,arg,uniq=None,background=False,high_priority=False,timeout=None,retry_count=0):
        Task.__init__(self,func,arg,uniq,background,high_priority,timeout,retry_count)
    
    def complete( self,result ):
        t = time.strftime( '%Y-%m-%d %X', time.localtime() )
        print "[Complete]task uniq:%s ,handle:%s ,size:%s [%s]" % (self.uniq,self.handle,len(result),t)
        print "[collect] result to sqlite..."
        Task1.collect_result( result )
        t = time.strftime( '%Y-%m-%d %X', time.localtime() )
        print "[Finish]Task really finished.[%s]\n" % t
        self._finished()

    #存储result中一个word的各类df记录到sqlite
    @staticmethod
    def store_word_df( con,word,cate_nums ):
        # 判断是否该词已经存在
        sql = "select * from %s where word='%s'" % (RAW_WORDS_TB,word)
        cur = con.execute( sql )
        record = cur.fetchone()
        if record:      # 该词已经存在
            cate_nums = map( add,record[1:],cate_nums )  # record[0]==word
            cols = list(CATES)
            cols.append('total')
            tmps = map( lambda c,v:"%s=%d" % (c,v),cols,cate_nums )
            cstr = ','.join( tmps ) 
            sql = "update or ignore %s set %s where word='%s'" % ( RAW_WORDS_TB,cstr,word )
        else:                   # 插入
            cstr = ','.join( map(str,cate_nums) ) 
            sql = "insert or ignore into %s values('%s',%s)" % ( RAW_WORDS_TB,word,cstr )
            pass
        #print sql
        con.execute( sql )
        
    @staticmethod
    def collect_result( result ):        
        con = sqlite3.connect( TASK1_RESULT_DB )
        lines = result.split('\n')
        # 汇总各类中的文档频率
        for line in lines:
            try:
                word,cates_str = line.split('\t')
                cate_nums = map( int,cates_str.split(',') )
                Task1.store_word_df( con,word,cate_nums )
            except ValueError:
                print '[W]Bad word_cates num data:%s' % line
                continue
        con.commit()
        con.close()
        return True
                
    def status( self,numerator,denominator ):
        t = time.strftime( '%Y-%m-%d %X', time.localtime() )
        print "[Status]task uniq:%s, handle:%s, status:%d/%d [%s]" % (self.uniq,self.handle,numerator,denominator,t)

    def retrying( self ):
        print "[Retry]task handle:%s" % self.handle 

    def fail( self ):
        t = time.strftime( '%Y-%m-%d %X', time.localtime() )
        print "[Failed]task uniq:%s ,handle:%s [%s]" % (self.uniq,self.handle,t)
        #self._finished()        
        

