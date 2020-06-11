# !usr/bin/env python3
#  -*- coding:utf-8 -*-

from typing import List

import requests
import json
import os

from .util import getDictVal, getDocPath, readJSON

apis = object()


def loadApisDoc(fileName: str):
    global apis
    apis = readJSON(getDocPath(fileName))


def genApiMetaData(path: str, parameters: List[dict]):
    method = 'get'
    url = 'http://' + getDictVal(apis, 'host') + path
    params = None
    data = None
    files = None
    json = None
    headers = None

    apiDoc = None
    for api in getDictVal(apis, 'apis'):
        if getDictVal(api, 'path') == path:
            apiDoc = api

    if apiDoc is None:
        raise Exception("未找到apiDoc", path)

    method = getDictVal(apiDoc, 'method')
    parametersDoc = getDictVal(apiDoc, 'parameters')

    if len(parameters) < len(parametersDoc):
        raise Exception("请求参数不全", path)

    for idx, p in enumerate(parametersDoc):
        position = getDictVal(p, 'position')
        if position == 'header':
            headers = parameters[idx]
        elif position == 'query' and method == 'get':
            params = parameters[idx]
        elif position == 'query' and method == 'post':
            data = parameters[idx]
        elif position == 'formData':
            files = parameters[idx]
        else:
            json = parameters[idx]

    if data is not None and json is not None:
        params = data
        data = None

    return method, url, params, data, files, json, headers


def doRequest(path: str, parameters: List[dict],
              **kwargs) -> requests.Response:
    '''
    :param path: 对应 api.json 中 接口path 属性, 
    :param parameters: 对应 api.json 中 接口parameters列表中的 schema 属性, 顺序保持一致
    '''
    method, url, params, data, files, json, headers = genApiMetaData(
        path, parameters)

    if getDictVal(kwargs, 'headers') is None:
        kwargs['headers'] = headers
    else:
        kwargs['headers'] = dict(headers, **kwargs['headers'])

    resp = requests.request(
        method,
        url,
        params=params,
        data=data,
        files=files,
        json=json,
        # headers=headers,
        **kwargs)
    print(resp.text)
    return resp


def doRequest2(session: requests.Session, path: str, parameters: List[dict],
               **kwargs) -> requests.Response:

    method, url, params, data, files, json = genApiMetaData(path, parameters)
    resp = session.request(method,
                           url,
                           params=params,
                           data=data,
                           files=files,
                           json=json,
                           **kwargs)
    print(resp.status_code)
    return resp
