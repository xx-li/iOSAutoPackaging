# -*- coding: utf-8 -*-
__author__ = 'lixinxing'

#--------打包信息---------
# 需要打包的项目信息
project_path = '项目所在目录'
workspace_name = 'test.xcworkspace'
scheme_name = 'test'
# 个人证书，用于打包ipa
provisioning_profile = 'testprofile'

# -------企业发布信息------
# 用于企业发布的plist文件，只会修改里面的ipa包下载路径，其他的需要改成与自己项目相符
template_plist_name = 'test.plist'

#-----重新签名信息------
#重签名需要的plist文件
resign_plist_name = 'entitlements.plist'
#企业证书名字
ep_cer_name = 'test'
# 企业账号，用于重签。需要放入template目录下
ep_provisioning_profile = 'test.mobileprovision'

# ----上传服务器配置（使用七牛）-----
access_key = 'test'
secret_key = 'test'
bucket_name = 'test'
ipa_base_url = 'test'
