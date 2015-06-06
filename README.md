Python多进程网页爬虫
====
**功能**

- 记录网址的标题，如果标题为空则也记录，标识为error。注：使用正则
- 记录网站的HTTP状态
- 记录网页源代码中，是否包含有百家乐、太阳城这两个关键字

**使用方法**

`python multiprocess-spider.py M N`
- M:进程数
- N:任务数
当然M < N

**情景模拟**

- 在名为`self`的源文件中，保存有10000一行一个的网址（不带http://）
- 分配思考：10000个网址，切割为1000份，一份10个。嗯...不错的想法
- 这边需要把self切割为多份,`split  -d -a 3 -l 10 self self`
 - d为数字，a为位数，l为文本行数，第一个self为源文件，第二个self为格式化的文件头
 - 命令执行完后，self文件被切割为10000/10=1000个文件，self000,self001,...,self099,self101,...,self999，这样的。
- `python multiprocess-spider.py 60 1000`
- 运行结果会保存为`self*-result`(星号指匹配，这边为任务数N),总计

**注意**

- 需要安装python模块chardet

**效率**

1核VPS(Vultr.com)，36个进程左右；2核VPS(directspace.net)，60进程左右。

**升级计划**

- 文本切片
- httplib2

**联系方式**

[我的维基][likunyan]
*******************
[likunyan]:https://www.likunyan.com
