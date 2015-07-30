**本工具包将一些常用的网页分类不同语言的相关开源软件，如ictclas，BeautifulSoup，libsvm等进行封装组合，以方便用python进行网页分类相关程序的开发。**

# uitl:一些常用的开源软件包
## ictclas:中文分词，包含词频统计，关键词提取，指纹提取等功能。不同的机器上使用，需要重新编译。

## ictclas.py:我对ictclas的python封装(其实就是简单的用python调用ictclas)
> 使用说明：
> from mypack.util.ictclas import ICTclas
> ic = ICTclas( text )
> ic.finger() #返回text的指纹
> ic.words()  #返回list:[(word,num),(word,num),...]

## smallseg:一个轻量级开源python分词程序
> 使用说明：
> from mypack.util.smallseg.myseg import seg
> word\_nums = seg( text ) #返回list:[(word,num),(word,num),...]

## htmlproc:一些常用的html处理程序

### BeautifulSoup.py  开源的html析取程序,网上文档:http://www.crummy.com/software/BeautifulSoup/documentation.zh.html

### chardet 自动编码检测与转换

### parser.py 对以上两个的封装
> 使用说明:
> pr = Parser()
> > if pr.parse( url ):
> > > print pr.get\_html() #返回网页的html格式
> > > print pr.get\_text().encode('utf-8') #返回网页中的字符串
### crawl.py 使用pycurl的单个网页爬取程序,由于pycurl速度并不比urllib快，所以没啥用

# classify:文本分类模块说明

## preprocess

### chi:卡方特征选择

#### input:
  1. df\_tb

> > 格式如下,book为word在book类的文档频率(int)，total为各类的df之和，为word的总df：
> > word|book|edu|finance|house|mil|sport|car|ent|game|lady|mobile|tech|total

> 2. min\_df

### tfidf:计算tfidf

### 使用说明
  1. config.py中设置所有的变量
> 2. 执行db/create.py，创建数据库表
> 3. 爬取url
> 4. 执行chi模块：去低频词、卡方值计算、idf值计算
> from mypack.classfiy.preprocess.chi import chi\_compute
> chi\_compute()
> 5. 执行卡方特征选择，构建新字典
> from mypack.classify.preprocess.voca import read\_voca,transform\_samples
> voca = read\_voca()
> transform\_samples( voca )
> 6. 预测
> from mypack.classify.svm.predict import classify\_text#对文本进行分类
> from mypack.classify.svm.predict import classify\_text#对url进行分类

## svm 里面有个predict.py，就是用svm来对网页进行分类，字典和已经训练好的svm 模型放在data/下
> 如果要自己训练的话，自己下libsvm。liblinear用python不方便调用。

# web\_content\_extract  网页正文提取

## 使用说明
> from mypack.web\_content\_extract.extract import Extractor
> extr = Extractor( url )
> if extr.is\_content\_page():   #判断是否是正文页面
> > text = extr.get\_content()   # 提取正文

> html = extr.get\_content\_with\_format() #带html标签的正文
> > images = extr.get\_images()  # 提取正文中的图片
> > title = extr.get\_title()    # 提取正文的标题
> > confidence = extr.get\_confidence() #是正文的置信度
> > extr.get\_detail()#详细分析信息

# NOTICE
## ictclas使用前，需要先编译，如果是64位平台，先 ln -s ictclas ictclas64
## libsvm.so 64位平台,需要先下载好libsvm，重新编译libsvm.so替换原来的