# python-sdk
打包方法：
1. python setup.py bdist_egg (egg 包) 或者 python setup.py sdist (pip包) 
2. 之后将整个目录打包发给调用方
    
安装和使用SDK：
1. 解压，进入主目录下
2. python setup.py install --record files.txt  安装
3. import rubikai 在python程序中，调用安装好的rubikai包
