Python多进程网页爬虫
====

## What is this:
笔者在IDC工作，那边的windows虚拟主机经常被黑，被加博彩链接，所以笔者就写了这个，判断哪个网站是打不开的、被加博彩链接的，好记录下来。

记录的话，会记录错误类型（404，502，被加的）、网址、标题
## Usage：
    >python m-spider.py <进程数> <每个进程处理多少行网址>.
    
## Example:
    >m-spider.py 10 20

## Necessary:
1. document name:url.txt
    1. 网址一行两列,以空格间隔
        *.每行第一列为虚拟主机提供商提供的测试网址，每行第二列为客户域名网址
    2. 不带http://
2. chardet

## Description:
* 运行结果会保存为*-result（*为模式匹配）
* 中止请按command+z(OS X)
    
 
## Efficiency:
* 1 CPU Core : 35 process
* 2 CPU Core : 60 process
    
## Project:
    https://github.com/likunyan/multiprocess-spider
        
## Follow:
    李坤严 2015/06/25
    https://www.likunyan.com

