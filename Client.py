# -*- coding: utf-8 -*-
# flake8: noqa

from qiniu import Auth
from qiniu import put_file
from qiniu import put_data
from PlistEdit import PlistEdit
import datetime
import Config
from Packaging import Packaging

formt_time = datetime.datetime.now().strftime("%Y-%m-%d")
print 'time:', formt_time

access_key = Config.access_key
secret_key = Config.secret_key
bucket_name = Config.bucket_name

q = Auth(access_key, secret_key)

# 上传本地ipa文件
ipa_path = Packaging().newIpa()
ipa_name = ipa_path.split('/')[-1]
print 'ipa_name: ',ipa_name

token = q.upload_token(bucket_name, ipa_name)
ret, info = put_file(token, ipa_name, ipa_path, mime_type="application/octet-stream", check_crc=True)
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

# 修改html页面并上传


