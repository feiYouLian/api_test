# !usr/bin/env python3
#  -*- coding:utf-8 -*-

from typing import List
import requests
import json

from .util import getDictVal, getDocPath, writeJSON


class Parameter(object):
    def __init__(self, position: str = '', schema=None):
        self.position = position
        self.schema = schema if schema is not None else {}


class Api(object):
    def __init__(self,
                 summary: str = '',
                 tags: str = '',
                 path: str = '',
                 method: str = '',
                 parameters: List[Parameter] = None):
        self.summary = summary
        self.tags = tags
        self.path = path
        self.method = method
        self.parameters = parameters if parameters is not None else []


class Doc(object):
    def __init__(self, host: str = '', apis: List[Api] = None):
        self.host = host
        self.apis = apis if apis is not None else []


def parseApiDoc(doc: dict) -> Doc:
    d = Doc()

    d.host = getDictVal(doc, 'host')

    pathListDoc = getDictVal(doc, 'paths')
    apis = []
    for path, pathDoc in pathListDoc.items():
        for method, apidoc in pathDoc.items():
            api = parseOneApi(doc, apidoc)

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
        paramType = getDictVal(paramDoc, 'type')
        paramNeed = getDictVal(paramDoc, 'required')

        index = -1
        parameter = Parameter()
        for idx, p in enumerate(parameterList):
            if p.position == paramIn:
                parameter = p
                index = idx
                break

        parameter.position = paramIn

        if parameter.position == 'body':
            parameter.schema = parseProp(doc, paramDoc, paramType, paramNeed)
        else:
            if '[0]' in paramName:
                paramNameList = paramName.split('[0].')
                paramName_0 = paramNameList[0]
                paramName_1 = paramNameList[1]
                if getDictVal(parameter.schema, paramName_0) is None:
                    parameter.schema[paramName_0] = {}

                parameter.schema[paramName_0][paramName_1] = parseProp(
                    doc, paramDoc, paramType, paramNeed)

            else:
                parameter.schema[paramName] = parseProp(
                    doc, paramDoc, paramType, paramNeed)

        if index < 0:
            parameterList.append(parameter)
        else:
            parameterList[index] = parameter

    return parameterList


def parseProp(doc: dict, propDoc: dict, propType: str, isNeed: bool):

    if propType is not None:
        if propType == 'array':
            itemsDoc = getDictVal(propDoc, 'items')
            itemsType = getDictVal(itemsDoc, 'type')
            return [parseProp(doc, itemsDoc, itemsType, isNeed)]

        return propType + "|" + str(isNeed)

    schemaDoc = getDictVal(propDoc, 'schema')
    schemaType = getDictVal(schemaDoc, 'type')

    if schemaType is not None:
        return parseProp(doc, schemaDoc, schemaType, isNeed)

    schemaRef = None
    if getDictVal(schemaDoc, '$ref') is not None:
        schemaRef = getDictVal(schemaDoc, '$ref')
    else:
        schemaRef = getDictVal(propDoc, '$ref')

    refs = schemaRef.split("/") if schemaRef is not None else ['']
    refType = refs[len(refs) - 1]
    refDoc = getDictVal(getDictVal(doc, 'definitions'), refType)

    if refDoc is not None:
        props = {}
        for p, pdoc in getDictVal(refDoc, 'properties').items():
            pType = getDictVal(pdoc, 'type')
            props[p] = parseProp(doc, pdoc, pType, isNeed)
        return props

    return refType + "|" + str(isNeed)


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
