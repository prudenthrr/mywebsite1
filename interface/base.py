import unittest
from interface.util import *

class TestBase(unittest.TestCase):

    def setUp(self):
        self.live_server_url = 'http://127.0.0.1:8000/'
        self.database = DB()
        self.database.connect()
        self.userTable = ''
        self.goodsTable = ''
        self.AddressTable = ''
        self.ordersTable = ''
        self.orderTable = ''
        self.util = Util()
        self.session = requests.session()
        self.sign = '0'

    # 初始化用户信息
    def get_initUserInfo(self,xml_path,Table):
        xmlInfo = GetXML(xml_path)  # 建立GetXml对象
        self.userTable = Table  # 定义数据库表名
        InitInfos = xmlInfo.getUserInitInfo()  # 获取用户的初始化信息
        # 插入初始化数据
        for values in InitInfos:
            self.database.insert(self.userTable, values)
        return InitInfos

    # 初始化商品信息
    def get_initGoodsInfo(self,xml_path,Table):
        xmlInfo = GetXML(xml_path)  # 建立GetXml对象
        self.goodsTable = Table  # 定义数据库表名
        InitInfos = xmlInfo.getGoodsInitInfo()  # 获取用户的初始化信息
        # 插入初始化数据
        for values in InitInfos:
            self.database.insert(self.goodsTable, values)
        return InitInfos

    # 初始化地址信息
    def get_initAddressInfo(self,xml_path,Table):
        xmlInfo = GetXML(xml_path)  # 建立GetXml对象
        self.AddressTable = Table  # 定义数据库表名
        InitInfos = xmlInfo.getAddressInitInfo()  # 获取用户的初始化信息
        # 插入初始化数据
        for values in InitInfos:
            self.database.insert(self.AddressTable, values)
        return InitInfos

    # 初始化总订单信息
    def get_initOrdersInfo(self,xml_path,Table):
        xmlInfo = GetXML(xml_path)  # 建立GetXml对象
        self.ordersTable = Table  # 定义数据库表名
        InitInfos = xmlInfo.getOrdersInitInfo()  # 获取用户的初始化信息
        # 插入初始化数据
        for values in InitInfos:
            self.database.insert(self.ordersTable, values)
        return InitInfos

    # 初始化单个订单信息
    def get_initOrderInfo(self,xml_path,Table):
        xmlInfo = GetXML(xml_path)  # 建立GetXml对象
        self.orderTable = Table  # 定义数据库表名
        InitInfos = xmlInfo.getOrderInitInfo()  # 获取用户的初始化信息
        # 插入初始化数据
        for values in InitInfos:
            self.database.insert(self.orderTable, values)
        return InitInfos

    # 获取测试数据
    def get_xml_data(self,xml_file):
        xmlInfo = GetXML(xml_file)  # 建立GetXml对象
        self.sign = xmlInfo.getIsLogin()
        test_datas = xmlInfo.gettestxmldata()  # 获取测试信息
        return test_datas

    def initChart(self):
        self.session.get(self.live_server_url + "remove_chart_all/")

    # 测试
    def run_test(self,test_data, userValue):
        login_url = self.live_server_url+'login_action/'   # 登录网址
        run_url = self.live_server_url+test_data["Url"]   # 运行测试网址
        username = userValue.split(',')[1].strip('\"')    # 用户名
        password = userValue.split(',')[2].strip('\"')    # 登录密码
        response = self.session.get(login_url)
        csrf_token = response.cookies["csrftoken"]       #获取csrf_token
        if self.sign=='1':
            payload = {"username": username, "password": password, "csrfmiddlewaretoken": csrf_token}
            try:
                response = self.session.post(login_url,data=payload)
            except Exception as e:
                print(e)
        try:
            if test_data["Method"] == "post":
                payload = eval(test_data["InptArg"])
                # 如果不是测试CSRF的
                if test_data["Result"] != "403":
                    payload["csrfmiddlewaretoken"] = csrf_token
                response = self.session.post(run_url, data=payload)
            elif test_data["Method"] == "get":
                if test_data["InptArg"]=='':
                    response = self.session.get(run_url)
                else:
                    payload = eval(test_data["InptArg"])
                    response = self.session.get(run_url, params=payload)
        except Exception as e:
            print(e)
        return response

    # 总的数据库表
    def clear_database(self):
        database_list = []
        database_list.append(self.userTable)
        database_list.append(self.AddressTable)
        database_list.append(self.goodsTable)
        database_list.append(self.ordersTable)
        database_list.append(self.orderTable)
        for key in database_list:
            if key != '':
                # 删除用例
                re = self.database.searchByid(key)
                for value in re:
                    id = value[0]
                    self.database.delete(key, id)

    def tearDown(self):
        self.clear_database()
        self.database.close()
        # print('-------------------------结束---------------------------')

