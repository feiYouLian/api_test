# !usr/bin/env python3
#  -*- coding:utf-8 -*-

import requests
from api.doc import *
from api.access import *
from conf.config import Config

if __name__ == "__main__":
    # 加载配置
    cfg = Config()
    doc_url = cfg.doc_url
    doc_file = cfg.doc_file

    # 生成文档 api.json
    generateDoc(doc_url, doc_file)

    # 针对有权限拦截的文档路径
    # 登录
    # session = requests.session()
    # r = session.post('http://10.87.200.21:8875/login',
    #                  data={
    #                      'username': 'admin',
    #                      'password': '111111'
    #                  })
    # print(r.status_code)
    # # 生成文档 api.json
    # generateDoc2(session, doc_url, doc_file)
