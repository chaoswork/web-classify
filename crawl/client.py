#coding=utf8
#client.py:启动client
from pysqlite2 import dbapi2 as sqlite3
from gearman import GearmanClient
from gearman.task import Taskset
from task1 import Task1
import time
from config import *

chi_fun = lambda tc,t,c,n:float((tc*n-c*t)**2)/(t*(n-t)*c*(n-c))

# get urls from db
# return: [(url,cate),...]
def get_urls( db ):
    urls = []
    con = sqlite3.connect( db )
    tables = ('book','edu','finance','house','mil','sport','car','ent','game','lady','mobile','tech')
    for tb in tables:
        sql = 'select * from %s limit 10' % tb
        rows = con.execute( sql )
        urls.extend( ['%s\t%s' % (row[0].encode('utf-8'),tb) for row in rows] )
        pass
    
    return urls

# 对汇总后的df，进行开方特征选择
# input:Task1.words={word:[cate0,cate1,...,all_num]}
#       Task1.cates=[cate0,cate1,...]
# output:chi值最高的TOP_CHI个词--即字典
def tsr_chi():
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
        row['max'] = max( chis )
        # for test
        row['chis'] = ','.join( map(str,chis) )
        # end
        chi_words.append( row )
    pass
    # 对word按GSS的最大值排序,降序
    chi_words.sort(lambda x,y:cmp(x['max'],y['max']),None,True)
    # for test
    dicts = [ item['word'] for item in chi_words[:TOP_CHI] ]
    #dicts = [ "%s\t%f\t%s" % (item['word'],item['max'],item['chis']) for item in chi_words[:TOP_CHI] ]
    # test end
    dict_str = '\n'.join( dicts )
    # test
    wf = open('dict.txt','w')
    wf.write( dict_str )
    wf.close()
    return dict_str

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
    client.do_taskset( tasks )    
    # 全局开方特征选择
    print "2.TSR by chi:"
    tsr_chi()
