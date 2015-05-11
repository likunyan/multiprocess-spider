#Python网页爬虫
* 两种多进程方式:
    * pool  //建议
    * thread
* 两种请求网页方式:
    * urllib2，对应文urllib2_title.py
    * httplib2，对应文件httplib2_title.py  //尚未发布
* 功能:
  1. 记录网址的标题
  2. 用来检查网站是否打不开，程序会判断请求的HTTP状态，非200的，会提示报错信息并保存
  3. 判断网址首页的源码是否有百家乐、太阳城这两个关键字
* 使用说明:
  1. 我这里是有一个urlFile文件(假如有1680行)，里面保存着网址，一行一个(我这边的环境导出来的网址是不带http://的)
  2. 多进程，所以这边需要把urlFile切割为多份,split -a 2 -d -l 168 urlFile self，命令执行完后，urlFile文件被切割为1680/168=10个文件，self00,self01,...,self10,self11,...，这样的。
  3. 程序运行结果会保存为self??-result这样的。
* 注意:
    * 需要安装python模块chardet
