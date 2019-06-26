import hashlib

from django.shortcuts import get_object_or_404

from goods.models import *
from goods.object import *


class Util:
    # MD5加密
    def md5(self, mystr):
        if isinstance(mystr, str):
            m = hashlib.md5()
            m.update(mystr.encode('utf8'))
            return m.hexdigest()
        else:
            return ""

    #检查用户登录
    def check_user(self,request):
        username = request.session.get('username','')
        user = User.objects.filter(username=username)
        if user:
            return username
        else:
            return ''

    # 判断这个地址是否属于当前用户
    def check_User_By_Address(self, username, address_id):
        address = get_object_or_404(Address, id=address_id)
        user = get_object_or_404(User, username=username)
        return user.id == address.user_id

    # 判断这个地址是否属于当前用户
    def check_User_By_Order(self, username, order_id):
        order = get_object_or_404(Order, id=order_id)
        user = get_object_or_404(User, username=username)
        return user.id == order.user_id

    # 判断这个地址是否属于当前用户
    def check_User_By_Orders(self, username, orders_id):
        order_all = Order.objects.filter(order_id=orders_id)
        user = get_object_or_404(User, username=username)
        if len(order_all)>0:
            return order_all[0].user_id==user.id
        else:
            return False

    # 返回购物车内商品的数量
    def count_cookies(self,request):
        cookies_list = request.COOKIES
        length = len(cookies_list)
        for i in cookies_list:
            if (i == "csrftoken") or (i == "sessionid") or (i.startswith("Hm_lvt_")) or (i.startswith("Hm_lpvt_")):
                length = length - 1
        return length

    def my_chart(self, request):
        # 获取购物车内的所有内容
        cookie_list = self.deal_cookes(request)
        # 定义my_chart_list列表
        my_chart_list = []
        # 遍历cookie_list，把里面的内容加入类Chart_list列my_chart_list中
        for key in cookie_list:
            chart_object = self.set_chart_list(key, cookie_list)
            my_chart_list.append(chart_object)
        # 返回 my_chart_list
        return my_chart_list

    # 获取购物车内的所有内容
    def deal_cookes(self, request):
        # 获取本地所有内COOKIES
        cookie_list = request.COOKIES
        # 去除COOKIES内的sessionid
        cookie_list.pop("sessionid")
        # 如果COOKIES内含有csrftoken，去除COOKIES内的csrftoken
        for key in list(cookie_list.keys()):
            if (key == "csrftoken") or (key == "sessionid") or (key.startswith("Hm_lvt_")) or (
                key.startswith("Hm_lpvt_")):
                del cookie_list[key]
        # 返回处理好的购物车内的所有内容
        return cookie_list

    # 把获取的购物车中的商品放在一个名为Chart_list()的类中，返回给模板
    def set_chart_list(self, key, cookie_list):
        chart_list = Chart_list()
        good_list = get_object_or_404(Goods, id=key)
        chart_list.set_id(key)  # 商品的标号
        chart_list.set_name(good_list.goods_name)  # 商品的名称
        chart_list.set_price(good_list.goods_price)  # 商品的价钱
        chart_list.set_count(cookie_list[key])  # 商品的个数
        return chart_list

    # 定义单个订单变量
    def set_order_list(self, key):
        order_list = Order_list()
        order_list.set_id(key.id)  # 主键
        good_list = get_object_or_404(Goods, id=key.goods_id)  # 获得当前商品信息
        order_list.set_good_id(good_list.id)  # 订单中商品编号
        order_list.set_name(good_list.goods_name)  # 订单中商品名字
        order_list.set_price(good_list.goods_price)  # 订单中商品价格
        order_list.set_count(key.count)  # 购买数量
        return order_list

    # 定义一个总订单
    def set_orders_list(self, key, prices):
        orders_list = Orders_list()
        orders_list.set_id(key.id)
        address_list = get_object_or_404(Address, id=key.address_id)
        orders_list.set_address(address_list.address)
        # orders_list.set_address(key.address)
        orders_list.set_create_time(key.creat_time)
        orders_list.set_prices(prices)
        return orders_list


