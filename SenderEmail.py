#!/usr/bin/env python
# -*- coding: utf-8 -*-
#导入smtplib和MIMEText
import smtplib,sys 
from email.mime.text import MIMEText 


class SenderEmail:

    def send_mail(self, sub, content):
    #############
    # 要发给谁
        mailto_list=["x@devlxx.com",
                     "13348782277@163.com"]
    #####################
    #设置服务器，用户名、口令以及邮箱的后缀
        mail_host="smtp.exmail.qq.com"
        mail_user="x@devlxx.com"
        mail_pass="dear334693"
        mail_postfix="devlxx.com"
    ######################
        '''
        to_list:发给谁
        sub:主题
        content:内容
        send_mail("aaa@126.com","sub","content")
        '''
        me = mail_user+"<"+mail_user+"@"+mail_postfix+">"
        msg = MIMEText(content, 'html', 'utf-8')
        msg['Subject'] = sub
        msg['From'] = me 
        msg['To'] = ";".join(mailto_list) 
        try: 
            s = smtplib.SMTP() 
            s.connect(mail_host) 
            s.login(mail_user,mail_pass) 
            s.sendmail(me, mailto_list, msg.as_string()) 
            s.close() 
            return True
        except Exception, e: 
            print str(e) 
            return False
if __name__ == '__main__':
    if SenderEmail().send_mail(u'这是python测试邮件1',u'python发送邮件1'):
        print u'发送成功'
    else:
        print u'发送失败'