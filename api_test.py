# !usr/bin/env python3
#  -*- coding:utf-8 -*-

import unittest

from api.access import *

from conf.config import Config

cfg = Config()

# loadApisDoc(cfg.doc_file)


class LoginTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        loadApisDoc(cfg.doc_file)

    def test_login(self):
        resp = doRequest('/user/login', [{
            'name': 'admin',
            'password': '123456'
        }])
        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(resp.json()['data']['token'])
        self.assertEqual(resp.json()['data']['token'], '123456')


if __name__ == "__main__":
    unittest.main()
