#coding=utf8
from pysqlite2 import dbapi2 as sqlite3

#util
add = lambda x,y:x+y

# 初始化开方数据库，清除原有数据
def init_db( db,tb_sql ):
    if os.path.exists( db ):
        os.unlink( db )
    # create table
    con = sqlite3.connect( db )    
    con.execute( tb_sql )       
    con.commit()
    con.close()
