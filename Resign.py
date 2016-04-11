# -*- coding: utf-8 -*-
__author__ = 'lixinxing'
# 用于重新签名

import subprocess
import os
import Config
import datetime



class Resign:

    def unzipIpa(self, ipaPath):
        zipName = 'resign.zip'
        # 复制成.zip后缀
        cpCmd = 'cp ' + ipaPath + ' ' + zipName
        print cpCmd
        process = subprocess.Popen(cpCmd, shell=True)
        process.wait()
        # 解压zip到指定目录
        unzipCmd = 'unzip ' + zipName
        print unzipCmd
        process = subprocess.Popen(unzipCmd, shell=True)
        process.wait()

        #删除无用的zip文件
        delZipCmd = 'rm -rf ' + zipName
        process = subprocess.Popen(delZipCmd, shell=True)
        process.wait()

    def replaceFiles(self):
        appName = Config.scheme_name + '.app'
        # 先删除需要替换的文件
        codisignPath = 'Payload/' + appName + '/_CodeSignature'
        targetPath = 'Payload/'+ appName + '/embedded.mobileprovision'
        delDirCmd = 'rm -rf ' + codisignPath + ' ' + targetPath
        print delDirCmd
        process = subprocess.Popen(delDirCmd, shell=True)
        process.wait()

        # 企业Profile的绝对路径
        profilePath = 'template/' + Config.ep_provisioning_profile
        # 需要替换的Profile的地址
        targetPath = 'Payload/' + appName + '/embedded.mobileprovision'
        replaceCmd = 'cp ' + profilePath + ' ' + targetPath
        print replaceCmd
        process = subprocess.Popen(replaceCmd, shell=True)
        process.wait()

    def codesign(self):

        appName = Config.scheme_name + '.app'
        # 重新签名 codesign -f -s $certifierName  --entitlements entitlements.plist Payload/test.app
        eplistPath = os.path.join(os.path.dirname(__file__), 'template', Config.resign_plist_name)
        signPath = 'Payload/' + appName
        signCmd = 'codesign -f -s "' + Config.ep_cer_name + '" --entitlements ' + eplistPath + ' ' + signPath
        print signCmd
        process = subprocess.Popen(signCmd, shell=True)
        process.wait()

    def reZipIpa(self):

        # 重新打包
        formt_time = datetime.datetime.now().strftime("%Y%m%d%H%M")
        resignIpaName = 'Resign' + Config.scheme_name + formt_time + '.ipa'
        reZipResultPath = os.path.join(os.path.dirname(__file__), 'history', resignIpaName)
        rezipCmd = 'zip -r ' + reZipResultPath + ' ' + 'Payload'
        print rezipCmd
        process = subprocess.Popen(rezipCmd, shell=True)
        process.wait()

        # 删除Payload文件
        delPayloadCmd = 'rm -fr ' + 'Payload'
        process = subprocess.Popen(delPayloadCmd, shell=True)
        process.wait()
        return reZipResultPath

    def start(self, ipaPath):
        self.unzipIpa(ipaPath)
        self.replaceFiles()
        self.codesign()
        path = self.reZipIpa()
        return path

if  __name__ == '__main__':
    dir = os.path.join(os.path.dirname(__file__), 'history')
    print dir
    # 获取各路径
    ipaPath = os.path.abspath(os.path.join(dir, 'test.ipa'))
    new_ipa = Resign().start(ipaPath)
    print new_ipa
