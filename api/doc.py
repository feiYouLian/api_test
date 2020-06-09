# !usr/bin/env python3
#  -*- coding:utf-8 -*-

from typing import List
import requests

from .util import getDictVal, getDocPath, writeJSON


class Parameter(object):

    def __init__(self, position: str = '', schema: dict = {}):
        self.position = position
        self.schema = schema


class Api(object):

    def __init__(self, tags: str = '', path: str = '', method: str = '', parameters: List[Parameter] = []):
        self.tags = tags
        self.path = path
        self.method = method
        self.parameters = parameters

    # @property
    # def tags(self) -> str:
    #     return self.__tags

    # @tags.setter
    # def tags(self, tags: str):
    #     self.__tags = tags

    # @property
    # def path(self) -> str:
    #     return self.__path

    # @path.setter
    # def path(self, path: str):
    #     self.__path = path

    # @property
    # def reqType(self) -> str:
    #     return self.__reqType

    # @reqType.setter
    # def reqType(self, reqType: str):
    #     self.__reqType = reqType

    # @property
    # def parameters(self) -> list:
    #     return self.__parameters

    # @parameters.setter
    # def parameters(self, parameters: list):
    #     self.__parameters = parameters


class Doc(object):

    def __init__(self, host: str = '', apis: List[Api] = []):
        self.host = host
        self.apis = apis

    # @property
    # def host(self):
    #     return self.__host

    # @host.setter
    # def host(self, host):
    #     self.__host = host

    # @property
    # def apis(self) -> list:
    #     return self.__apis

    # @apis.setter
    # def apis(self, apis: list):
    #     self.__apis = apis


def aceessApiDoc(url: str) -> dict:
    r = requests.get(url)
    return r.json()


def parseApiDoc(doc: dict) -> Doc:
    d = Doc()

    d.host = getDictVal(doc, 'host')

    paths = getDictVal(doc, 'paths')
    apis = []
    for path, desc in paths.items():
        for method, apidesc in desc.items():
            api = parseOneApi(doc, apidesc)
            api.path = path
            api.method = method
            apis.append(api)

    d.apis = apis
    return d


def parseOneApi(doc: dict, apidesc: dict) -> Api:
    api = Api()

    api.tags = ','.join(getDictVal(apidesc, 'tags'))
    parameters = getDictVal(apidesc, 'parameters')
    if parameters is not None:
        api.parameters = parseApiParam(doc, parameters)
    return api


def parseApiParam(doc: dict, parameters: list) -> List[Parameter]:
    params: List[Parameter] = []

    for param in parameters:

        paramIn = getDictVal(param, 'in')
        paramName = getDictVal(param, 'name')
        paramNeed = getDictVal(param, 'required')

        paramType = getDictVal(param, 'type')
        paramSchema = getDictVal(param, 'schema')

        schemaType = getDictVal(paramSchema, 'type')
        schemaRef = getDictVal(paramSchema, '$ref')

        index = -1
        parameter = Parameter()
        schema = {}
        for idx, p in enumerate(params):
            if p.position == paramIn:
                parameter = p
                index = idx
                schema = parameter.schema
                break
        parameter.position = paramIn

        if paramType is not None:

            if paramType == 'array':
                itemsType = getDictVal(getDictVal(param, 'items'), 'type')
                schema[paramName] = [itemsType+"|"+str(paramNeed)]
            else:
                schema[paramName] = paramType+"|"+str(paramNeed)

        elif paramSchema is not None:

            if schemaType is not None:
                if schemaType == 'array':
                    schemaItemsType = getDictVal(
                        getDictVal(paramSchema, 'items'), 'type')
                    schema[paramName] = [schemaItemsType]
                else:
                    schema[paramName] = schemaType

            elif schemaRef is not None:
                definitions = getDictVal(doc, 'definitions')
                refs = schemaRef.split("/")
                refDesc = getDictVal(definitions, refs[len(refs)-1])
                props = {}
                for prop, propDesc in getDictVal(refDesc, 'properties').items():
                    props[prop] = getDictVal(propDesc, 'type')
                schema[paramName] = props

        parameter.schema = schema
        if index < 0:
            params.append(parameter)
        else:
            params[index] = parameter
    return params


def generateDoc(url: str, fileName: str):
    doc = aceessApiDoc(url)
    docObj = parseApiDoc(doc)

    filepath = getDocPath(fileName)
    writeJSON(filepath, docObj)
    print('====> generate doc file success! path : %s' % filepath)
