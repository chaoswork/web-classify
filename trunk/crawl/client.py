#coding=utf8
#client.py:启动client
from pysqlite2 import dbapi2 as sqlite3
from gearman import GearmanClient
from gearman.task import Task,Taskset
import time

class MyTask( Task ):
    def __init__(self,func,arg,uniq=None):
        Task.__init__(self,func,arg,uniq)
    
    def complete( self,result ):
        t = time.strftime( '%Y-%m-%d %X', time.localtime() )
        print "[Complete]task uniq:%s ,handle:%s ,result:%s [%s]" % (self.uniq,self.handle,result,t)
        self._finished()
        
    def status( self,numerator,denominator ):
        t = time.strftime( '%Y-%m-%d %X', time.localtime() )
        print "[Status]task uniq:%s ,status:%d/%d [%s]" % (self.uniq,numerator,denominator,t)

    def retrying( self ):
        print "[Retry]task handle:%s" % self.handle 

    def fail( self ):
        t = time.strftime( '%Y-%m-%d %X', time.localtime() )
        print "[Failed]task uniq:%s ,handle:%s [%s]" % (self.uniq,self.handle,t)
        #self._finished()        
        
# get urls from db
# return: [(url,cate),...]
def get_urls( db ):
    urls = []
    con = sqlite3.connect( db )
    tables = ('book','edu','finance','house','mil','sport','car','ent','game','lady','mobile','tech')
    for tb in tables:
        sql = 'select * from %s' % tb
        rows = con.execute( sql )
        urls.extend( ['%s\t%s' % (row[0].encode('utf-8'),tb) for row in rows] )
        pass
    
    return urls

if __name__ == '__main__':
    urls = get_urls( 'urls.db' )
    
    client = GearmanClient( ['10.61.0.145'] )
    tasks = Taskset()
    TASK_URLS_NUM = 100    
    # distribute task 
    i = 0
    while i<len(urls):
        sub_urls = urls[i:i+TASK_URLS_NUM]
        workload = '\n'.join(sub_urls)
        t = MyTask('crawl',workload,str(i) )
        tasks.add( t )
        print "add task:%s" % t.uniq
        i += TASK_URLS_NUM
        # test
        pass
    
    # run the tasks in parallel
    print "do tasks:"
    client.do_taskset( tasks )    
