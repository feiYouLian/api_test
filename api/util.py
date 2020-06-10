# !usr/bin/env python3
#  -*- coding:utf-8 -*-

from typing import List
import json
import sys
import os


def getDictVal(d, key):
    if d == None or type(d) != dict or key not in d:
        return None
    return d[key]


def getDocPath(fileName: str) -> str:
    # return os.path.join(os.path.abspath(''), fileName)
    return os.path.join(sys.path[0], fileName)


def writeJSON(filePath: str, obj: object):
    dirpath = os.path.dirname(filePath)
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    content = json.dumps(obj,
                         default=lambda ohj: ohj.__dict__,
                         indent=2,
                         ensure_ascii=False)
    with open(filePath, 'wb') as f:
        f.write(content.encode('utf8'))


def readJSON(filePath: str) -> object:
    with open(filePath, 'r') as f:
        return json.load(f)
