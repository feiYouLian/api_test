# !usr/bin/env python3
#  -*- coding:utf-8 -*-

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
