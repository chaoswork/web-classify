#coding=utf8
# config.py 一些配置信息

CATES = ('book','edu','finance','house','mil','sport','car','ent','game','lady','mobile','tech')

NUM_CATES = len( CATES )
NUM_WORDS = 72641
#user-defined
MIN_NUM = 2                     # >=MIN_NUM will be selected
GSS_TOP = 5000

RAW_DOCS_DIR = 'raw_data/'
WF_FILE = 'data/wf.txt'

DATA_FILE = 'old_data/svm.data'
WORDS_FILE = 'old_data/words.txt'
TSR1_FILE = 'data/words_num_%d.txt' % MIN_NUM
TSR2_FILE = 'data/words_chi.txt'
NEW_DICT_FILE = 'data/new_dict.txt'
NEW_DOCS_FILE = 'data/new_docs.txt'
TFIDF_FILE = 'data/tfidf.txt'
