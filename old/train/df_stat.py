#coding=utf8
#wf_stat.py:统计词在各类中出现的频率
#input:[cate]_docs.txt
#     word1:num word2:num ...\nword1:num ...
#output:wf.txt
#     word:cate1_num cate2_num ... all_num
from config import *

class Word:
    def __init__(self,word):
        self.word = word
        self.catenums = [0]*NUM_CATES
        pass
    def __str__(self):
        temp = map( str,self.catenums )
        return "%s:%s" % ( self.word,','.join(temp) )

def readfile( path,cate ):
    cates = [0]*NUM_CATES            # 统计各cate的次数
    words = [ [0]*(NUM_CATES+1) for i in xrange( NUM_WORDS ) ] # 二维数据的初始化
    rf = open( path )
    for line in rf:
        if not line or line[0]=='#':continue # 过滤注释或者空行
        items = line.split()
        cid = int(items[0])-1
        cates[cid] += 1         # cate出现次数计数加1
         for item in items[1:]:
            wid,num = map(int,item.split(':'))
            words[wid-1][NUM_CATES] = words[wid-1][NUM_CATES]+num # word计数加num
            words[wid-1][cid] = words[wid-1][cid]+num # word在该类中出现次数加num

    rf.close()
    return cates,words

# 从目录dir_path获取各个类的doc文件
def getfiles( dir_path ):
    pass

def write_words( words,path ):
    wf = open( path,'w' )
    for word in words:
        wf.write( "%s\n" % str(word) )
    
    wf.close()
    
if __name__ == '__main___':
    print "1) get files from:%s" % RAW_DOCS_DIR
    files = getfiles( RAW_DOCS_DIR )
    
    print "2) statis wf..."
    words = []                  # [word,cate1_num,...]
    for fname in files:
        cate,temp = fname.split('_') # 从文件名获取类别信息
        words = readfile( fname,cate )
    
    #  写入总词频文件
    print "wirte wf:%s" % WF_FILE
    write_words( words,WF_FILE )
