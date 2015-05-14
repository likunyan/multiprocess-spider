#coding=utf-8
#!/usr/bin/python
#进程数量、任务数这两个可以在末尾代码修改下
from urllib2 import Request, urlopen, URLError, HTTPError
from multiprocessing import Pool
import os
import chardet  # 编码转换用
import sys
import string
import urllib2
import re  # 正则
import time
# import socket
# urllib2.socket.setdefaulttimeout(60) # Python2.6以前的版本

def myPool(name):
        print "进程"+name+"开始"
        # 以下两行引用文件和输出文件!
        file = name
        resultFile = name+"-result"  # 多(N)进程的执行结果保存到各自的result文件中去
        for line in open(file):  # 轮询self*文件中的网址
            line = line.replace("\n", "")  # 替换上一步中，轮询到的每行结果中的换行字符为空白
            reqUrl = "http://"+line  # 因为self*的域名是不带http://的，这边加下
            try:  # 试着...
                response = urlopen(reqUrl)
                #time.sleep(N)  #等待N(N值暂未测量)秒，以免Web服务器频繁挂掉连接
            except Exception, e:
                with open(resultFile, 'a') as output:
                    output.write("url_Error "+str(e)+" "+reqUrl+"\n")
            except:  # beta版本代码
                print "0"
            else:
                try:  # 请求网址，超时时间60秒
                    html = urllib2.urlopen(reqUrl, timeout=60).read()
                except Exception, x:
                    # 保存错误到文件中去
                    with open(resultFile, 'a') as output:
                        output.write("http_Error "+str(x)+" "+reqUrl+"\n")
                except:  # beta版本代码
                    print "1"
                else:
                    coding = str(chardet.detect(html))
                    #print coding
                    isUTF8 = ["ISO-8859-2", "utf"]
                    if isUTF8[0] in coding.lower() or isUTF8[1] in coding.lower():
                        #print "Yes,It's utf8"
                        htmlIsutf8 = html
                        if "百家乐" in htmlIsutf8:
                            with open(resultFile, 'a') as output:
                                output.write("违规信息-百家乐"+" "+reqUrl+"\n")
                        elif "太阳城" in htmlIsutf8:
                            with open(resultFile, 'a') as output:
                                output.write("违规信息-太阳城"+" "+reqUrl+"\n")
                        # 因为有的标题是多行的，保存起来有问题，所以这边去掉一切换行
                        htmlIsutf8 = string.replace(htmlIsutf8, '\r\n', '');
                        htmlIsutf8 = string.replace(htmlIsutf8, '\n', '');
                        m = re.search(r'<title>(.*?)</title>', htmlIsutf8, flags=re.I)
                        #print m  #如果标题不为空 则真，否则为假
                        #if m:
                            #print m.group()
                        if m:
                            with open(resultFile, 'a') as output:
                                output.write(m.group(1)+" "+reqUrl+"\n")
                            #print htmlIsutf8;
                        else:  # 特殊标题的标记
                            # <title xmlns=...><title> 个人用
                            m = re.search(r'<title xmlns="">(.*)</title>', htmlIsutf8, flags=re.I)
                            if m:
                                with open(resultFile, 'a') as output:
                                    output.write(m.group(1)+" "+reqUrl+"\n")
                                #print htmlIsutf8;
                            else:
                                with open(resultFile, 'a') as output:
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
                            with open(resultFile, 'a') as output:
                                output.write("违规信息-百家乐"+" "+reqUrl+"\n")
                        elif "太阳城" in htmlNoutf8:
                            with open(resultFile, 'a') as output:
                                output.write("违规信息-太阳城"+" "+reqUrl+"\n")
                        if m:  # 如果标题不为空 则真，否则为假
                            with open(resultFile, 'a') as output:
                                output.write(m.group(1)+" "+reqUrl+"\n")
                            # print htmlNoutf8;
                        else:
                            m = re.search(r'<title xmlns="">(.*)</title>', htmlNoutf8, flags=re.I)
                            if m:
                                with open(resultFile, 'a') as output:
                                    output.write(m.group(1)+" "+reqUrl+"\n")
                            else:
                                 with open(resultFile, 'a') as output:
                                    output.write("error"+" "+reqUrl+"\n")
        print "进程"+name+"结束"
if __name__=='__main__':
    print 'Parent process %s.' % os.getpid()
    p = Pool(40)  #同时运行的数目
    taskListnum = 1000
    for i in range(taskListnum):  #队列中的数目
        if taskListnum < 100
            if i < 10:
                p.apply_async(myPool, args=("self0"+str(i),))
            elif:  # 即 10 < i < 100
                p.apply_async(myPool, args=("self"+str(i),))
        elif taskListnum < 1000:
            if i < 10:
                p.apply_async(myPool, args=("self00"+str(i),))
            elif i < 100:
                p.apply_async(myPool, args=("self0"+str(i),))
            else :  # 即 100 < i < 1000
                p.apply_async(myPool, args=("self"+str(i),))
        elif taskListnum < 10000:
            if i < 10:
                p.apply_async(myPool, args=("self000"+str(i),))
            elif i < 100:
                p.apply_async(myPool, args=("self00"+str(i),))
            elif i < 1000: 
                p.apply_async(myPool, args=("self0"+str(i),))
            else:   # 即 1000 < i < 10000
                p.apply_async(myPool, args=("self"+str(i),))
        else:
            print "任务数超过1W!"
    print 'Waiting for all subprocesses done...'
    p.close()
    p.join()
    print 'All subprocesses done.'
