import unittest


class TestMathFunc(unittest.TestCase):

    # TestCase基类方法,所有case执行之前自动执行
    @classmethod
    def setUpClass(cls):
        print("这里是所有测试用例前的准备工作")

    # TestCase基类方法,所有case执行之后自动执行
    @classmethod
    def tearDownClass(cls):
        print("这里是所有测试用例后的清理工作")

    # TestCase基类方法,每次执行case前自动执行
    def setUp(self):
        print("这里是一个测试用例前的准备工作")

    # TestCase基类方法,每次执行case后自动执行
    def tearDown(self):
        print("这里是一个测试用例后的清理工作")

    # @unittest.skip(reason) // 无条件跳过
    # @unittest.skipIf(condition, reason) // 当condition为True时跳过
    # @unittest.skipUnless(condition, reason) // 当condition为False时跳过
    @unittest.skipIf(True, "我想临时跳过这个测试用例.")
    def test_1(self):
        self.assertEqual(2, 3)

    def test_2(self):
        self.assertEqual(1, 1)
        self.skipTest('跳过后面的测试用例')
        self.assertEqual(1, 2)
        self.assertEqual(1, 2)

    def test_3(self):
        self.assertEqual(6, 6)

    def test_4(self):
        self.assertEqual(2, 2)


if __name__ == '__main__':
    # unittest.main(verbosity=2)
    d1 = {"barcode": "123456"}
    d2 = {'User-Agent:': 'tester'}

    for k, v in d2.items():
        print(type(k))

    for k1, v1 in dict(d1, **d2).items():
        print(type(k1))
