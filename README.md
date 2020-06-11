# 1. api_test
<!-- TOC -->

- [1. api_test](#1-api_test)
    - [1.1. background](#11-background)
    - [1.2. good point](#12-good-point)
    - [1.3. usage](#13-usage)

<!-- /TOC -->
## 1.1. background

针对 `spring boot` 的 `swagger`接口文档，生成**测试人员**能**测试**用的接口文档-`api.json`

## 1.2. good point

1. 测试人员不需要过多关注`http`协议 和 接口参数包装。这些都有程序根据文档自动识别。

2. 测试人员只需 知道 接口对应的功能 和 参数内容填充, 一个方法就能完成接口调用

## 1.3. usage

1. 目录结构
```
api_test
├─api
|  ├─access.py
|  ├─doc.py
|  ├─util.py
|  ├─__init__.py
├─conf
|  ├─config.py
|  ├─init.cfg
|  ├─__init__.py
├─htr
|  ├─HTMLTestRunner.py
|  ├─__init__.py
├─.gitignore
├─api.json
├─api_doc.py
├─api_test.py
├─HTMLReport.html
├─README.md
├─requirements.txt
├─test.py
```
2. config

```properties
[doc]
url = http://10.87.200.21:8875/v2/api-docs //swagger url
file = api.json // 生成文档名
html = HTMLReport.html // 生成的测试报告名
```

3. 爬取`swagger`文档,重构成`api.json`

```sh
> cd api_test
> python api_doc.py
```

[代码实现]("./api_doc.py")

4. `api.json`结构example
```json
{
  "host": "10.87.200.21:8875",
  "apis": [
    {
      "summary": "api登录",
      "tags": "api-login-controller",
      "path": "/winApi/auth",
      "method": "post",
      "parameters": [
        {
          "position": "header",
          "schema": {
            "Authorization": "string|False"
          }
        },
        {
          "position": "query",
          "schema": {
            "imei": "string|False",
            "password": "string|False",
            "username": "string|False"
          }
        }
      ]
    }
  ]
}

```

5. 根据`api.json`访问接口

```py
from api.access import *
from conf.config import Config


def login():
    '''
    :param path: 对应 api.json 中 接口path 属性, 
    :param parameters: 对应 api.json 中 接口parameters列表中的 schema 属性, 顺序保持一致
    '''
    return doRequest('/winApi/auth', [{
        "Authorization": "your express"
    }, {
        "imei": "your express",
        "password": "your express",
        "username": "your express"
    }])
if __name__ == '__main__':
    # 加载配置
    cfg = Config()
    # 加载 测试接口文档 api.json
    loadApisDoc(cfg.doc_file)
    # 访问接口
    login()
```

6. 接口测试

[代码参考]("./api_test.py")
