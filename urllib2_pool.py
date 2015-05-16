#coding=utf-8
#!/usr/bin/python
#进程数量、任务数这两个可以在末尾代码修改下
from urllib2 import Request, urlopen, URLError, HTTPError
from multiprocessing import Pool
import os
import chardet        # 编码转换用
import sys
import string
import urllib2
import re        # 正则
import time
# import socket
# urllib2.socket.setdefaulttimeout(60) # Python2.6以前的版本

def myPool(source_file_name):
    def myPoolmain(line):
        line = line.replace("\n", "")        # 替换上一步中，轮询到的每行结果中的换行字符为空白
        req_url = "http://"+line        # 因为self*的域名是不带http://的，这边加下
        
        try:
            response_of_req_url = urlopen(req_url)
        except Exception, e:
            with open(result_file_name, 'a') as output:
                output.write("url_Error "+str(e)+" "+req_url+"\n")
            return 0
        except: print "0"        # beta版本代码	
        else:
            try: html = urllib2.urlopen(req_url, timeout=60).read()        # 请求网址，超时时间60秒
            except Exception, x:
                # 保存错误到文件中去
                with open(result_file_name, 'a') as output:
                    output.write("http_Error "+str(x)+" "+req_url+"\n")
            except:
                print "1"        # beta版本代码
            else:
                coding = str(chardet.detect(html))
                #print coding
                isUTF8 = ["ISO-8859-2", "utf"]
                if isUTF8[0] in coding.lower() or isUTF8[1] in coding.lower():
                    #print "Yes,It's utf8"
                    htmlIsutf8 = html
                    if "百家乐" in htmlIsutf8:
                        with open(result_file_name, 'a') as output:
                            output.write("违规信息-百家乐"+" "+req_url+"\n")
                    elif "太阳城" in htmlIsutf8:
                        with open(result_file_name, 'a') as output:
                            output.write("违规信息-太阳城"+" "+req_url+"\n")
                    # 因为有的标题是多行的，保存起来有问题，所以这边去掉一切换行
                    htmlIsutf8 = string.replace(htmlIsutf8, '\r\n', '');
                    htmlIsutf8 = string.replace(htmlIsutf8, '\n', '');
                    m = re.search(r'<title>(.*?)</title>', htmlIsutf8, flags=re.I)
                    # print m        #如果标题不为空 则真，否则为假
                    # if m:
                        #print m.group()
                    if m:
                        with open(result_file_name, 'a') as output:
                            output.write(m.group(1)+" "+req_url+"\n")
                        # print htmlIsutf8;
                    else:  # 特殊标题的标记
                        # <title xmlns=...><title> 个人用
                        m = re.search(r'<title xmlns="">(.*)</title>', htmlIsutf8, flags=re.I)
                        if m:
                            with open(result_file_name, 'a') as output:
                                output.write(m.group(1)+" "+req_url+"\n")
                            # print htmlIsutf8;
                        else:
                            with open(result_file_name, 'a') as output:
                                output.write("error"+" "+req_url+"\n")
                else:
                    # print "No utf8 "
                    htmlNoutf8 = html.decode('gbk', 'ignore').encode('utf-8')
                    htmlNoutf8 = string.replace(htmlNoutf8, '\r\n', '');
                    htmlNoutf8 = string.replace(htmlNoutf8, '\n', '');
                    m = re.search(r'<title>(.*?)</title>', htmlNoutf8, flags=re.I)
                    # if m:
                        # print m.group()
                    if "百家乐" in htmlNoutf8:
                        with open(result_file_name, 'a') as output:
                            output.write("违规信息-百家乐"+" "+req_url+"\n")
                    elif "太阳城" in htmlNoutf8:
                        with open(result_file_name, 'a') as output:
                            output.write("违规信息-太阳城"+" "+req_url+"\n")
                    if m:  # 如果标题不为空 则真，否则为假
                        with open(result_file_name, 'a') as output:
                            output.write(m.group(1)+" "+req_url+"\n")
                        # print htmlNoutf8;
                    else:
                        m = re.search(r'<title xmlns="">(.*)</title>', htmlNoutf8, flags = re.I)
                        if m:
                            with open(result_file_name, 'a') as output:
                                output.write(m.group(1)+" "+req_url+"\n")
                        else:
                            with open(result_file_name, 'a') as output:
                                output.write("error"+" "+req_url+"\n")
                                
    print "进程"+source_file_name+"开始"
    # 以下两行引用文件和输出文件!
    source_file = source_file_name        # 这边定义下两行要打开的源文件
    result_file_name = source_file_name+"-result"  # 多(N)进程的执行结果保存到各自的result结果文件中去
    
    for line in open(source_file):        # 轮询源文件中的网址
        host_value = line.split()        # 用空格分割字符串，并保存到列表
        status = myPoolmain(host_value[0])
        # 如果source_file_name这个文本中第一列的网址能够访问的话，执行第二列中的网址
        if status == 0:  myPoolmain(host_value[1])
        
    print "进程"+source_file_name+"结束"
    
if __name__=='__main__':
    print 'Parent process %s.' % os.getpid()
    p = Pool(1)        # at the same time,running number # 同时运行的数目
    task_list_num = 1        # alignment number # 列队中的数目
    
    for i in xrange(task_list_num):
        if task_list_num < 10:
            p.apply_async(myPool, args=("self"+str(i),))
        elif task_list_num < 100:
            if i < 10:
                p.apply_async(myPool, args=("self0"+str(i),))
            else:
                p.apply_async(myPool, args=("self"+str(i),))        # that is 10 < i < 100
        elif task_list_num < 1000:
            if i < 10:
                p.apply_async(myPool, args=("self00"+str(i),))
            elif i < 100:
                p.apply_async(myPool, args=("self0"+str(i),))
            else:
                p.apply_async(myPool, args=("self"+str(i),))        # that is 100 < i < 1000
        elif task_list_num < 10000:
            if i < 10:
                p.apply_async(myPool, args=("self000"+str(i),))
            elif i < 100:
                p.apply_async(myPool, args=("self00"+str(i),))
            elif i < 1000:
                p.apply_async(myPool, args=("self0"+str(i),))
            else:
                p.apply_async(myPool, args=("self"+str(i),))        # that is 1000 < i < 10000
        else:
            print "tasklist number over 1W! # 队列数目超过1W"
            
    print 'Waiting for all subprocesses done...'
    p.close()
    p.join()
    os.system("amh mysql start")
    print 'All subprocesses done.'
