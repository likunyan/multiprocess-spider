#coding=utf-8
#!/usr/bin/python
#进程数量可以在后面自己修改下
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
from multiprocessing import Pool
import os
def myPool(name):
        #插入旧版本的python爬虫(1.0)开始 #修改了两处地方
        print "进程"+name+"开始"
        # 引用文件和输出文件!
        file = name  # 转为string类型
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
                                #print htmlNoutf8;
                            else:
                                 with open(resultFile, 'a') as output:
                                    output.write("error"+" "+reqUrl+"\n")
        print "进程"+name+"结束"
        #插入旧版本的python爬虫(1.0)结束
if __name__=='__main__':
    print 'Parent process %s.' % os.getpid()
    p = Pool(40)  #同时运行的数目
    for i in range(99):  #队列中的数目
        if i < 10:
            p.apply_async(myPool, args=("self0"+str(i),))
        else:
            p.apply_async(myPool, args=("self"+str(i),))
    print 'Waiting for all subprocesses done...'
    p.close()
    p.join()
    print 'All subprocesses done.'
