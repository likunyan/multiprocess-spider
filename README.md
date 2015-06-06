Python网页爬虫
====
**多进程**

pool  //代码里可以设置要分配M个任务、同时执行N个任务，运行程序，最后执行完它。当然M>N，比如我的小VPS，差不多36个进程就持续100%。假如我有36000个网址要爬，那么我不会分割为100份，一份360。因为到最后不足36个进程在运行，那么最后就等得比较久了，所以，我会分为1000份，然后同时36个进程再跑，就算不足36个了，但是每个进程只有36个网址需要处理，36个大概也就一分多钟而已。//首选、建议、多进程

**功能**

- 记录网址的标题
- 用来检查网站是否打不开，程序会判断请求的HTTP状态，非200的，会提示报错信息并保存
- 判断网址首页的源码是否有百家乐、太阳城这两个关键字

**使用说明**

- 我这里是有一个urlFile文件(假如有1680行)，里面保存着网址，一行一个(我这边的环境导出来的网址是不带http://的)
 - 多进程，所以这边需要把urlFile切割为多份,split -a 2 -d -l 168 urlFile self，命令执行完后，urlFile文件被切割为1680/168=10个文件，self00,self01,...,self10,self11,...，这样的。
 - 程序运行结果会保存为self??-result这样的。

**注意**

- 需要安装python模块chardet

**升级计划**

- httplib2
