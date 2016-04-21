# -*- coding: utf-8 -*-
# flake8: noqa

from qiniu import Auth
from qiniu import put_file
from qiniu import put_data
from PlistEdit import PlistEdit
import datetime
import Config
from Packaging import Packaging
from SenderEmail import SenderEmail
from  Resign import Resign


formt_time = datetime.datetime.now().strftime("%Y-%m-%d")
print 'time:', formt_time

access_key = Config.access_key
secret_key = Config.secret_key
bucket_name = Config.bucket_name

q = Auth(access_key, secret_key)

# 上传本地ipa文件
ipa_path = Packaging().newIpa()

resign_ipa_path = Resign().start(ipa_path)

ipa_name = resign_ipa_path.split('/')[-1]
print 'ipa_name: ',ipa_name

token = q.upload_token(bucket_name, ipa_name)
ret, info = put_file(token, ipa_name, resign_ipa_path, mime_type="application/octet-stream", check_crc=True)
print(info)
assert ret['key'] == ipa_name

# 上传本地plist文件
template_name = Config.template_plist_name
# 得到生成的plist文件的路径
plist_path =  PlistEdit().newplist(template_name, ipa_name)
plist_name = plist_path.split('/')[-1]
token = q.upload_token(bucket_name, plist_name)
ret, info = put_file(token, plist_name, plist_path, mime_type='application/xml', check_crc=True)
# ret, info = put_data(token, plist_name, data)
print(info)
assert ret['key'] == plist_name

emailTitle = Config.scheme_name + " 新测试包发布".decode('utf-8')
detailTime = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
installLink = 'itms-services://?action=download-manifest&url=https://dn-appreleasexx.qbox.me/' + plist_name

inputNote = raw_input("请输入你的版本更新备注:").decode('utf-8')
print '输入的版本更新备注：', inputNote

emailHtml = \
u'<html xmlns="http://www.test.com" xml:lang="zh">\
    <head>\
        <meta charset="utf-8" />\
    </head> \
    <body>\
        <h1>%s</h1>\n\
        <p>打包时间：<font color="#5172B5">%s</font></p>\
        <p>安装方法：<a href="%s">点此直接安装(目前只支持iOS系统邮件客户端)</a></p>\
        <p>历史地址：<a href="http://www.test.com/test.html">http://www.test.com/test.html</a></p>\
        <p>安装方法：<font color="#5172B5">如果安装到iOS9以后弹出提示无法打开，请到设置 - 通用 - 设备管理 - 选择eegsmart的证书，添加到信任，就可以打开APP了。</font></p>\n\
        <p>更新说明：<font color="#9CC14F" size=4>%s</font></p>\
    </body>\n\
</html>' % (emailTitle, detailTime, installLink, inputNote)

snederFlag = SenderEmail().send_mail( emailTitle, emailHtml)

if snederFlag:
    print('打包发布成功与邮件发送成功！')

# 修改html页面并上传


