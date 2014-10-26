#coding:utf-8
from urllib2 import Request, urlopen, URLError, HTTPError
import chardet
import sys
import urllib2
import re
import time
#轮询主机列表
for line in open("host"):
  #替换 轮询主机列表 每行结果的换行 为空白
  line=line.replace("\n","")
  req = Request("http://"+line)
  try:
    response = urlopen(req)
    #等待200毫秒，以免服务器挂掉连接
     time.sleep(0.2)
  except HTTPError, e:
    output=open('result.txt','a')
    output.write("HTTPError"+str(e.code)+" "+line+"\n")
  except URLError, e:
    output=open('result.txt','a')
    output.write("URLError"+str(e.reason)+" "+line+"\n")
  else:
    html_1 = urllib2.urlopen('http://'+line,timeout=200).read()
     time.sleep(0.2)
    encoding_dict = chardet.detect(html_1)
    web_encoding = encoding_dict['encoding']
    if web_encoding == 'utf-8' or web_encoding == 'UTF-8':
      html=html_1
      if "百家乐" in html:
        output=open('result.txt','a')
        output.write("baijiale"+" "+line+"\n")
      elif "太阳城" in html:
        output=open('result.txt','a')
        output.write("taiyangcheng"+" "+line+"\n")
      m=re.search(r'<title>(.*)</title>', html, flags=re.I)
      #如果标题不为空 则真，否则为假
      if m:
        output=open('result.txt','a')
        output.write(m.group(1)+line+"\n")
        #print html
      else:
        output=open('result.txt','a')
        output.write("error"+" "+line+"\n")
    else :
      html = html_1.decode('gbk','ignore').encode('utf-8')
      m=re.search(r'<title>(.*)</title>', html, flags=re.I)
      if "百家乐" in html:
        output=open('result.txt','a')
        output.write("baijiale"+" "+line+"\n")
      elif "太阳城" in html:
        output=open('result.txt','a')
        output.write("taiyangcheng"+" "+line+"\n")
      #如果标题不为空 则真，否则为假
      if m:
        output=open('result.txt','a')
        output.write(m.group(1)+line+"\n")
        #print html;
      else:
        output=open('result.txt','a')
        output.write("error"+" "+line+"\n")
