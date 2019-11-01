#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import nmap
import time
import yagmail
import ipaddress

def check_host_state(host_ip):
    check_result = nmap.PortScanner().scan(host_ip,arguments='-sP')
    check_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if check_result['scan']:
        state_result = check_result['scan'][host_ip]['status']['state']
        return check_time,state_result
    else:
        return check_time,'down'

def send_alert_mail(mail_addr,host_ip,host_state,check_time,mail_contents):
    yag=yagmail.SMTP(user='18867120286@139.com',password='bay10rHuang',host='smtp.139.com')
    # contents = '{}状态变为{},时间{}'.format(host_ip,host_state,check_time)
    try:
        yag.send(mail_addr,'主机状态监控报警邮件',mail_contents)
        sendmail_msg = '告警邮件发送成功。'
        print(sendmail_msg)
        return sendmail_msg
    except OSError:
        sendmail_msg = '本机网络故障，告警邮件发送失败'
        print(sendmail_msg)
        pass
        # return sendmail_msg

if __name__ == '__main__':
    # host_ip = '192.168.11.1'
    host_ip = sys.argv[1]
    pre_state='down'
    logfile_name = host_ip.replace('.','_') + '.txt'
    while True:
        check_time , res_state = check_host_state(host_ip)
        if res_state != pre_state:
            log_contents = '{}状态变化，当前状态为{}，检查时间{}。'.format(host_ip,res_state,check_time)
            print(log_contents)
            with open(logfile_name,'a+') as logfile:
                logfile.write(log_contents + '\n')
            send_alert_mail('huangxy@ahope.com.cn',host_ip,check_time,res_state,log_contents)
            pre_state = res_state
        else:
            log_contents = '{}状态为{}，检查时间{}'.format(host_ip,res_state,check_time)
            print(log_contents)
            with open(logfile_name,'a+') as logfile:
                logfile.write(log_contents + '\n')
        time.sleep(10)


