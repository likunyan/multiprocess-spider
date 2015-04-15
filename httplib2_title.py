#coding:utf-8
from urllib2 import Request, urlopen, URLError, HTTPError
import chardet
import httplib2
import sys
import re
import socket
import time
httplib2.socket.setdefaulttimeout(30)
#轮询主机列表
for line in open("host"):
  #替换 轮询主机列表 每行结果的换行 为空白
  line=line.replace("\n","")
  req = Request("http://"+line)
  try:
    #请求状态 
    response = urlopen(req)
    #等待200毫秒，以免服务器挂掉连接
    #time.sleep(0.2)
  except Exception,e:
    output=open(result,'a')
    output.write("url_Error"+str(e)+" http://"+line+"\n")
  else:
    #模拟访问网站
    #html_1 = urllib2.urlopen('http://'+line).read()
    h = httplib2.Http(".cache")
    resp, html_1 = h.request('http://'+line, "GET")
    #time.sleep(0.2)
    #编码
    encoding_dict = chardet.detect(html_1)
    web_encoding = encoding_dict['encoding']
    #判断编码是否为UTF-8
    if web_encoding == 'utf-8' or web_encoding == 'UTF-8':
      html=html_1
      #如果源码中有百家乐
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
