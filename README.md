Python网页爬虫
====
**功能**

- 记录网址的标题（正则）
- 记录网站的HTTP状态
- 记录网页源代码中，是否包含有百家乐、太阳城这两个关键字

**多进程**

`python multiprocess-spider.py M N`
- M:进程数
- N:任务数
当然M < N

**效率**

1核VPS(Vultr.com)，36个进程左右；2核VPS(directspace.net)，60进程左右。

**分配**
假如有600000个网址要爬，60进程的话，那么我一般会分配为1000个任务，

`总网址=文件中的网址数量*任务数M`  
`10000=10*1000`

**使用说明**

- 在名为`self`(源文件)文本中，保存不带http://的网址，，一行一个
- 多进程，所以这边需要把self切割为多份,`split  -d -a 3 -l 10 self self`
 - d为数字，a为位数，l为行数，第一个self为源文件，第二个self为格式化的文件头 
 - 命令执行完后，self文件被切割为10000/10=1000个文件，self000,self001,...,self099,self101,...,self999，这样的。
- 运行结果会保存为`self*-result`(星号指匹配，这边为任务数N),总计

**注意**

- 需要安装python模块chardet

**升级计划**

- httplib2
- 
**联系方式**

[我的维基][likunyan]
*******************
[likunyan]:https://www.likunyan.com
