#coding=utf8
# config.py 一些配置信息

### COMMAN
CATES =  ('book','edu','finance','house','mil','sport','car','ent','game','lady','mobile','tech')
NUM_CATES = len( CATES )

### CLIENT
URLS_DB = 'urls.db'
# task
TASK1_TIMEOUT = 600              # 第一个任务的单个执行期限是600s
# threshold
TRAIN_URLS = 2000               # 每个类用来训练的url数目,-1为所有的
TH_LOCAL_TSR = 1                # 局部特征选择时的最低词频
TH_GLOBAL_TSR = 2               # 全局去低频词中所保留的最低词频
TOP_CHI = 10000                 # 全局开方特征选择的词数

#file
TASK1_RESULT_DB = '../db/task1_result.db' # 存储第一个task的返回结果，即词的各类df
RAW_WORDS_TB = 'df_word_tb'
CHI_DB = '../db/chi.db'
CHI_TB = 'chi_tb'

#### WORKER
RAW_DOC_DIR = 'pages'           # 爬取、分词以及局部低频词过滤后的网页存放目录

# data format,主要分割符:\t , :。由于有的词中含有':',当使用':'时，需要先去除这些词
# 1.url_cate:from client to worker as job.arg
#        url\tcate\n
# 2.doc_[jobid].txt:worker stored after ictclas 
#        tech\tword1:num,word2:num,...
# 3.df matrix:from worker return to client
#        cate1_num,cate2_num,...\nword\tcate1_num,cate2_num,...,all_num
