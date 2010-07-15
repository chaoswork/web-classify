#coding=utf8
#config.py for chi,tfidf
import os
from mypack.util.logger import Logger

#LOG_FILE = 'client.log'
log = Logger().logger

# 分类的类别,为直观，此时尚不采用数字表示
CATES =  ('book','edu','finance','house','mil','sport','car','ent','game','lady','mobile','tech')

# for chi
MIN_DF = 50               # 全局去低频词中所保留的最低词频
CLASSIFY_DIR = os.path.dirname(os.path.realpath(__file__)) #classify目录

DB = CLASSIFY_DIR+'/db/test.db'                  # 所有的表都存到这个db

# 词的文档频率表
# 格式如下,book为word在book类的文档频率(int)，total为各类的df之和，为word的总df：
#  word|book|edu|finance|house|mil|sport|car|ent|game|lady|mobile|tech|total
# 更多，请参见db/__init__.py中的数据库建表语句
DF_TB = 'df_tb'

# 词的开方值以及idf值表
# 格式：
# word|book|edu|finance|house|mil|sport|car|ent|game|lady|mobile|tech|idf
# word之后的各列为chi(float)值，最后一列为idf(float)值
# 更多，请参见db/__init__.py中的数据库建表语句
CHI_TB = 'chi_tb'
MIN_CHI = 3.84                  # 每个类特征选择时最小的卡方值

# 经过卡方特征选择后的字典文件
# 格式: word     idf
VOCA_FILE = CLASSIFY_DIR+'/data/voca.txt'    

# 原始样本数据
# 数据格式:cate word:num,word:num,...
SAMPLE_FILE = CLASSIFY_DIR+'/data/last_docs.txt'

######### from svm ##################
SVM_MODEL = CLASSIFY_DIR+'/data/svm.model'
