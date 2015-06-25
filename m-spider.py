#!/usr/bin/python
#coding=utf-8
from urllib2 import Request, urlopen, URLError, HTTPError
from multiprocessing import Pool
import os
import chardet # require to install
import sys
import string
import urllib2
import re
import time
import sys
# import socket
# urllib2.socket.setdefaulttimeout(30) # backup.before the Python 2.6

def usage():
    print u'''
    Usage：
        >python m-spider.py <进程数 每个进程处理多少行网址>
        
    Example:
        >m-spider.py 10 20
    
    Necessary:
        1.document name:url.txt
            1.网址一行两列,以空格间隔
                *.每行第一列为虚拟主机提供商提供的测试网址，每行第二列为客户域名网址
            2.不带http://
        2.chardet
    
    Description:
        *.运行结果会保存为*-result（*为模式匹配）
        *.中止请按command+z(OS X)
        
     
    Efficiency:
        *.1 CPU Core : 35 process
        *.2 CPU Core : 60 process
        
    Project:
        https://github.com/likunyan/multiprocess-spider
            
    Follow:
        李坤严 2015/06/25
        https://www.likunyan.com
    '''
    
#定义,文件名    
text_file = "url.txt"    

if len(sys.argv) is 3:
    #定义,进程数
    number_of_processes = int(sys.argv[1])
    #定义,每个进程处理多少行网址
    text_lines = int(sys.argv[2])
elif len(sys.argv) is not 3:
    usage()
    sys.exit(1)

'''
统计文本行数
'''
total_text_lines = 0 				
thefile = open(text_file,'rb')  
while True:  
    buffer = thefile.read(1024 * 8192)  
    if not buffer:  
        break  
    total_text_lines += buffer.count('\n')
    print "url.txt总共" + str(total_text_lines) + "行网址"
thefile.close()

'''
计算url.txt在指定『每个进程处理多少行网址』的时候，需要安排几个任务
'''
if total_text_lines%text_lines == 0:
    # alignment number # 列队中的数目
    global number_of_tasks
    number_of_tasks = total_text_lines/text_lines 
else:
    # 有余数的时候，需要多安排一个任务
    number_of_tasks = (total_text_lines/text_lines)+1    
print "计划安排" + str(number_of_tasks) + "个任务"


def open_text_file(i,start_line, end_line):
    
    def spider(text_line):
        # text_line = text_line.replace("\n", "")      # 替换上一步中，轮询到的每行结果中的换行字符为空白
        req_url = "http://"+text_line              # 因为start_line的域名是不带http://的，这边加下
        
        try:
            urlopen(req_url)
        except Exception, e:
            with open(result_text_file, 'a') as output:
                output.write("url_Error "+str(e)+" "+req_url+"\n")
            return 0 # 表示失败当前（即第一列）网址访问报错，需要重新访问第二列网址
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
                    #if m: # 网址标题是否为空
                        #print title.group()
                    if title:
                        with open(result_text_file, 'a') as output:
                            output.write(title.group(1)+" "+req_url+"\n")
                    else:
                        # <title xmlns=...><title> 特殊情况
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
                            
                    if title:  # 网址标题是否为空
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
                                
    # 记录开始时间                            
    with open("log_result", 'a') as output:
        output.write("开始时间:"+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())+"\n")
    print "进程"+str(i)+"开始"
    
    result_text_file = str(i)+"-result"  # 执行结果以进程标志+result形式保存
    
    for text_line in open(text_file).readlines()[start_line:end_line]:  # 轮询源文件中的网址
        host_value = text_line.split() # 用空格分割字符串，并保存到列表
        status = spider(host_value[0])
        if status == 0: # 如果url.txt这个文本中第一列的网址不能够访问的话，执行第二列中的网址
            spider(host_value[1])
            
    with open("log_result", 'a') as output:
        output.write("结束时间:"+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())+"\n")   
    print "进程"+str(i)+"结束"
    
    
if __name__=='__main__':
    print 'Parent process %s.' % os.getpid()
    p = Pool(number_of_processes)
    for i in xrange(number_of_tasks):
        i+=1 #从1开始
        p.apply_async(open_text_file, args=(i,text_lines*(i-1),text_lines*i,))
            
    print 'Waiting for all subprocesses done...'
    p.close()
    p.join()
    print 'All subprocesses done.'
