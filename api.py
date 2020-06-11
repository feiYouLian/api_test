from api.access import *
from conf.config import Config


def login():
    '''
    :param path: 对应 api.json 中 接口path 属性, 
    :param parameters: 对应 api.json 中 接口parameters列表中的 schema 属性, 顺序保持一致
    '''
    return doRequest('/user/delete', [
        {
            "idList": [10, 11]
        },
    ])


if __name__ == '__main__':
    # 加载配置
    cfg = Config()
    # 加载 测试接口文档 api.json
    loadApisDoc(cfg.doc_file)
    # 访问接口
    login()
