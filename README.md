Python多进程网页爬虫
====
**功能**

- 记录网址的标题，如果标题为空则也记录，标识为error。注：使用正则
- 记录网站的HTTP状态
- 记录网页源代码中，是否包含有百家乐、太阳城这两个关键字

**使用方法**

`python multiprocess-spider.py p l`
- p:进程数(根据机器性能调整，详见效率)
- l:行数

**情景模拟**

- 在名为`self`的源文件中，保存有10000一行一个的网址（不带http://）
- 想要任务数为60，每个进程处理10行数据
- `python multiprocess-spider.py 60 10`
- 运行结果会保存为`*-result`(星号指匹配，这边为第N任务数)

**注意**

- 需要安装python模块chardet

**效率**

1核VPS(Vultr.com)，36个进程左右；2核VPS(directspace.net)，60进程左右。

**升级计划**

- httplib2

**联系方式**

[我的维基][likunyan]
*******************
[likunyan]:https://www.likunyan.com
