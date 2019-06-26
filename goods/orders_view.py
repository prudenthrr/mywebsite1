from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from goods.forms import *
from goods.util import Util
from goods.models import *
from goods.object import Order_list

# 创建单个订单
def create_order(request):
    # 检查用户是否登录
    util = Util()
    username = util.check_user(request)
    if username == '':
        uf = LoginForm()
        return render(request, 'index.html', {'uf': uf, 'error': '请登录后再进入'})
    else:
        user_list = get_object_or_404(User, username=username)
        address_id = request.POST.get('address','')
        if address_id=='':
            address_list = Address.objects.filter(user_id=user_list.id)
            return render(request, 'view_address.html', {'user':username, 'addresses':address_list, 'error':'必须选择一个地址'})
        else:
            orders = Orders()
            orders.address_id = int(address_id)
            orders.status = False
            orders.save()    # 创建一个总订单
            mychart_list = util.deal_cookes(request)   # 获取购物车中的所有商品列表
            # 将每个商品创建一个订单
            for key in mychart_list:
                Order.objects.create(order_id=orders.id, goods_id=key, user_id=user_list.id,
                                     count=int(mychart_list[key]))
            # 清除所有的cookies并显示总订单
            response = HttpResponseRedirect('/view_orders/'+str(orders.id))
            for key in mychart_list:
                response.set_cookie(key,1,0)
            return response

# 显示总订单
def view_orders(request, orders_id):
    # 检查用户是否登录
    util = Util()
    username = util.check_user(request)
    if username == '':
        uf = LoginForm()
        return render(request, 'index.html', {'uf': uf, 'error': '请登录后再进入'})
    else:
        orders_filter = get_object_or_404(Orders, id=orders_id)
        address_list = get_object_or_404(Address, id=orders_filter.address_id)
        address = address_list.address
        order_filter = Order.objects.filter(order_id=orders_filter.id)
        sum_price = 0
        order_list_var = []
        for order in order_filter:
            order_object = util.set_order_list(order)
            sum_price += order_object.price * order_object.count
            order_list_var.append(order_object)
        return render(request, 'view_order.html',{'user':username, 'orders':orders_filter,'address':address,
                                                  'prices':sum_price,'order':order_list_var})

# 显示所有总订单
def view_all_orders(request):
    # 检查用户是否登录
    util = Util()
    username = util.check_user(request)
    if username == '':
     uf = LoginForm()
     return render(request, 'index.html', {'uf': uf, 'error': '请登录后再进入'})
    else:
     orders_all = Orders.objects.all()
     orders_set = []
     for key1 in orders_all:
         order_all = Order.objects.filter(order_id=key1.id)  # 获取该总订单的所有单个订单
         cur_user = get_object_or_404(User, id=order_all[0].user_id)
         if cur_user.username==username:
             order_object_list = []
             prices = 0
             for key in order_all:
                 order_object = util.set_order_list(key)
                 prices = order_object.price*order_object.count + prices
                 order_object.set_prices(prices)
                 order_object_list.append(order_object)
             orders_prices = order_object_list[-1].prices
             orders_object = util.set_orders_list(key1,orders_prices)
             orders_set.append({orders_object:order_object_list})
     return render(request, 'view_all_order.html',{'user':username, 'Orders_set':orders_set})

# 删除订单
def delete_orders(request, orders_id, sign):
    # 检查用户是否登录
    util = Util()
    username = util.check_user(request)
    if username == '':
        uf = LoginForm()
        return render(request, 'index.html', {'uf': uf, 'error': '请登录后再进入'})
    else:
        if sign=='1' or sign=='3':
            # 判断修改地址是否为当前登录用户
            if not util.check_User_By_Order(username, orders_id):
                return render(request, 'error.html', {'user': username, 'error': '你试图修改不属于你的订单'})
            order = get_object_or_404(Order, id=orders_id)    # 获取当前的单个订单
            orders = get_object_or_404(Orders, id=order.order_id)  # 获取单个订属于的总订单
            Order.objects.filter(id=orders_id).delete()   # 删除单个订单
            check_cue_order = Order.objects.filter(order_id=orders.id)
            if len(check_cue_order)==0:
                Orders.objects.filter(id=orders.id).delete()   # 删除总订单
                if sign=='3':
                    return redirect('/goods_view/')
                else:
                    return redirect('/view_all_orders/')
            elif sign=='3':
                return redirect('/view_orders/'+str(orders.id)+'/')
            else:
                return redirect('/view_all_orders/')
        else:
            if not util.check_User_By_Orders(username, orders_id):
                return render(request, 'error.html', {'user': username, 'error': '你试图修改不属于你的订单'})
            Order.objects.filter(order_id=orders_id).delete()
            Orders.objects.filter(id=orders_id).delete()
            return redirect('/view_all_orders/')