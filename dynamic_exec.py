# !usr/bin/env python3
#  -*- coding:utf-8 -*-

if __name__ == "__main__":
    with open('./api_doc.py', 'rb') as f:
        # print(f.read().decode('utf8'))
        exec(f.read().decode('utf8'))
