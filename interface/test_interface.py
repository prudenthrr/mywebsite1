import requests
from interface.base import TestBase

class MyTest(TestBase):

    def test_page(self):
        print('-------------------------首页测试开始---------------------------')
        response = requests.get(self.live_server_url)
        self.assertEqual(200, response.status_code)
        url = self.live_server_url + 'index/'
        response = requests.get(url)
        self.assertEqual(200, response.status_code)
        print('------------------------首页测试结束----------------------------')

    # 用户登录， 注册，
    def test_login_and_register(self):
        print('---------------------用户登录和注册测试开始----------------------')
        # 初始化数据库
        userInit_xml = './interface/initInfo.xml'
        initInfos = self.get_initUserInfo(userInit_xml, 'goods_user')
        usreinfo_xml = './interface/loginRegConfig.xml'
        test_datas = self.get_xml_data(usreinfo_xml)
        for test_data in test_datas:
            for value in initInfos:
                response = self.run_test(test_data, value)
                self.assertEqual(test_data['Result'], str(response.status_code))
                self.assertIn(test_data['CheckWord'], response.content.decode())
        print('--------------------用户登录和注册测试结合素----------------------')

    # 用户信息显示，密码修改
    def test_show_user_info(self):
        print('--------------------用户信息显示测试开始-------------------------')
        # 初始化数据库
        userInit_xml = './interface/initInfo.xml'
        initInfos = self.get_initUserInfo(userInit_xml, 'goods_user')
        usreinfo_xml = './interface/userInfoConfig.xml'
        test_datas = self.get_xml_data(usreinfo_xml)
        for test_data in test_datas:
            for value in initInfos:
                response = self.run_test(test_data, value)
                self.assertEqual(test_data['Result'], str(response.status_code))
                self.assertIn(test_data['CheckWord'], response.content.decode())
        print('----------------------用户信息显示测试结束-----------------------')

    # 商品搜索   商品详情展示  翻页显示所有商品的列表展示
    def test_search_good(self):
        print('----------------------显示所有商品测试开始-----------------------')
        InitInfo_xml = './interface/initInfo.xml'
        inituserInfos = self.get_initUserInfo(InitInfo_xml, 'goods_user')
        self.get_initGoodsInfo(InitInfo_xml, 'goods_goods')
        goods_test_config = './interface/goodsConfig.xml'
        test_datas = self.get_xml_data(goods_test_config)
        for test_data in test_datas:
            for value in inituserInfos:
                response = self.run_test(test_data, value)
                self.assertEqual(test_data['Result'], str(response.status_code))
                if 'NOT' in test_data['CheckWord']:
                    self.assertNotIn(test_data['CheckWord'].split(',')[1], response.content.decode())
                else:
                    self.assertIn(test_data['CheckWord'], response.content.decode())
        print('---------------------显示所有商品测试结束------------------------')

    # 加入购物车， 查看购物车，修改商品数量， 删除指定商品，删除所有商品
    def test_add_chart(self):
        print('-------------------------购物车测试开始-------------------------')
        self.initChart()       # 初始化购物车
        InitInfo_xml = './interface/initInfo.xml'
        inituserInfos = self.get_initUserInfo(InitInfo_xml, 'goods_user')
        self.get_initGoodsInfo(InitInfo_xml, 'goods_goods')
        test_config = './interface/chartConfig.xml'
        test_datas = self.get_xml_data(test_config)
        for test_data in test_datas:
            for value in inituserInfos:
                response = self.run_test(test_data, value)
                self.assertEqual(test_data['Result'], str(response.status_code))
                if 'NOT' in test_data['CheckWord']:
                    self.assertNotIn(test_data['CheckWord'].split(',')[1], response.content.decode())
                else:
                    self.assertIn(test_data['CheckWord'], response.content.decode())
        print('-------------------------购物车测试结束-------------------------')

    # 新增地址，展示所有的地址信息，修改地址信息
    def test_add_address(self):
        print('-------------------------地址测试开始-------------------------')
        InitInfo_xml = './interface/initInfo.xml'
        inituserInfos = self.get_initUserInfo(InitInfo_xml, 'goods_user')
        self.get_initAddressInfo(InitInfo_xml, 'goods_address')
        test_config = './interface/addressConfig.xml'
        test_datas = self.get_xml_data(test_config)
        for test_data in test_datas:
            for value in inituserInfos:
                response = self.run_test(test_data, value)
                self.assertEqual(test_data['Result'], str(response.status_code))
                if 'NOT' in test_data['CheckWord']:
                    self.assertNotIn(test_data['CheckWord'].split(',')[1], response.content.decode())
                else:
                    self.assertIn(test_data['CheckWord'], response.content.decode())
        print('-------------------------地址测试结束-------------------------')

    # 显示总订单
    def test_show_orders(self):
        print('-------------------------总订单测试开始-------------------------')
        InitInfo_xml = './interface/initInfo.xml'
        inituserInfos = self.get_initUserInfo(InitInfo_xml, 'goods_user')
        self.get_initGoodsInfo(InitInfo_xml, 'goods_goods')
        self.get_initAddressInfo(InitInfo_xml, 'goods_address')
        self.get_initOrdersInfo(InitInfo_xml, 'goods_orders')
        self.get_initOrderInfo(InitInfo_xml, 'goods_order')
        test_config = './interface/orderConfig.xml'
        test_datas = self.get_xml_data(test_config)
        for test_data in test_datas:
            for value in inituserInfos:
                response = self.run_test(test_data, value)
                self.assertEqual(test_data['Result'], str(response.status_code))
                if 'NOT' in test_data['CheckWord']:
                    self.assertNotIn(test_data['CheckWord'].split(',')[1], response.content.decode())
                else:
                    self.assertIn(test_data['CheckWord'], response.content.decode())
        print('-------------------------总订单测试结束-------------------------')