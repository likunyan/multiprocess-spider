#coding=utf-8
#!/usr/bin/python
#python爬虫1.1 beta 加入多进程 进程数量可以在后面自己添加下，暂时还没改好让使用者输入数字为多进程的数量
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
#urllib2.socket.setdefaulttimeout(60) #Python2.6以前的版本

exitFlag = 0
class myThread (threading.Thread):   #继承父类threading.Thread
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):      #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        #插入旧版本的python爬虫(1.0)开始 #修改了两处地方
        file=str(self.name)  #转为string类型
        result=self.name+"-result"  #多(N)进程的执行结果保存到各自的result文件中去
        for line in open(file):  #轮询self*文件中的网址
            line=line.replace("\n","")  #替换上一步中，轮询到的每行结果中的换行字符为空白
            req = "http://"+line
            try:
                response = urlopen(req)
                #time.sleep(N)  #等待N(N值暂未测量)毫秒，以免Web服务器频繁挂掉连接
            except Exception,e:
                output=open(result,'a')
                output.write("url_Error "+str(e)+" http://"+line+"\n")
            else:
                try:
                    html_1 = urllib2.urlopen('http://'+line,timeout=60).read()
                except Exception,x:
                    output=open(result,'a')
                    output.write("http_Error "+str(x)+" http://"+line+"\n")
                else:
                    data = urllib.urlopen(req).read()
                    target =str(chardet.detect(data))
                    #print target
                    bianma = ["ISO-8859-2","utf"]
                if bianma[0] in target.lower() or bianma[1] in target.lower():
                    #print "Yes,It's utf-8"
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
                    #print m  #如果标题不为空 则真，否则为假
                    #if m:
                        #print m.group()
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
                    #print "No utf8 "
                    html = html_1.decode('gbk','ignore').encode('utf-8')
                    html=string.replace(html,'\r\n','');
                    html=string.replace(html,'\n','');
                    m=re.search(r'<title>(.*?)</title>', html, flags=re.I)
                    #if m:
                        #print m.group()
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
#插入旧版本的python爬虫(1.0)结束
# 创建新线程
thread1 = myThread(1, "self00")
thread2 = myThread(2, "self01")
thread3 = myThread(3, "self02")
thread4 = myThread(4, "self03")
thread5 = myThread(5, "self04")
thread6 = myThread(6, "self05")
thread7 = myThread(7, "self06")
thread8 = myThread(8, "self07")
# 开启线程
thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread5.start()
thread6.start()
thread7.start()
thread8.start()
