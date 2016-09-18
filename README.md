在我们日常的工作中，经常需要打包给测试进行测试，或者给产品经理体验。一次又一次的手动打包，修改plist文件，上传服务器浪费了我们大量宝贵的学习时间。
这是一个用于自动打包的Python脚本，可以直接打包ipa并生成对应的plist，然后使用企业证书进行重签名，并上传指定的七牛服务器。这所有的动作只需要在终端敲入一行命令即可解决。

###功能流程说明
`打包ipa`-->`重签名ipa`-->`生成plist文件`-->`上传服务器`-->`发送邮件`

###使用说明（针对`iOS开发者`）
+ 1、安装`HomeBrew` 
	+ 安装命令：`/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`

+ 2、安装`xctool`用于`iOS项目`打包
	+ `brew install xctool`

+ 3、安装`pip`
	+ 1.我们先获取`pip`安装脚本:`wget https://bootstrap.pypa.io/get-pip.py`
	如果没有安装`wget`可以执行`brew install wget`安装
	+ 2.安装pip `sudo python get-pip.py`

+ 4、安装Python虚拟环境virtualenv
	+ `$ sudo pip install virtualenv`

+ 5、进入下载的项目所在的目录
```shell
$ cd (you path)
$ virtualenv venv		执行此命令后会在当前目录下创建一个venu文件夹
New python executable in venv/bin/python
Installing distribute............done.
$ venv/bin/pip install -r requirements.txt
```

+ 6、配置项目
	+ 修改`entitlements.plist`文件，不知道修改可以看我的博文[iOS证书及ipa包重签名](http://devlxx.com/ioszheng-shu-ji-ipabao-zhong-qian-ming/)
	+ 修改`test.plist`,根据这个plist文件来安装app，具体配置方法可以搜索iOS企业发布流程
	+ 修改`Config.py`文件,如何配置根据注释来。

+ 7、自动打包
	+ 执行`venv/bin/python Client.py`。上传成功后会让你输入版本注释，输入后点击回车就会发邮件，整个流程就走完了。
> 打包完成后，可以在history文件夹下看到生成的ipa包以及改好的plist文件等


###原理说明
####archive
使用`xctool`执行`archive`操作，`xctool`是`FaceBook`开源的一个命令行工具，用来替代苹果的`xcodebuild`工具。下面对xctool的参数和命令进行一个说明。为了能运行shell命令，此项目使用了`Python`的`subprocess`库
+ 参数：
```
-workspace 需要打包的workspace 后面接的文件一定要是.xcworkspace 结尾的
-scheme 需要打包的Scheme
-configuration 需要打包的配置文件，我们一般在项目中添加多个配置，适合不同的环境
```
+ 命令：
```
clean 清除编译产生的问题，下次编译就是全新的编译了
archive 打包命令，会生成一个.xcarchive的文件
```
注：`archive`命令需要接一个参数：-archivePath 即你存放Archive文件的目录
+ 使用说明
	+ 命令：`xctool -workspace ProjectName.xcworkspace -scheme SchemeName clean archive`
	+ 样例：`xctool -workspace /Users/lixinxing/Desktop/SchemeName_APP/ProjectName.xcworkspace -scheme SchemeName clean archive -archivePath /Users/lixinxing/Desktop/iOSAutoPackaging/history/test.xcarchive`
执行这个命令后，会将打好的包命名为`test.xcarchive`放在目录`/Users/lixinxing/Desktop/iOSAutoPackaging/history/`

####2、export为ipa包
这个操作需要用到`xcodebuild`,他是`xocde`的 `Command line tools` 就有的一个命令
+ 参数
```
-exportArchive  告诉xcodebuild需要导出archive文件
-exportFormat 告诉xcodebuild需要导出的archive文件最后格式 后面接IPA 就是archive文件导出的格式为ipa文件
-archivePath archive文件目录
-exportPath 导出的ipa存放目录
-exportProvisioningProfile 打包用到的ProvisioningProfile
```

+ 命令
```
xcodebuild -exportArchive -archivePath ${PROJECT_NAME}.xcarchive \
                          -exportPath ${PROJECT_NAME} \
                          -exportFormat ipa \
                          -exportProvisioningProfile ${PROFILE_NAME}
```

+ 样例：
```
xcodebuild -exportArchive -archivePath /Users/lixinxing/Library/Developer/Xcode/Archives/2015-09-07/SchemeName\ 15-9-7\ 下午2.38.xcarchive -exportPath /Users/lixinxing/Desktop/test/test.ipa -exportFormat ipa -exportProvisioningProfile ProjectNameEnterprise
```
这个例子的含义可以结合上面的参数说明进行理解，这样就完成的打包工作，生成了一个`test.ipa`文件放在`/Users/lixinxing/Desktop/test/`目录下

####3、重签名
[iOS证书及ipa包重签名](http://devlxx.com/ioszheng-shu-ji-ipabao-zhong-qian-ming/)

####4、生成plist文件
为了简单，这里生成的plist文件是通过编辑模板plist文件的一些key的value来生成的，这里只改变了plist文件里面ipa包下载地址对应的key。这里对plist文件进行编辑使用的是`Python`的`biplist`

####5、上传七牛
使用七牛提供的`Python SDK`, 上传七牛，具体介绍见[七牛的官方文档](http://developer.qiniu.com/docs/v6/sdk/python-sdk.html),使用可以在Client.py文件中看到。

####6、发送邮件

####7、TODO
直接从七牛获取所有的plist文件， 自动生成网页。
