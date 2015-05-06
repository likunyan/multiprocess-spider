#coding=utf-8
#!/usr/bin/python
#python爬虫1.1 beta 加入多进程 进程数量可以在后面自己添加下，暂时还没改好让使用者输入数字为多进程的数量
from urllib2 import Request, urlopen, URLError, HTTPError
import chardet  #编码转换用
import sys
import string
import urllib2
#import urllib  #使用urllib2，这个没有使用到
import re  #正则
import time
#import socket 
#urllib2.socket.setdefaulttimeout(60) #Python2.6以前的版本
import threading  #多进程用


exitFlag = 0
class myThread (threading.Thread):   #继承父类threading.Thread
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):      #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        #插入旧版本的python爬虫(1.0)开始 #修改了两处地方
        file=str(self.name)  #转为string类型
        resultFile=self.name+"-result"  #多(N)进程的执行结果保存到各自的result文件中去
        for line in open(file):  #轮询self*文件中的网址
            line=line.replace("\n","")  #替换上一步中，轮询到的每行结果中的换行字符为空白
            reqUrl = "http://"+line  #因为self*的域名是不带http://的，这边加下
            try:  #试着...
                response = urlopen(reqUrl)
                #time.sleep(N)  #等待N(N值暂未测量)毫秒，以免Web服务器频繁挂掉连接
            except Exception,e:
                output=open(resultFile,'a')
                output.write("url_Error "+str(e)+" "+reqUrl+"\n")
            except:
                print "0"
            else:
                try:
                    html = urllib2.urlopen(reqUrl,timeout=60).read()  #请求网址，超时时间60秒
                except Exception,x:
                    output=open(resultFile,'a')
                    output.write("http_Error "+str(x)+" "+reqUrl+"\n") #保存错误到文件中去
                except:
                    print "1"
                else:
                    coding =str(chardet.detect(html))
                    #print coding
                    isUTF8 = ["ISO-8859-2","utf"]
                    if isUTF8[0] in coding.lower() or isUTF8[1] in coding.lower():
                        #print "Yes,It's utf8"
                        htmlIsutf8=html
                        if "百家乐" in htmlIsutf8:
                            output=open(resultFile,'a')
                            output.write("违规信息-百家乐 "+reqUrl+"\n")
                        elif "太阳城" in htmlIsutf8:
                            output=open(resultFile,'a')
                            output.write("违规信息-太阳城 "+reqUrl+"\n")
                        htmlIsutf8=string.replace(htmlIsutf8,'\r\n','');  #因为有的标题是多行的，保存起来有问题，所以这边去掉一切换行
                        htmlIsutf8=string.replace(htmlIsutf8,'\n','');
                        m=re.search(r'<title>(.*?)</title>', htmlIsutf8, flags=re.I)
                        #print m  #如果标题不为空 则真，否则为假
                        #if m:
                            #print m.group()
                        if m:
                            output=open(resultFile,'a')
                            output.write(m.group(1)+" "+reqUrl+"\n")
                            #print htmlIsutf8;
                        else:  #特殊标题的标记
                            m=re.search(r'<title xmlns="">(.*)</title>', htmlIsutf8, flags=re.I)
                            if m:
                                output=open(resultFile,'a')
                                output.write(m.group(1)+" "+reqUrl+"\n")
                                #print htmlIsutf8;
                            else:
                                output=open(resultFile,'a')
                                output.write("error"+" "+reqUrl+"\n")
                    else :
                        #print "No utf8 "
                        htmlNoutf8 = html.decode('gbk','ignore').encode('utf-8')
                        htmlNoutf8=string.replace(htmlNoutf8,'\r\n','');
                        htmlNoutf8=string.replace(htmlNoutf8,'\n','');
                        m=re.search(r'<title>(.*?)</title>', htmlNoutf8, flags=re.I)
                        #if m:
                            #print m.group()
                        if "百家乐" in htmlNoutf8:
                            output=open(resultFile,'a')
                            output.write("违规信息-百家乐"+" "+reqUrl+"\n")
                        elif "太阳城" in htmlNoutf8:
                            output=open(resultFile,'a')
                            output.write("违规信息-太阳城"+" http://"+line+"\n")
                        if m:  #如果标题不为空 则真，否则为假
                            output=open(resultFile,'a')
                            output.write(m.group(1)+" "+reqUrl+"\n")
                            #print htmlNoutf8;
                        else:
                            m=re.search(r'<title xmlns="">(.*)</title>', htmlNoutf8, flags=re.I)
                            if m:
                                output=open(resultFile,'a')
                                output.write(m.group(1)+" "+reqUrl+"\n")
                                #print htmlNoutf8;
                            else:
                                output=open(resultFile,'a')
                                output.write("error"+" "+reqUrl+"\n")
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
