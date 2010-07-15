#coding=utf8
# predict.py 采用svm预测分类
from mypack.classify.config import *
from mypack.web_content_extract.extract import Extractor
from mypack.util.ictclas  import ICTclas
#from mypack.util.smallseg.myseg import seg
from mypack.classify.preprocess.voca import read_voca,transform_doc 
from svm import *

# 对文本进行分类
def classify_text( text ):
    # 2. 分词
    ic = ICTclas( text )
    word_nums = ic.words()     # ictclas分词
    #word_nums = seg( text )     # smallseg分词
    #for w,num in word_nums:
    #    print '%s:%d' % (w.encode('utf8'),num) 
    # 3. 转换为tfidf的向量
    log.info( '3. transform doc to tfidf vector' )
    voca = read_voca()
    new_doc = transform_doc( voca,word_nums )
    #new_doc = ['%s:%f' % (w,tfidf) for w,tfidf in new_doc]
    #new_doc_str = ' '.join( new_doc )
    #wf = open( '../data/test.txt','w')
    #wf.write( new_doc_str )
    # 4. 预测
    m = svm_model( SVM_MODEL )
    r = m.predict( dict(new_doc) )
    return CATES[int(r)]
    
# 对url进行爬取，然后提取正文分类
def classify_url( url ):
    # 1. 爬取网页，正文提取
    log.info(  'classify url:%s' % url )
    log.info( 'extract content' )
    extr = Extractor( url )
    if not extr.is_content_page():
        log.warning( 'This page has no content:%s' % url )
        exit(0)
    text = extr.get_content()   # 正文提取
    log.info( 'word segment')
    return classify_text( text )
    
if __name__=='__main__':
    url = 'http://finance.ifeng.com/stock/roll/20100521/2219151.shtml'
    #url = 'http://blog.sina.com.cn/s/blog_58270b4b0100im31.html?tj=1'
    url = 'http://news.qq.com/a/20100521/002029.htm'
    
    cate = classify( url )
    print CATES[ r ]
