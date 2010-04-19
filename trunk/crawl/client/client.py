#coding=utf8
#client.py:启动client
from pysqlite2 import dbapi2 as sqlite3
from gearman import GearmanClient
from gearman.task import Taskset
from task1 import Task1
from util import *
import time
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

if __name__ == '__main__':
    urls = get_urls( URLS_DB )
    
    client = GearmanClient( ['10.61.0.145'] )
    tasks = Taskset()
    TASK_URLS_NUM = 100
    # disptribute task 
    i = 0
    while i<len(urls):
        sub_urls = urls[i:i+TASK_URLS_NUM]
        workload = '\n'.join(sub_urls)
        t = Task1('crawl',workload,str(i),timeout=TASK1_TIMEOUT,retry_count=1 )
        tasks.add( t )
        print "add task:%s" % t.uniq
        i += TASK_URLS_NUM
        # test
        pass
    
    # 0.init database for return result from worker
    print "0.initialize database for results."   
    tmps = [ "%s int" % cate for cate in CATES]
    cates_str = ','.join( tmps )
    tb_sql = "create table %s (word text primary key,%s,total int);" % (RAW_WORDS_TB,cates_str)
    print tb_sql
    init_db( TASK1_RESULT_DB,tb_sql ) 
    # 1.run the tasks in parallel
    print "1.Preprocess tasks:"   
    client.do_taskset( tasks )
    # 全局开方特征选择--以下是单机版程序
    #print "2.TSR by chi:"
    #tsr_chi()
