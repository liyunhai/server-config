#!/usr/bin/env python
# -*- coding:utf-8 -*-

import smtplib
import re, urllib2
import datetime
from email.mime.text import MIMEText

#setup mailto, server, username, password
mail_to = "liyunhai@yuntengsoft.cn"
mail_host = "smtp.exmail.qq.com"
mail_user = "liyunhai@cloudsoaring.com"
mail_pass = "joycelee"

def send_mail(sub, content):
    msg = MIMEText(content)
    msg['Subject'] = sub
    msg['From'] = mail_user
    msg['To'] = mail_to
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user, mail_pass)
        s.sendmail(mail_user, mail_to, msg.as_string())
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False

def visit(url):
    opener = urllib2.urlopen(url)
    if url == opener.geturl():
        str = opener.read()
    return re.search('\d+\.\d+\.\d+\.\d+', str).group(0)

def getoriginip():
    ipfile = open('/home/liyunhai/util/oip.txt', 'r')
    try:
        oip = ipfile.readline()
    finally:
        ipfile.close()
    return oip

def writeoriginip(remoteip):
    ipfile = open('/home/liyunhai/util/oip.txt', 'w')
    try:
        ipfile.write(remoteip)
    finally:
        ipfile.close()
 
def getremoteip():
    try:
        eip = visit("http://www.whereismyip.com")
    except:
        print "whereismyip error";
        try:
            eip = visit("http://www.bliao.com/ip.phtml")
        except:
            print "bliao error"
            try:
                eip = visit("http://www.ip138.com/ip2city.asp")
            except:
                print "ip138 and all website error"
                eip = "0.0.0.0"
    return eip

if __name__ == '__main__':
    now = str(datetime.datetime.now())
    originip = getoriginip()
    remoteip = getremoteip()
    if remoteip != originip and remoteip != "0.0.0.0":
        writeoriginip(remoteip)
        if send_mail("network_status_report_" + now, "IP Address:" + remoteip + " From Raspberry-Pi"):
            print "sent mail succeed at " + now + "." 
        else:
            print "sent mail failed at " + now + "."
    else:
        print "remote ip is not changed at " + now + "."

