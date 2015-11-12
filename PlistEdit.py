# -*- coding: utf-8 -*-
__author__ = 'lixinxing'

import os
import json
from biplist import *
import datetime
import Config


class PlistEdit:
    # 保存生成的plist，并且将路径返回
    def savenewplist(self, plist):
        formt_time = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
        save_name = Config.scheme_name + formt_time + '.plist'
        plist_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'history', save_name))

        try:
            writePlist(plist, plist_path)
            return plist_path
        except (InvalidPlistException, NotBinaryPlistException), e:
            print 'someting bad happend when writePlist:',e

    # 通过模板生成新的plist文件
    def newplist(self,templatename, ipaname):
        # 通过此生成外链ipa地址
        base_url = Config.ipa_base_url
        plist_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'template', templatename))
        print 'plist path :', plist_path

        try:
            plist = readPlist(plist_path)
            plist["items"][0]['assets'][0]['url'] = base_url + ipaname
            ipa_url = plist["items"][0]['assets'][0]['url']
            print ipa_url
            # version 暂不关心
            # version = plist["items"][0]['metadata']['bundle-version']
            # print version
            return self.savenewplist(plist)

        except (InvalidPlistException, NotBinaryPlistException),e:
            print 'Not a plist:',e
