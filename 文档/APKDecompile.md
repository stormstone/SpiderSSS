## APK反编译：

https://blog.csdn.net/s13383754499/article/details/78914592

- apktool ：使用apktool反编译apk得到图片、XML配置、语言资源等文件，

```shell
java -jar apktool_2.0.1.jar d -f [PATH_APK] -o [PATH_OUT]
```

- dex2jar：使用dex2jar反编译apk得到Java源代码，将要反编译的APK后缀名改为.rar或者 .zip，并解压，得到其中的classes.dex文件（它就是java文件编译再通过dx工具打包而成的）

```shell
d2j-dex2jar classes.dex
```

- jd-gui ：源码查看，IDEA亦可

## 脱壳：

https://www.jianshu.com/p/138c9de2c987

工具：VirtualXposed（或者直接xposed）、FDex2

## JAD-反编译class文件：

[利用jdk自带的jad.exe实现批量反编译class文件](https://www.cnblogs.com/flydkPocketMagic/p/7048350.html)


```shell
jad -o -8 -r -d[PATH_OUT] -sjava [PATH_CLASS]
```







