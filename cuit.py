# -*- coding: utf-8 -*-
"""
Created on 2019/12/5 005 下午 4:13
@author: DapingLee
@license : Copyright(C), CUIT
@contact : ldp01@vip.qq.com
"""
import sys
import requests


def get_info():
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36'}
    ret = requests.get('http://10.254.241.19/', headers=headers)
    return ret.text.split('\'')[1].split('?')[1]


def login(username, password):
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36'}
    data = {'userId': username,
            'password': password,
            'service': '%E6%A0%A1%E5%9B%AD%E7%BD%91',
            'queryString': get_info(),
            'operatorPwd': '',
            'operatorUserId': '',
            'validcode': '',
            'passwordEncrypt': 'false'}
    ret = requests.post('http://10.254.241.19/eportal/InterFace.do?method=login', headers=headers, data=data)

    if 'success' in ret.text:
        print('登录成功，可关闭程序')
    else:
        print('登录失败，请检查用户名和密码是否正确')


if __name__ == '__main__':
    try:
        login(sys.argv[1], sys.argv[2])
    except:
        print('登录失败，请检查是否已经在线')
