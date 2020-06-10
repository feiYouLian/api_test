# !usr/bin/env python3
#  -*- coding:utf-8 -*-

import profig
import sys
import os


class Config:
    def __init__(self):
        cfgPath = os.path.join(sys.path[0], 'conf', 'init.cfg')
        config = profig.Config(cfgPath)
        config.read()

        self.doc_url = config.get('doc.url')
        self.doc_file = config.get('doc.file')
        self.doc_html = config.get('doc.html')

        print(
            '====> cfg load success, doc_url: %s,  doc_file : %s ,  doc_file : %s '
            % (self.doc_url, self.doc_file, self.doc_html))
