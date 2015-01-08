#coding:utf-8
from urllib2 import Request, urlopen, URLError, HTTPError
import chardet
import sys
import string
import urllib2
import urllib
import re
import time
import socket
urllib2.socket.setdefaulttimeout(30)
#轮询主机列表
result="result0.txt"
for line in open("host0"):
  #替换 轮询主机列表 每行结果的换行 为空白
  line=line.replace("\n","")
  req = "http://"+line
  try:
    response = urlopen(req)
    #time.sleep(200)
    #等待200毫秒，以免服务器挂掉连接
  except Exception,e:
    output=open(result,'a')
    output.write("url_Error"+str(e)+" http://"+line+"\n")
  else:
   try:
    html_1 = urllib2.urlopen('http://'+line).read()
   except Exception,x:
    output=open(result,'a')
    output.write("http_Error"+str(x)+" http://"+line+"\n")
   else:
    data = urllib.urlopen(req).read()
    target =str(chardet.detect(data))
    print target
    bianma = ["ISO-8859-2","utf"]
    if bianma[0] or bianma[1] in target.lower():
      print "yes"
      html=html_1
      if "百家乐" in html:
        output=open(result,'a')
        output.write("违规信息-百家乐"+" http://"+line+"\n")
      elif "太阳城" in html:
        output=open(result,'a')
        output.write("违规信息-太阳城"+" http://"+line+"\n")
      html=string.replace(html,'\r\n','');
      html=string.replace(html,'\n','');
      m=re.search(r'<title>(.*?)</title>', html, flags=re.I)
      #如果标题不为空 则真，否则为假
      print m
      if m:
       print m.group()
      if m:
        output=open(result,'a')
        output.write(m.group(1)+" http://"+line+"\n")
        #print html;
      else:
        m=re.search(r'<title xmlns="">(.*)</title>', html, flags=re.I)
        if m:
          output=open(result,'a')
          output.write(m.group(1)+" http://"+line+"\n")
          #print html;
        else:
          output=open(result,'a')
          output.write("error"+" http://"+line+"\n")
    else :
      html = html_1.decode('gbk','ignore').encode('utf-8')
      html=string.replace(html,'\r\n','');
      html=string.replace(html,'\n','');
      m=re.search(r'<title>(.*?)</title>', html, flags=re.I)
      if m:
       print m.group()
      if "百家乐" in html:
        output=open(result,'a')
        output.write("违规信息-百家乐"+" http://"+line+"\n")
      elif "太阳城" in html:
        output=open(result,'a')
        output.write("违规信息-太阳城"+" http://"+line+"\n")
      #如果标题不为空 则真，否则为假
      if m:
        output=open(result,'a')
        output.write(m.group(1)+" http://"+line+"\n")
        #print html;
      else:
        m=re.search(r'<title xmlns="">(.*)</title>', html, flags=re.I)
        if m:
          output=open(result,'a')
          output.write(m.group(1)+" http://"+line+"\n")
          #print html;
        else:
          output=open(result,'a')
          output.write("error"+" http://"+line+"\n")
