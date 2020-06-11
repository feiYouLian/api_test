# !usr/bin/env python3
#  -*- coding:utf-8 -*-

import unittest
from htr.HTMLTestRunner import *
from api.access import *

from conf.config import Config

cfg = Config()

#########################
emptyAuth = {'Authorization': ''}
loginUser = {
    "username": "admin",
    "password": "111111",
}

antifakeCode = {"barcode": "123456"}

testHeader = {'User-Agent': 'tester'}


def login():
    return doRequest('/winApi/auth', [emptyAuth, loginUser],
                     headers=testHeader)


def login2(username: str, password: str):
    return doRequest(
        '/winApi/auth',
        [emptyAuth, {
            "username": username,
            "password": password,
        }],
        headers=testHeader)


def antifake(authorization: str):
    return doRequest('/winApi/channel/antifake',
                     [{
                         'Authorization': authorization
                     }, antifakeCode],
                     headers=testHeader)


class LoginTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        loadApisDoc(cfg.doc_file)

    def test_antifake(self):
        r = login()
        r4 = antifake(r.json()['data']['token'])
        self.assertNotEqual(r4.status_code, 200)

    def test_login(self):
        r = login2("", "")
        self.assertNotEqual(r.status_code, 200)

        r2 = login2("admin", "")
        self.assertNotEqual(r2.status_code, 200)

        r3 = login2("admin", "admin")
        self.assertNotEqual(r3.status_code, 200)

        r4 = login2("admin", "111111")
        self.assertEqual(r4.status_code, 200)
        self.assertIsNotNone(r4.json()['data']['token'])

        r5 = antifake('')
        self.assertNotEqual(r5.status_code, 200)

        r6 = antifake(r4.json()['data']['token'])
        self.assertEqual(r6.status_code, 200)


if __name__ == '__main__':
    # unittest.main()

    suite = unittest.TestSuite()
    # suite.addTest(LoginTest('test_login'))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(LoginTest))

    with open(cfg.doc_html, 'wb') as f:
        runner = HTMLTestRunner(stream=f,
                                title='Api Test Report',
                                description='generated by HTMLTestRunner.',
                                verbosity=2)
        runner.run(suite)
