在我们日常的工作中，经常需要打包给测试进行测试，或者给产品经理体验。一次又一次的手动打包，修改plist文件，上传服务器浪费了我们大量宝贵的学习时间。
这是一个用于自动打包的Python脚本，可以直接打包ipa并生成对应的plist，并上传指定的七牛服务器。这所有的动作只需要在终端敲入一行命令即可解决。
###如何开始
+ 确保安装了xctool
	+ xctool 是FaceBook开源的一个命令行工具，用来替代苹果的xcodebuild工具。
	+ 没有安装xctool，可以用brew安装，没有安装brew的，可以通过搜索安装brew，然后执行如下操作安装xctool:`sudo brew install xctool`             
+ 找到Config.py，根据里面的注释做好配置设置
+ 在template文件夹里放入正确的模板plist文件，这个程序只会改模板plist中ipa包下载地址对应的值
+ 在终端定位到项目所在文件夹，执行`qiniu/bin/python Client.py`
+ 等待脚本运行完成，运行完成后自动打好的ipa包和plist文件都会上传到Config.py配置好的七牛服务器上，并且在History文件夹里面保存对应的archive文件、ipa文件、plist文件

**另外这里使用了Python的[虚拟环境](http://www.pythondoc.com/flask-mega-tutorial/helloworld.html#flask)**

**如果不想上传七牛服务器，不配置七牛的相关信息即可(上传失败)**

###原理说明
要完成这几个动作，我们需要做四件事情，依次是archive--->打包成ipa--->生成对应的plist文件--->上传七牛，下面来依次说明原理。

####一、archive
使用xctool执行archive操作，下面对xctool的参数和命令进行一个说明。为了能运行shell命令，使用了`Python`的`subprocess`库

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
注：archive命令需要接一个参数：-archivePath 即你存放Archive文件的目录

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

####3、生成plist文件
为了简单，这里生成的plist文件是通过编辑模板plist文件的一些key的value来生成的，这里只改变了plist文件里面ipa包下载地址对应的key。这样对plist文件进行编辑使用的是`Python`的`biplist`

####4、上传七牛
使用七牛提供的`Python SDK`, 上传七牛，具体介绍见[七牛的官方文档](http://developer.qiniu.com/docs/v6/sdk/python-sdk.html)，使用可以在Client.py文件中看到。

####5、TODO
直接从七牛获取所有的plist文件， 自动生成网页。
