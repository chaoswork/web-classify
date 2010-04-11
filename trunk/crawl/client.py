#coding=utf8
#client.py:启动client
from pysqlite2 import dbapi2 as sqlite3
from gearman import GearmanClient
from gearman.task import Taskset
from task1 import Task1
import time,os
from config import *

chi_fun = lambda tc,t,c,n:float((tc*n-c*t)**2)/(t*(n-t)*c*(n-c))

# get urls from db
# return: [(url,cate),...]
def get_urls( db ):
    urls = []
    con = sqlite3.connect( db )
    for tb in CATES:
        sql = 'select * from %s limit %d' % (tb,TRAIN_URLS)
        rows = con.execute( sql )
        urls.extend( ['%s\t%s' % (row[0].encode('utf-8'),tb) for row in rows] )
        pass
    
    return urls

# 初始化开方数据库，清除原有数据
def init_chi_db():
    if os.path.exsits( CHI_DB ):
        os.unlink( CHI_DB )
    # create table
    con = sqlite3.connect( CHI_DB )    
    sql = 'create table chi_tb (word text,book float,edu float, finance float, house float, mil float, sport float, car float, ent float, game float, lady float, mobile float, tech float)'
    con.commit()
    con.close()
    
# 存储一个word的开方数据到sqlite
def store_chi( word,chis ):
    con = sqlite3.connect( CHI_DB )
    sql = 'insert into chi_tb values (%s,%s)' % ( word,','.join( map(float,chis) ) )
    con.commit()
    con.close()
    
# 对汇总后的df，进行开方特征选择
# input:Task1.words={word:[cate0,cate1,...,all_num]}
#       Task1.cates=[cate0,cate1,...]
def tsr_chi():
    init_chi_db()               # 初始化数据库
    cates = Task1.cates
    chi_words = []
    n = sum( cates )
    # w_cates=[cate0_num,cate1_num,...,all_num]
    for word,w_cates in Task1.words.items():
        row = {'word':word}
        chis = []
        for i in range(NUM_CATES):
            #print "tc:%d t:%d c:%d n:%d" % (w_cates[i],w_cates[-1],cates[i],n)
            chis.append( chi_fun(w_cates[i],w_cates[-1],cates[i],n) ) # 若不止一个类，分母就不会为0
            pass

        # 将该word的开方信息存到sqlite
        store_chi( word,chis )
    pass
    return True

if __name__ == '__main__':
    urls = get_urls( 'urls.db' )
    
    client = GearmanClient( ['10.61.0.145'] )
    tasks = Taskset()
    TASK_URLS_NUM = 100
    # disptribute task 
    i = 0
    while i<len(urls):
        sub_urls = urls[i:i+TASK_URLS_NUM]
        workload = '\n'.join(sub_urls)
        t = Task1('crawl',workload,str(i) )
        tasks.add( t )
        print "add task:%s" % t.uniq
        i += TASK_URLS_NUM
        # test
        pass
    
    # 1.run the tasks in parallel
    print "1.Preprocess tasks:"
    client.do_taskset( tasks,timeout=TASKS1_TIMEOUT )    
    # 全局开方特征选择
    print "2.TSR by chi:"
    tsr_chi()
