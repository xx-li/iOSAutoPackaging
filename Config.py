# -*- coding: utf-8 -*-
__author__ = 'lixinxing'

# 需要打包的项目信息
project_path = '项目所在目录'
workspace_name = 'test.xcworkspace'
scheme_name = 'test'
template_plist_name = 'test.plist'
resign_plist_name = 'entitlements.plist'

# 个人证书，用于打包ipa
provisioning_profile = 'testprofile'

#重新签名信息
#企业证书名字
ep_cer_name = 'test'
# 企业账号，用于重签。需要放入template目录下
ep_provisioning_profile = 'test.mobileprovision'

# 企业证书对应的Prefix
# ep_cer_prefix = '828E9CDH58'
# 企业账号用于发布的*Provisioning Profiles*对应的*Bundle Identifier
# ep_provisioning_BI = 'com.test.test'


# 七牛配置
access_key = 'test'
secret_key = 'test'
bucket_name = 'test'
ipa_base_url = 'test'
