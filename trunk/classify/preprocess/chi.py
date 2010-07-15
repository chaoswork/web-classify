#coding=utf8
#对词频数据进行开方和idf计算:
# input:df_tb
#      word|book|edu|finance|house|mil|sport|car|ent|game|lady|mobile|tech|total
# output:chi_tb
#      word|book|edu|finance|house|mil|sport|car|ent|game|lady|mobile|tech|idf
# usage：
# from mypack.classfiy.chi.chi import chi_compute()
# chi_compute()
from mypack.classify.config import *
from pysqlite2 import dbapi2 as sqlite3

# 存储一个word的开方,idf数据到sqlite
def _store_chi( chi_m ):
    con = sqlite3.connect( DB )
    for row in chi_m:
        cates_str = ','.join( map(str,row['chis']) )
        sql = "insert or ignore into %s values ('%s',%s,%f)" % ( CHI_TB,row['word'],cates_str,row['idf'] )
        #print sql
        con.execute( sql )
        pass
    con.commit()
    con.close()
    
def _tsr_chi():
    '''select words which df larger than MIN_DF,and compute chi and idf value for words.'''
    #chi计算公式
    chi_fun = lambda tc,t,c,n:float(n*(tc*n-c*t)**2)/((n-c)*c*t*(n-t))
    
    con = sqlite3.connect( DB )
    # 1.获取各类的df
    cate_nums = []
    for cate in CATES:
        sql = "select sum(%s) from %s" % (cate,DF_TB)
        cur = con.execute( sql )
        cate_nums.append( cur.fetchone()[0] )
        pass
    #test
    print cate_nums

    # 2.算总文档数
    n = sum( cate_nums )
    
    # 3.对各词进行开方计算
    chi_words = []
    sql = "select * from %s where total>=%d" % (DF_TB,MIN_DF)
    cur = con.execute( sql )
    chi_m = []
    for witem in cur:
        # word cate1_chi cate2_chi ... df
        row = {'word':witem[0],'chis':[],'idf':log( float(n)/witem[-1] )}
    
        for i in range(NUM_CATES):
            #print "tc:%d t:%d c:%d n:%d" % (witem[i+1],witem[-1],cate_nums[i],n)
            row['chis'].append( chi_fun(witem[i+1],witem[-1],cate_nums[i],n) ) # 若不止一个类，分母就不会为0
            pass
        chi_m.append( row )
        pass
    
    con.close()
    return chi_m

def chi_compute():
    '''对外接口'''
    log.info( 'begin chi and idf compute,select words which df>%d' % MIN_DF )
    chi_m = _tsr_chi()
    _stor_chi( chi_m )
    log.info( 'chi and idf have been computed,see %s:%s' % (DB,CHI_TB) ) 
        
def chi_select():
    # 从卡方信息表中读取:(word,idf)
    con = sqlite3.connect( DB )
    tmp = []
    for cate in CATES:
        tmp.append( '%s>%f' % (cate,MIN_CHI) )
        pass
    ph = ' or '.join( tmp )
    sql = 'select word,idf from %s where %s' % (CHI_TB,ph)
    cur = con.execute( sql )
    rows = cur.fetchall()
    #写到文件
    wf = open( VOCA_FILE,'w' )
    for row in rows:
        wf.write( "%s\t%f\n" % row )
        pass
    wf.close()
