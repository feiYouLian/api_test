# !usr/bin/env python3
#  -*- coding:utf-8 -*-

from typing import List
import requests
import json

from .util import getDictVal, getDocPath, writeJSON


class Parameter(object):
    def __init__(self, position: str = '', schema=None):
        self.position = position
        if schema is None:
            schema = {}
        self.schema = schema


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
        if parameters is None:
            parameters = []
        self.parameters = parameters


class Doc(object):
    def __init__(self, host: str = '', apis: List[Api] = None):
        self.host = host
        if apis is None:
            apis = []
        self.apis = apis


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
        api.parameters = parseApiParam2(doc, paramListDoc)
    return api


def parseApiParam2(doc: dict, paramListDoc: list) -> List[Parameter]:
    parameterList: List[Parameter] = []

    for paramDoc in paramListDoc:

        paramIn = getDictVal(paramDoc, 'in')

        index = -1
        parameter = Parameter()
        for idx, p in enumerate(parameterList):
            if p.position == paramIn:
                parameter = p
                index = idx
                schema = parameter.schema
                break

        parameter.position = paramIn

        if parameter.position == 'body':
            parseBodyParameter(doc, paramDoc, parameter)
        else:
            parseNormalParameter(doc, paramDoc, parameter)

        if index < 0:
            parameterList.append(parameter)
        else:
            parameterList[index] = parameter

    return parameterList


def parseBodyParameter(doc: dict, paramDoc: dict, bodyParameter: Parameter):
    schema = bodyParameter.schema

    paramName = getDictVal(paramDoc, 'name')
    paramNeed = getDictVal(paramDoc, 'required')

    paramSchemaDoc = getDictVal(paramDoc, 'schema')
    schemaType = getDictVal(paramSchemaDoc, 'type')
    schemaRef = getDictVal(paramSchemaDoc, '$ref')

    if schemaType is not None:
        if schemaType == 'array':
            schemaItemsType = getDictVal(getDictVal(paramSchemaDoc, 'items'),
                                         'type')
            schema = [paramName + "|" + schemaItemsType + "|" + str(paramNeed)]
        else:
            schema = paramName + "|" + schemaType + "|" + str(paramNeed)
    else:
        if schemaRef is not None:
            definitions = getDictVal(doc, 'definitions')
            refs = schemaRef.split("/")
            refType = refs[len(refs) - 1]
            refDesc = getDictVal(definitions, refType)
            props = {}
            if refDesc is not None:
                for prop, propDesc in getDictVal(refDesc,
                                                 'properties').items():
                    props[prop] = getDictVal(propDesc, 'type')
                schema = props
            else:
                schema[paramName] = refType + "|" + str(paramNeed)
    bodyParameter.schema = schema


def parseNormalParameter(doc: dict, paramDoc: dict, parameter: Parameter):

    schema = parameter.schema

    paramName = getDictVal(paramDoc, 'name')
    paramNeed = getDictVal(paramDoc, 'required')
    paramType = getDictVal(paramDoc, 'type')

    if paramType is None:
        paramSchemaDoc = getDictVal(paramDoc, 'schema')
        schemaType = getDictVal(paramSchemaDoc, 'type')
        if schemaType is not None:
            paramType = schemaType
        else:
            schemaRef = getDictVal(paramSchemaDoc, '$ref')
            refs = schemaRef.split("/")
            paramType = refs[len(refs) - 1]

    schema[paramName] = paramType + "|" + str(paramNeed)

    parameter.schema = schema


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
