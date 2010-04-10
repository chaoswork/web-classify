#coding=utf8
import time
import os
from subprocess import Popen,PIPE,STDOUT
from crawl import Parser,Myerror
from config import RAW_DOC_DIR

# 记录一个job相关的全局信息操作,抽象对象，不应该被实例化
class Job:
    def __init__( self ):
        self.words={}                        # 用来统计词频
        self.fingers = []                    # doc指纹
        self.cur_cate = None                 # 记录当前处理的url所属类别
        self.wf = None                       # 结果输出文件
        if not os.path.isdir( RAW_DOC_DIR ): # 确保输出目录存在
            os.makedirs( dir_name )
    
    # 统计词w,出现n次
    def __add_word(self,w,n):
        if not self.words.has_key[w]:
            self.words[w] = [0]*NUM_CATES
            pass
        cate_id = CATES.index(self.cate)
        self.words[w][cate_id] += n
        
    # 获取urls
    def __get_url_cates(self):
        pass
    
    # process for a url
    def __main_url( self,url ):
        print "1) crawling:%s" % url
        p = Parser( url )        # 爬取网页
        print "2) parser text begin"
        page_text = p.get_text() # 析取网页文本
        print '3) words segement begin'
        page_words = self.__ictclas( page_text ):
        if page_words:
            print '4) writing doc record.\n'
            Job.write_doc( page_words ) #写doc
            return True
        elif page_words=='':
            print '   doc is empty.\n'
        else:
            print '   already recorded.'
            pass
        return False
    
    # 分词,统计词频
    def __ictclas( text ):
        text = text.replace('\'',' ')      # 去除单引号，以免对分词操作造成影响
        cmd = "./ictclas '%s'"  % text.encode('gbk','ignore')
        std_out = Popen(cmd, shell = True,stdout = PIPE).stdout
        # 提取指纹
        finger = std_out.readline()
        # 仅记录指纹没有出现过的--去重
        if finger in Job.fingers:return None 
        Job.fingers.append( finger )
        word_nums = []
        for line in std_out:
            line=line.strip()
            if line:
                word,num = line.split()
                word = word.decode('gbk').encode('utf-8','ignore')
                # 1.统计词频
                Job.add_word(w,int(num) )
                # 2.形成doc
                word_nums.append( "%s:%s" % (word,num) )
                pass
            pass
        page_words = ' '.join( word_nums )
        return page_words

    def run(self):
        url_cates = self.__get_url_cates()
        num = 0
        for url,cate in url_cates:
            Job.cur_cate = cate
            # 计数
            print 'num:%d' % num
            num += 1
            try:
                self.__main_url( url ):
            except Myerror,e:
                print e
            except StandardError,e:
                print e
            pass
    
    #记录一个doc，格式cate:word:num word:num ... \n
    def write_doc( self,dos_str ):
        self.wf.write( "%s:%s\n" % (self.cur_cate,dos_str) )
    
    # job finish,返回汇总后的词频矩阵，str形式
    def finish(self):
        self.wf.close()
        #汇总统计词频，str化输出
        words_str = ''
        for word in self.words.keys():
            all_num = sum( self.words[word] )
            cates_str = ','.join( self.words[word] )
            words_str += "%s:%s,%d\n" % (word,cates_str,all_num) 
            pass
        return words_str
    
# job record for Gearman
class GmJob(Job):
    def __init__( self,job ):
        Job.__init__( self )
        self.job = job                       # GearmanJob
        # 打开写入文件
        jobid = self.job.handle.split(':')[-1]
        fname = 'doc_%s.txt' % jobid # fname:doc_[jobid]
        self.wf = open( fname,'w' )
        # tips
        t = time.strftime( '%Y-%m-%d %X', time.localtime() )
        print "[%s]received job:%s" % (t,job.handle)
        print "write docs to file:%s" % path

    # 获取urls,以及对应的cate
    def __get_url_cates(self):
        #extact job.arg
        urls = job.arg.split('\n')
        url_cates = []
        for url_cate in urls:
            url,cate = url_cate.split()
            url_cates.append( (url,cate) )
            pass
        return url_cates

# simple factory pattern
class JobFactory:
    def factory( self,job_type ):
        if job_type = 'gearman':
            return GmJob( job )
        else:
            return SaJob()
