#coding=utf-8
#!/usr/bin/python
'''
by 小李世界 lky216@gmail.com
'''
from urllib2 import Request, urlopen, URLError, HTTPError
from multiprocessing import Pool
import os
import chardet
import sys
import string
import urllib2
import re
import time
import sys
# import socket
# urllib2.socket.setdefaulttimeout(60) # Python2.6以前的版本

number_of_at_the_same_time_the_process = int(sys.argv[1])        #同时进程数
number_of_tasks = int(sys.argv[2])        # alignment number # 列队中的数目

def open_text_file(source_text_file):
    
    
    def spider(text_line):
        text_line = text_line.replace("\n", "")  # 替换上一步中，轮询到的每行结果中的换行字符为空白
        req_url = "http://"+text_line  # 因为source_text_file的域名是不带http://的，这边加下
        
        try:
            urlopen(req_url)
        except Exception, e:
            with open(result_text_file, 'a') as output:
                output.write("url_Error "+str(e)+" "+req_url+"\n")
            return 0
        else:
            try:
                html_source = urllib2.urlopen(req_url, timeout=60).read()
            except Exception, x:
                with open(result_text_file, 'a') as output:
                    output.write("http_Error "+str(x)+" "+req_url+"\n")
            else:
                coding = str(chardet.detect(html_source))
                utf8 = ["ISO-8859-2", "utf"]
                
                if utf8[0] in coding.lower() or utf8[1] in coding.lower():
                    source_is_utf8 = html_source
                    if "百家乐" in source_is_utf8:
                        with open(result_text_file, 'a') as output:
                            output.write("违规信息-百家乐"+" "+req_url+"\n")
                    elif "太阳城" in source_is_utf8:
                        with open(result_text_file, 'a') as output:
                            output.write("违规信息-太阳城"+" "+req_url+"\n")
                            
                    # 因为有的标题是多行的，保存起来有问题，所以这边去掉一切换行
                    source_is_utf8 = string.replace(source_is_utf8, '\r\n', '');
                    source_is_utf8 = string.replace(source_is_utf8, '\n', '');
                    title = re.search(r'<title>(.*?)</title>', source_is_utf8, flags=re.I)
                    #if m: # 如果标题不为空 则真，否则为假
                        #print title.group()
                    if title:
                        with open(result_text_file, 'a') as output:
                            output.write(title.group(1)+" "+req_url+"\n")
                    else:  # 特殊标题的标记
                        # <title xmlns=...><title> 个人用
                        title = re.search(r'<title xmlns="">(.*)</title>', source_is_utf8, flags=re.I)
                        if title:
                            with open(result_text_file, 'a') as output:
                                output.write(title.group(1)+" "+req_url+"\n")
                        else:
                            with open(result_text_file, 'a') as output:
                                output.write("error"+" "+req_url+"\n")
                else:
                    source_no_utf8 = html_source.decode('gbk', 'ignore').encode('utf-8')
                    source_no_utf8 = string.replace(source_no_utf8, '\r\n', '');
                    source_no_utf8 = string.replace(source_no_utf8, '\n', '');
                    title = re.search(r'<title>(.*?)</title>', source_no_utf8, flags=re.I)
                    if "百家乐" in source_no_utf8:
                        with open(result_text_file, 'a') as output:
                            output.write("违规信息-百家乐"+" "+req_url+"\n")
                    elif "太阳城" in source_no_utf8:
                        with open(result_text_file, 'a') as output:
                            output.write("违规信息-太阳城"+" "+req_url+"\n")
                            
                    if title:  # 如果标题不为空 则真，否则为假
                        with open(result_text_file, 'a') as output:
                            output.write(title.group(1)+" "+req_url+"\n")
                    else:
                        title = re.search(r'<title xmlns="">(.*)</title>', source_no_utf8, flags = re.I)
                        if title:
                            with open(result_text_file, 'a') as output:
                                output.write(title.group(1)+" "+req_url+"\n")
                        else:
                            with open(result_text_file, 'a') as output:
                                output.write("error"+" "+req_url+"\n")
                                
                                
    with open("log", 'a') as output:
        output.write("开始时间:"+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())+"\n")
    print "进程"+source_text_file+"开始"
    
    result_text_file = source_text_file+"-result"  # 执行结果以源文件名+result形式保存
    
    for text_line in open(source_text_file):  # 轮询源文件中的网址
        host_value = text_line.split() # 用空格分割字符串，并保存到列表
        status = spider(host_value[0])
        if status == 0: # 如果source_text_file这个文本中第一列的网址不能够访问的话，执行第二列中的网址
            spider(host_value[1])
            
    with open("log", 'a') as output:
        output.write("结束时间:"+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())+"\n")   
    print "进程"+source_text_file+"结束"
    
    
if __name__=='__main__':
    print 'Parent process %s.' % os.getpid()
    p = Pool(number_of_at_the_same_time_the_process)  # at the same time,running number # 同时运行的数目
    
    for i in xrange(number_of_tasks):
        if number_of_tasks < 10:
            p.apply_async(open_text_file, args=("self"+str(i),))
        elif number_of_tasks < 100:
            if i < 10:
                p.apply_async(open_text_file, args=("self0"+str(i),))
            else:  # that is 10 < i < 100
                p.apply_async(open_text_file, args=("self"+str(i),))
                
        elif number_of_tasks < 1000:
            if i < 10:
                p.apply_async(open_text_file, args=("self00"+str(i),))
            elif i < 100:
                p.apply_async(open_text_file, args=("self0"+str(i),))
            else:  # that is 100 < i < 1000
                p.apply_async(open_text_file, args=("self"+str(i),))
                
        elif number_of_tasks < 10000:
            if i < 10:
                p.apply_async(open_text_file, args=("self000"+str(i),))
            elif i < 100:
                p.apply_async(open_text_file, args=("self00"+str(i),))
            elif i < 1000:
                p.apply_async(open_text_file, args=("self0"+str(i),))
            else:   # that is 1000 < i < 10000
                p.apply_async(open_text_file, args=("self"+str(i),))
                
        else:
            print "tasklist number over 1W! # 队列数目超过1W"
            
    print 'Waiting for all subprocesses done...'
    p.close()
    p.join()
    os.system("amh mysql start")        #怕mysql挂掉
    print 'All subprocesses done.'

