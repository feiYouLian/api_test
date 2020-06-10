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
    def __init__(self,
                 summary: str = '',
                 tags: str = '',
                 path: str = '',
                 method: str = '',
                 parameters: List[Parameter] = []):
        self.summary = summary
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


def parseOneApi(doc: dict, apidoc: dict) -> Api:
    api = Api()
    api.summary = getDictVal(apidoc, 'summary')
    api.tags = ','.join(getDictVal(apidoc, 'tags'))
    paramListDoc = getDictVal(apidoc, 'parameters')
    if paramListDoc is not None:
        api.parameters = parseApiParam(doc, paramListDoc)
    return api


def parseApiParam(doc: dict, paramListDoc: list) -> List[Parameter]:
    parameterList: List[Parameter] = []

    for paramDoc in paramListDoc:

        paramIn = getDictVal(paramDoc, 'in')
        paramName = getDictVal(paramDoc, 'name')
        paramNeed = getDictVal(paramDoc, 'required')

        paramType = getDictVal(paramDoc, 'type')
        paramSchema = getDictVal(paramDoc, 'schema')

        schemaType = getDictVal(paramSchema, 'type')
        schemaRef = getDictVal(paramSchema, '$ref')

        index = -1
        parameter = Parameter()
        schema = {}
        for idx, p in enumerate(parameterList):
            if p.position == paramIn:
                parameter = p
                index = idx
                schema = parameter.schema
                break
        parameter.position = paramIn

        if paramType is not None:

            if paramType == 'array':
                itemsType = getDictVal(getDictVal(paramDoc, 'items'), 'type')
                schema[paramName] = [itemsType + "|" + str(paramNeed)]
            else:
                schema[paramName] = paramType + "|" + str(paramNeed)

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
                refType = refs[len(refs) - 1]
                refDesc = getDictVal(definitions, refType)
                props = {}
                if refDesc is not None:
                    for prop, propDesc in getDictVal(refDesc,
                                                     'properties').items():
                        props[prop] = getDictVal(propDesc, 'type')
                    schema[paramName] = props
                else:
                    schema[paramName] = refType + "|" + str(paramNeed)

        parameter.schema = schema
        if index < 0:
            parameterList.append(parameter)
        else:
            parameterList[index] = parameter
    return parameterList


def generateDoc(url: str, fileName: str):
    session = requests.session()
    generateDoc2(session, url, fileName)


def generateDoc2(session: requests.Session, url: str, fileName: str):
    r = session.get(url)
    doc = r.json()
    docObj = parseApiDoc(doc)

    filepath = getDocPath(fileName)
    writeJSON(filepath, docObj)
    print('====> generate doc file success! path : %s' % filepath)
