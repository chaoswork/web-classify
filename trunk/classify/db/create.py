#coding=utf8
# create.py 创建相关数据库和表，仅在程序开始前，做一次操作即可
from mypack.classify.config import *
import os
from pysqlite2 import dbapi2 as sqlite3

def init_db():
    if os.path.exists( DB ):
        log.error( '%s aready exists!' % DB )
        exit(1)
        #os.unlink( DB )
        
    con = sqlite3.connect( DB )    
#def create_df_tb():
    tmps = [ "%s int" % cate for cate in CATES]
    cates_str = ','.join( tmps )
    tb_sql = "create table %s (word text primary key,%s,total int);" % (DF_TB,cates_str)
    con.execute( tb_sql )       
    log.info( 'create table :%s' % tb_sql )
    
#def create_chi_tb():
    tmps = [ "%s float" % cate for cate in CATES]
    cates_str = ','.join( tmps )
    tb_sql = "create table %s (word text primary key,%s,idf float);" % (CHI_TB,cates_str)
    con.execute( tb_sql )       
    log.info( 'create table :%s' % tb_sql )
    
   # create table
    con.commit()
    con.close()

if __name__=='__main__':
    init_db()
