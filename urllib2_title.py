#coding=utf-8
#!/usr/bin/python
#python爬虫1.1 beta 加入多进程 进程数量可以在后面自己添加下，暂时还没改好让使用者输入数字为多进程的数量
from urllib2 import Request, urlopen, URLError, HTTPError
import chardet  # 编码转换用
import sys
import string
import urllib2
#import urllib  #使用urllib2，这个没有使用到
import re  # 正则
import time
# import socket
# urllib2.socket.setdefaulttimeout(60) # Python2.6以前的版本
import threading  # 多进程用


exitFlag = 0
class myThread (threading.Thread):  # 继承父类threading.Thread
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):      # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        #插入旧版本的python爬虫(1.0)开始 #修改了两处地方
        print "进程"+str(self.threadID)+"开始"
        file = str(self.name)  # 转为string类型
        resultFile = self.name+"-result"  # 多(N)进程的执行结果保存到各自的result文件中去
        for line in open(file):  # 轮询self*文件中的网址
            line = line.replace("\n", "")  # 替换上一步中，轮询到的每行结果中的换行字符为空白
            reqUrl = "http://"+line  # 因为self*的域名是不带http://的，这边加下
            try:  # 试着...
                response = urlopen(reqUrl)
                #time.sleep(N)  #等待N(N值暂未测量)毫秒，以免Web服务器频繁挂掉连接
            except Exception, e:
                output = open(resultFile, 'a')
                output.write("url_Error "+str(e)+" "+reqUrl+"\n")
            except:
                print "0"
            else:
                try:  # 请求网址，超时时间60秒
                    html = urllib2.urlopen(reqUrl, timeout=60).read()
                except Exception, x:
                      # 保存错误到文件中去
                    output = open(resultFile, 'a')
                    output.write("http_Error "+str(x)+" "+reqUrl+"\n")
                except:
                    print "1"
                else:
                    coding = str(chardet.detect(html))
                    #print coding
                    isUTF8 = ["ISO-8859-2", "utf"]
                    if isUTF8[0] in coding.lower() or isUTF8[1] in coding.lower():
                        #print "Yes,It's utf8"
                        htmlIsutf8 = html
                        if "百家乐" in htmlIsutf8:
                            output = open(resultFile, 'a')
                            output.write("违规信息-百家乐 "+reqUrl+"\n")
                        elif "太阳城" in htmlIsutf8:
                            output = open(resultFile, 'a')
                            output.write("违规信息-太阳城 "+reqUrl+"\n")
                        # 因为有的标题是多行的，保存起来有问题，所以这边去掉一切换行
                        htmlIsutf8 = string.replace(htmlIsutf8, '\r\n', '');
                        htmlIsutf8 = string.replace(htmlIsutf8, '\n', '');
                        m = re.search(r'<title>(.*?)</title>', htmlIsutf8, flags=re.I)
                        #print m  #如果标题不为空 则真，否则为假
                        #if m:
                            #print m.group()
                        if m:
                            output = open(resultFile, 'a')
                            output.write(m.group(1)+" "+reqUrl+"\n")
                            #print htmlIsutf8;
                        else:  # 特殊标题的标记
                            m = re.search(r'<title xmlns="">(.*)</title>', htmlIsutf8, flags=re.I)
                            if m:
                                output = open(resultFile, 'a')
                                output.write(m.group(1)+" "+reqUrl+"\n")
                                #print htmlIsutf8;
                            else:
                                output = open(resultFile, 'a')
                                output.write("error"+" "+reqUrl+"\n")
                    else:
                        #print "No utf8 "
                        htmlNoutf8 = html.decode('gbk', 'ignore').encode('utf-8')
                        htmlNoutf8 = string.replace(htmlNoutf8, '\r\n', '');
                        htmlNoutf8 = string.replace(htmlNoutf8, '\n', '');
                        m = re.search(r'<title>(.*?)</title>', htmlNoutf8, flags=re.I)
                        #if m:
                            #print m.group()
                        if "百家乐" in htmlNoutf8:
                            output = open(resultFile, 'a')
                            output.write("违规信息-百家乐"+" "+reqUrl+"\n")
                        elif "太阳城" in htmlNoutf8:
                            output = open(resultFile, 'a')
                            output.write("违规信息-太阳城"+" http://"+line+"\n")
                        if m:  # 如果标题不为空 则真，否则为假
                            output = open(resultFile, 'a')
                            output.write(m.group(1)+" "+reqUrl+"\n")
                            # print htmlNoutf8;
                        else:
                            m = re.search(r'<title xmlns="">(.*)</title>', htmlNoutf8, flags=re.I)
                            if m:
                                output = open(resultFile, 'a')
                                output.write(m.group(1)+" "+reqUrl+"\n")
                                #print htmlNoutf8;
                            else:
                                output = open(resultFile, 'a')
                                output.write("error"+" "+reqUrl+"\n")
        print "进程"+str(self.threadID)+"结束"
        #插入旧版本的python爬虫(1.0)结束
createVar = locals()
listTemp = range(0,41)  # 40进程
for i in enumerate(listTemp):
    # 因为使用split -a 2 -d -l 168 urlFile self
    # 所以文件名是self00,self01,......,self09,self10,self11,......
    if i < 10:
        myThread(i, "self0"+str(i)).start()
    else:
        myThread(i, "self"+str(i)).start()
