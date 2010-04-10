#coding=utf8
#worker.py:
#  1. 爬取网页文本，并分词，文档本地记录,doc_[jobid].txt:cate word1:num,word2:...\ncate word1...
#  2. Gearman返回统计后的分类词频矩阵：word1 cate1_num,cate2_num,...,all_num(过滤all_num=1的词)
import sys
from gearman import GearmanWorker
from job import GmJob,SaJob

 # work function for gearman
def preprocess_gm( job ):
    try:
        job.status(0,0)
        myjob = GmJob( job )    # Gearman job
        myjob.run()
        result = myjob.finish()
    except Exception,e:
        print e
        result = ''
    print 'worker finished job:%s' % job.handle
    print '-'*80
    return result 

def preprocess_sa():
    myjob = SaJob()         # 单机job
    myjob.run()
    result = myjob.finish()
    wf = open('tmp.txt','w')
    wf.write(result)
    return result 
    
if __name__ == '__main__':
    if len(sys.argv)>1:
        preprocess_sa()
    else:
        worker = GearmanWorker( ['10.61.0.145'] )
        print "worker started."
        worker.register_function( 'crawl',preprocess_gm )
        worker.work()
