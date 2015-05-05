#coding=utf-8
#!/usr/bin/python
from urllib2 import Request, urlopen, URLError, HTTPError
import chardet
import sys
import string
import urllib2
import urllib
import re
import time
import socket
import threading  #多进程用
urllib2.socket.setdefaulttimeout(30)
#python爬虫1.1 beta 加入多进程 为8进程
exitFlag = 0

class myThread (threading.Thread):   #继承父类threading.Thread
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):           #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
#插入python爬虫 1.0开始
        file=str(self.name)  #tmp，转为string类型
        result="result"
        for line in open(file):  #轮询主机列表
          line=line.replace("\n","")  #替换 轮询主机列表 每行结果的换行 为空白
          req = "http://"+line
          try:
            response = urlopen(req)
            #time.sleep(200)  #等待200毫秒，以免Web服务器频繁挂掉连接
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
            if bianma[0] in target.lower() or bianma[1] in target.lower():
              print "Yes,It's utf-8"
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
              print m  #如果标题不为空 则真，否则为假
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
              print "No utf8 "
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
              if m:  #如果标题不为空 则真，否则为假
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
#插入python爬虫 2.0开始
# 创建新线程
thread1 = myThread(1, "self0")
thread2 = myThread(2, "self1")
thread3 = myThread(3, "self2")
thread4 = myThread(4, "self3")
thread1 = myThread(5, "self4")
thread2 = myThread(6, "self5")
thread3 = myThread(7, "self6")
thread4 = myThread(8, "self7")
# 开启线程
thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread5.start()
thread6.start()
thread7.start()
thread8.start()
