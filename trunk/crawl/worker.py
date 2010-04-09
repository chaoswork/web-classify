#coding=utf8
#worker.py:
from gearman import GearmanWorker
from crawl import Parser,Myerror
import os,sys,time
# for test
from pysqlite2 import dbapi2 as sqlite3
from subprocess import Popen,PIPE,STDOUT

def open_file( fname ):
    dir_name = 'pages' 
    if not os.path.isdir( dir_name ):
        os.makedirs( dir_name )
    path = '%s/%s.txt' % (dir_name,fname) 
    print "write docs to file:%s" % path
    wf = open( path,'a' )
    return wf

# work function for gearman
def gm_crawl( job ):
    t = time.strftime( '%Y-%m-%d %X', time.localtime() )
    print "[%s]received job:%s" % (t,job.handle)
    #extact job.arg
    urls = job.arg.split('\n')
    old_cate = ''               # 每个类的doc写到一个文件，如果类改变，重新打开文件
    wf = None
    fingers = []
    num = 0
    success_num = 0
    for url_cate in urls:
        url,cate = url_cate.split()
        # justify if cate changed
        if cate != old_cate:
            if wf:wf.close()    # 关闭原有file
            jobid = job.handle.split(':')[-1]
            fname = '%s_%s' % (cate,jobid) # fname:cate_jobid
            print 'fname:'+fname
            wf = open_file( fname )
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
        except StandardError,e:
            print e
        pass
    
    if wf:wf.close()
    return "finished:%d" % success_num

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

def ictclas( text ):
    text = text.replace('\'',' ')      # 去除单引号，以免对分词操作造成影响
    cmd = "./ictclas '%s'"  % text.encode('gbk','ignore')
    std_out = Popen(cmd, shell = True,stdout = PIPE).stdout
    # 提取指纹
    finger = std_out.readline()
    
    word_nums = []
    for line in std_out:
        line=line.strip()
        if line:
            word,num = line.split()
            word_nums.append( "%s:%s" % (word,num) )
            pass
    
    page_words = ' '.join( word_nums ).decode('gbk').encode('utf-8','ignore')
    return (finger,page_words)

# process for a url
def main_url( url,wf,fingers ):
    print "1) crawling:%s" % url
    p = Parser( url )        # 爬取网页
    print "2) parser text begin"
    page_text = p.get_text() # 析取网页文本
    print '3) words segement begin'
    finger,page_words = ictclas( page_text ) # 分词，并提取关键词
    # 仅记录指纹没有出现过的--去重
    if finger not in fingers:
        fingers.append( finger )
        if page_words:
            print '4) writing doc record.\n'
            wf.write( "%s\n" % page_words ) #写doc
            return True
            pass
        else:
            print '   doc is empty.\n'
    else:
        print '   already recorded,finger:%s\n' % finger
    
    return False
        
if __name__ == '__main__':
    if len(sys.argv)>1:
        test_crawl()
    else:
        worker = GearmanWorker( ['10.61.0.145'] )
        print "worker started."
        worker.register_function( 'crawl',gm_crawl )
        worker.work()
