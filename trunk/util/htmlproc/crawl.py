#coding=utf8
# crawl.py  还算上urllib爬来得快，不要用这个了！
# Usage:
# from util.htmlproc.crawl import craw_url 
# html = craw_url( url )
import pycurl
from cStringIO import StringIO

def crawl_url( url ):
    '''return html of url,if exception,return None'''
    wf = StringIO()
    try:
        curl = pycurl.Curl()
        curl.setopt(pycurl.URL, url)
        curl.setopt(pycurl.WRITEFUNCTION, wf.write)
        curl.setopt(pycurl.FOLLOWLOCATION, 1)
        curl.setopt(pycurl.MAXREDIRS, 5)
        curl.setopt(pycurl.USERAGENT, "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; InfoPath.2)")
        #curl.setopt(pycurl.CONNECTTIMEOUT, 60)
        curl.setopt(pycurl.TIMEOUT, 300)
        #curl.setopt(pycurl.NOSIGNAL, 1)
        curl.perform()
        data = wf.getvalue()
        wf.close()
        return data
    except Exception, e:
        print "curl.perform() Exception : %s" % e
        return None
