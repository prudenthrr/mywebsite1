from interface import HTMLTestRunner
import unittest
from interface.test_interface  import MyTest

suite = unittest.TestSuite()
# 获取TestSuite的实例对象，并加入
suite.addTest(MyTest("test_page"))
suite.addTest(MyTest("test_login_and_register"))
suite.addTest(MyTest("test_show_user_info"))
suite.addTest(MyTest("test_page_show_goods"))
# 文件名
filename = "test.html"
fp = open(filename, "wb")
# 以二进制的方式打开文件并写入结果
runner = HTMLTestRunner.HTMLTestRunner(
    stream=fp,
    verbosity=2,
    title="测试报告的标题",
    description="测试报告的详情")
runner.run(suite)
fp.close()