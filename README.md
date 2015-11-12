###使用xctool archive

+ 命令：`xctool -workspace ProjectName.xcworkspace -scheme SchemeName clean archive`

+ 自动打包并放到指定目录
	+ `xctool -workspace ProjectName.xcworkspace -scheme SchemeName clean archive -archivePath /Users/lixinxing/Desktop/test11/test.xcarchive`

	+ `xctool -workspace /Users/lixinxing/Desktop/SchemeName_APP/ProjectName.xcworkspace -scheme SchemeName clean archive -archivePath /Users/lixinxing/Desktop/AutoPackaging/history/test.xcarchive`

+ archive 打包成ipa包
```
xcodebuild -exportArchive -archivePath ${PROJECT_NAME}.xcarchive \
                          -exportPath ${PROJECT_NAME} \
                          -exportFormat ipa \
                          -exportProvisioningProfile ${PROFILE_NAME}
```

+ 样例：
`xcodebuild -exportArchive -archivePath /Users/lixinxing/Library/Developer/Xcode/Archives/2015-09-07/SchemeName\ 15-9-7\ 下午2.38.xcarchive -exportPath /Users/lixinxing/Desktop/test11/test.ipa -exportFormat ipa -exportProvisioningProfile ProjectNameEnterprise`