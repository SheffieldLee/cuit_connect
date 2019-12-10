# -*- coding: utf-8 -*-
"""
Created on 2019/12/5 005 下午 4:13
@author: DapingLee
@license : Copyright(C), CUIT
"""
import json
import sys
import time
import requests


class Connect:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.url = 'http://10.254.241.19/'
        self.login_url = 'http://10.254.241.19/eportal/InterFace.do?method=login'
        self.online_info_url = 'http://10.254.241.19/eportal/InterFace.do?method=getOnlineUserInfo'
        self.user_agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36'
        self.userIndex = None

    def is_online(self):
        headers = {'User-Agent': self.user_agent}
        data = {'userIndex': self.userIndex}
        while True:
            try:
                ret = requests.post(self.online_info_url, headers=headers, data=data)
                ret.encoding = ret.apparent_encoding
                ret2dic = json.loads(ret.content)
                if ret2dic['result'] == 'fail':
                    return False
                else:
                    return True
            except:
                continue

    def get_info(self):
        headers = {'User-Agent': self.user_agent}
        while True:
            try:
                ret = requests.get(self.url, headers=headers)
                return ret.text.split('\'')[1].split('?')[1]
            except:
                continue

    def login(self):
        headers = {'User-Agent': self.user_agent}
        data = {'userId': self.username,
                'password': self.password,
                'service': '%E6%A0%A1%E5%9B%AD%E7%BD%91',
                'queryString': self.get_info(),
                'operatorPwd': '',
                'operatorUserId': '',
                'validcode': '',
                'passwordEncrypt': 'false'}
        while True:
            try:
                ret = requests.post(self.login_url, headers=headers, data=data)
                ret.encoding = ret.apparent_encoding
                ret2dic = json.loads(ret.content)
                self.userIndex = ret2dic['userIndex']
                if ret2dic['result'] == 'success':
                    print('登录成功')
                    return
                else:
                    print('登录失败')
                    print(ret2dic['message'])
                    sys.exit(1)
            except:
                continue

    def stay_online(self):
        print('发送心跳包，维持在线中...')
        while True:
            # 每隔10秒发送心跳包
            time.sleep(10)
            if not self.is_online():
                print('检测到可能掉线，正在重新登录...')
                self.login()
                print('发送心跳包，维持在线中...')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('用法: python {} username password'.format(sys.argv[0].split('/')[-1]))
        sys.exit(1)

    cuit = Connect(sys.argv[1], sys.argv[2])
    if not cuit.is_online():
        cuit.login()
        cuit.stay_online()
    else:
        print('用户已经在线，无需登录')
        cuit.stay_online()
