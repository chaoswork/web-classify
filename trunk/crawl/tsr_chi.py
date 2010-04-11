#coding=utf8
#对回收的数据进行开方计算:
#注意，为了达到尽可能低的偶合，采用sqlite作为中间数据存储方式
from uitl import *
from config import *

# 存储一个word的开方数据到sqlite
def store_chi( chi_m ):
    con = sqlite3.connect( CHI_DB )
    for row in chi_m:
        cates_str = ','.join( map(str,row['chis']) )
        sql = 'insert or ignore into %s values (%s,%s)' % ( CHI_TB,row['word'],cates_str )
        con.execute( sql )
        pass
    con.commit()
    con.close()
    
# 对汇总后的df，进行开方特征选择
# input:Task1.words={word:[cate0,cate1,...,all_num]}
#       Task1.cates=[cate0,cate1,...]
def tsr_chi():
    con = sqlite3.connect( TASK1_RESULT_DB )
    # 1.获取各类的df
    cate_nums = []
    for cate in CATES:
        sql = "select sum(%s) from %s" % (cate,RAW_WORDS_TB)
        cur = con.execute( sql )
        cate_nums.append( cur.fetchone()[0] )
        pass
    #test
    print cate_nums
    # 2.算总文档数
    n = sum( cate_nums )
    # 3.对各词进行开方计算
    chi_words = []
    sql = "select * from %s where total>%d" % (RAW_WORDS_TB,TH_GLOBAL_TSR)
    cur = con.execute( sql )
    chi_m = []
    for witem in cur:
        row = {'word':witem[0],'chis':[]}
        
        for i in range(NUM_CATES):
            #print "tc:%d t:%d c:%d n:%d" % (w_cates[i],w_cates[-1],cates[i],n)
            row[chis]append( chi_fun(w_cates[i],w_cates[-1],cates[i],n) ) # 若不止一个类，分母就不会为0
            pass
        chi_m.append( row )
        pass
    return chi_m

if __name__=='__main__':
    print "0.initialize database:%s" % CHI_DB   
    tmps = [ "%s float" % cate for cate in CATES]
    cates_str = ','.join( tmps )
    tb_sql = "create table %s (word text primary key,%s);" % (CHI_TB,cates_str)
    print tb_sql
    init_db( CHI_DB,tb_sql ) 
    
    print "1.read word df matrix and compute chi value for words."
    chi_m = tsr_chi()
    
    print "2.store chi values to sqlite."
    store_chi( chi_m )

