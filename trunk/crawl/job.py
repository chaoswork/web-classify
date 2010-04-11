#coding=utf8
import time
import os
from subprocess import Popen,PIPE,STDOUT
from parser import Parser
from config import *
from util import add

# 记录一个job相关的全局信息操作,抽象对象，不应该被实例化
class Job:
    def __init__( self ):
        self.words={}                        # 用来统计词频
        self.fingers = []                    # doc指纹
        self.cur_cate = None                 # 记录当前处理的url所属类别
        self.wf = None                       # 结果输出文件
        if not os.path.isdir( RAW_DOC_DIR ): # 确保输出目录存在
            os.makedirs( RAW_DOC_DIR )
    
    # 统计词w,出现n次--修正，算文档频率DF，不管出现多少次，都算1次
    def add_word(self,w,n):
        if not self.words.has_key(w):
            self.words[w] = [0]*NUM_CATES
            pass
        cate_id = CATES.index(self.cur_cate)
        self.words[w][cate_id] += 1
        
    # 获取urls
    def get_url_cates(self):
        pass
    
    # process for a url
    def process_url( self,url ):
        print "1) crawling:%s" % url
        p = Parser()        # 爬取网页
        if not p.parse( url ):return False # 爬取失败
        
        print "2) parser text begin"
        page_text = p.get_text() # 析取网页文本
        
        print '3) words segement begin'
        page_words = self.ictclas( page_text )
        if page_words=='':      # 无分词结果
            print '   doc is empty.\n'
            return False
        elif page_words==None:
            print '   already recorded.\n'
            return False
        
        print '4) writing doc record.\n'
        self.write_doc( page_words ) #写doc
        return True
    
    # 分词,统计词频,保存结果到类
    def ictclas( self,text ):
        text = text.replace('\'',' ')      # 去除单引号，以免对分词操作造成影响
        cmd = "./ictclas '%s'"  % text.encode('gbk','ignore')
        std_out = Popen(cmd, shell = True,stdout = PIPE).stdout
        # 提取指纹
        finger = std_out.readline()
        # 仅记录指纹没有出现过的--去重
        if finger in self.fingers:return None 
        self.fingers.append( finger )
        word_nums = []
        for line in std_out:
            line=line.strip()
            if line:
                word,num = line.split()
                word = word.decode('gbk').encode('utf-8','ignore')
                # 1.统计词频
                if word.find(':')!=-1:continue # 过滤含':'的词
                self.add_word(word,int(num) )
                # 2.形成doc
                word_nums.append( "%s:%s" % (word,num) )
                pass
            pass
        page_words = ','.join( word_nums )
        return page_words

    def run(self):
        url_cates = self.get_url_cates()
        num = 0
        for url,cate in url_cates:
            self.cur_cate = cate
            # 计数
            print 'num:%d' % num
            num += 1
            try:
                self.process_url( url )
            except StandardError,e:
                print e
            pass
    
    #记录一个doc，格式cate word:num,word:num,... \n
    def write_doc( self,dos_str ):
        self.wf.write( "%s\t%s\n" % (self.cur_cate,dos_str) )
    
    # job finish,返回汇总后的词频矩阵，str形式
    def finish(self):
        print "count document frequency in cates..."
        self.wf.close()
        #汇总分类文档数目 
        # cate_nums = [0]*NUM_CATES
        # cates_str = ','.join( map(str,cate_nums) )
        #汇总统计词频，str化输出
        word_dfs = []
        for word in self.words.keys():
            cate_nums = map( add,cate_nums,self.words[word] )
            all_num = sum( self.words[word] )
            # 局部特征选择--去低频词
            if all_num >= TH_LOCAL_TSR:
                cates_str = ','.join( map(str,self.words[word]) )
                word_dfs.append( "%s\t%s,%d" % (word,cates_str,all_num) )
            pass
        words_str = '\n'.join( word_dfs )
        #return "%s\n%s" % (cates_str,words_str)
        return words_str
    
# job record for Gearman:从client获取参数
class GmJob(Job):
    def __init__( self,job ):
        Job.__init__( self )
        self.job = job                       # GearmanJob
        # 打开写入文件
        jobid = self.job.handle.split(':')[-1]
        path = '%s/doc_%s.txt' % (RAW_DOC_DIR,jobid) # fname:doc_[jobid]
        self.wf = open( path,'w' )
        # tips
        t = time.strftime( '%Y-%m-%d %X', time.localtime() )
        print "[%s]received job:%s" % (t,job.handle)
        print "write docs to file:%s" % path

    # 获取urls,以及对应的cate
    def get_url_cates(self):
        url_cates = []
        #extact job.arg
        urls = self.job.arg.split('\n')
        for url_cate in urls:
            if not url_cate or url_cate.find('\t')==-1:continue # 防止错误格式数据
            url,cate = url_cate.split('\t')
            url_cates.append( (url,cate) )
            pass
        return url_cates

# stand-alone job:从sqlite中获取输入
class SaJob(Job):
    def __init__( self ):
        Job.__init__( self )
        path = '%s/doc_sa.txt' % (RAW_DOC_DIR,) # fname:doc_[jobid]
        self.wf = open( path,'w' )
        # tips
        t = time.strftime( '%Y-%m-%d %X', time.localtime() )
        print "[%s]start stand-alone job..." % (t,)
        print "write docs to file:%s" % path
        
    # 获取urls,以及对应的cate
    def get_url_cates(self):
        url_cates = []
        #extact job.arg
        from pysqlite2 import dbapi2 as sqlite3
        con = sqlite3.connect( 'urls.db' )
        for tb in CATES:
            sql = 'select * from %s limit 9' % tb # for test
            rows = con.execute( sql )
            url_cates.extend(  [(row[0].encode('utf-8','ingore'),tb) for row in rows] ) # 有的url就是有'-'
            pass
        con.close()
        return url_cates
