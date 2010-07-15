#coding=utf8
#voca.py 开方特征选择，形成字典
# input:chi_tb
#      word|book|edu|finance|house|mil|sport|car|ent|game|lady|mobile|tech|total
# output:voca.txt 字典
#      word    idf
# usage：
from mypack.classify.config import *
# 读取字典中的词
# 输出格式：[(word,idf),...]
def read_voca():
    log.info("read vocabulary:%s" % VOCA_FILE)
    rf = open( VOCA_FILE )
    dic = []
    for line in rf:
        word,idf = line.split()
        dic.append( (word.decode('utf8'),float(idf)) )
        
    return dic

# 将一个文档转换为字典表示的tfidf向量
# para doc:[(word,num),...]
# return new_doc:[(windex,tfidf),...]
def transform_doc( voca,doc ):
    if len(doc)==0:
        return None
    new_doc = []
    words = [t[0] for t in voca]
    words_num = sum( [t[1] for t in doc] )
    for word,num in doc:
        if word in words:
            index = words.index( word )
            tfidf = num*voca[index][1]/words_num # tfidf = tf*idf
            new_doc.append( (index+1,tfidf ) ) # libsvm index从1开始

    # 按词的index进行排序
    new_doc = sorted( new_doc,key=lambda x:x[0] )
    return new_doc

# 将一个doc字符串转换为list:
# word:num,...->[(word,num),...]
def _read_doc( doc_str ):
    word_nums = doc_str.split(',')
    doc = []
    for word_num in word_nums:
        w,num = word_num.split(':')
        doc.append( [w,num] )
        pass
    return doc

# 对所有样本文档进行字典转换
# 读一行转换一行
def transform_samples( voca ):
    all_file = SAMPLES_FILE
    log.info( "read docs:%s" % all_file )
    
    rf = open( all_file )
    wf = open( NEW_DOC,'w' )
    docs = []
    for line in rf:
        line = line.strip().decode('utf8')
        if line and line.find('\t')!=-1:
            cate,doc_str = line.split('\t',1)
            doc = _read_doc( doc_str )
            new_doc = transform_doc( doc,voca )
            if len(new_doc)>0:
                cate_index = CATES.index( cate )
                new_doc = [ "%s:%f" % (w,tfidf) for w,tfidf in new_doc ]
                new_doc_str = ' '.join(new_doc)
                wf.write( '%d %s\n' % (cate_index,new_doc_str) )
                pass
    rf.close()
    wf.close()

if __name__ == "__main__":
    voca = read_voca()
    if 1:
        transform_samples( voca )
    else:
        doc = [('分词',1),('结果',2)]
        transform_doc( voca,doc )
