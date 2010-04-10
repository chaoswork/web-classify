#coding=utf8
#worker.py:
#  1. 爬取网页文本，并分词，文档本地记录,doc_[jobid].txt:cate word1:num word2:...\ncate word1...
#  2. Gearman返回统计后的分类词频矩阵：word1 cate1_num cate2_num ... all_num(过滤all_num=1的词)
import sys
from gearman import GearmanWorker
from job import GmJob,SaJob
# for test
from pysqlite2 import dbapi2 as sqlite3

 # work function for gearman
def preprocess( job=None ):
    if job:
        myjob = GmJob( job )    # Gearman job
    else:
        myjob = SaJob()         # 单机job
        pass
    myjob.run()

    result = myjob.finish()
    return result

# 单机 test before move on gearman
def test_crawl():
    con = sqlite3.connect( 'urls.db' )
    tables = ('book','edu','finance','house','mil','sport','car','ent','game','lady','mobile','tech')
    urls = []
    #for tb in tables:
    tb = 'tech'
    sql = 'select * from %s' % tb
    rows = con.execute( sql )
    urls =  ['%s\t%s' % (row[0].encode('utf-8'),tb) for row in rows] # 有的url就是有'-'
    old_cate = ''               # 每个类的doc写到一个文件，如果类改变，重新打开文件
    wf = None
    fingers = []
    # recorder
    num= 0
    success_num = 0
    for url_cate in urls:
        url,cate = url_cate.split()      
        # justify if cate changed
        if cate != old_cate:
            if wf:wf.close()    # 关闭原有file
            wf = open_file( cate )
            old_cate = cate
            pass
        # 计数
        print 'num:%d' % num
        num += 1
        
        try:
            if main_url( url,wf,fingers ):
                success_num += 1
        except Myerror,e:
            print e
    return "finished"

 

if __name__ == '__main__':
    if len(sys.argv)>1:
        preprocess()
    else:
        worker = GearmanWorker( ['10.61.0.145'] )
        print "worker started."
        worker.register_function( 'crawl',preprocess )
        worker.work()
