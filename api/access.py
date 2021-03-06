# !usr/bin/env python3
#  -*- coding:utf-8 -*-

from typing import List

import requests
import json
import os

from . import util

apis = object()


def loadApisDoc(fileName: str):
    global apis
    apis = util.readJSON(util.getDocPath(fileName))


def genApiMetaData(path: str, parameters: List[dict]):
    method = 'get'
    url = 'http://' + util.getDictVal(apis, 'host') + path
    params = None
    data = None
    files = None
    json = None
    headers = None

    apiDoc = None
    for api in util.getDictVal(apis, 'apis'):
        if util.getDictVal(api, 'path') == path:
            apiDoc = api
            break

    if apiDoc is None:
        raise Exception("未找到apiDoc", path)

    method = util.getDictVal(apiDoc, 'method')
    parametersDoc = util.getDictVal(apiDoc, 'parameters')

    if len(parameters) < len(parametersDoc):
        raise Exception("请求参数不全", path)

    for idx, paramDoc in enumerate(parametersDoc):
        position = util.getDictVal(paramDoc, 'position')
        if position == 'header':
            headers = parameters[idx]

        elif position == 'path':
            p = parameters[idx]
            for k, v in p.items():
                url = url.replace('{' + k + '}', str(v))

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
    session = requests.session()
    return doRequest2(session, path, parameters, **kwargs)


def doRequest2(session: requests.Session, path: str, parameters: List[dict],
               **kwargs) -> requests.Response:
    '''
    :param session: 对应 requests.Session 对象, 
    :param path: 对应 api.json 中 接口path 属性, 
    :param parameters: 对应 api.json 中 接口parameters列表中的 schema 属性, 顺序保持一致
    :param **kwargs: 对应 requests 中除了 method, url, params, data, files, json, 以外的其他属性
    '''
    method, url, params, data, files, json, headers = genApiMetaData(
        path, parameters)

    if util.getDictVal(kwargs, 'headers') is None:
        kwargs['headers'] = headers
    else:
        kwargs['headers'] = dict(headers, **kwargs['headers'])

    resp = session.request(method,
                           url,
                           params=params,
                           data=data,
                           files=files,
                           json=json,
                           **kwargs)

    print('\r\n-------------------------------------------')
    print(url)
    print('method:', method)
    if kwargs['headers'] is not None:
        print('headers:', kwargs['headers'])

    if params is not None:
        print('params:', params)

    if data is not None:
        print('data:', data)

    if files is not None:
        f = []
        for k in files.keys():
            f.append(k)
        print('files:', f)

    if json is not None:
        print('json:', json)

    print('response:', resp.text)

    return resp
