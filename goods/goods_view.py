from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from goods.forms import *
from goods.util import Util
# Create your views here.
from goods.models import *

def goods_view(request):
    # 检查用户是否登录
    util = Util()
    username = util.check_user(request)
    if username == '':
        uf = LoginForm()
        return render(request, 'index.html', {'uf': uf, 'error': '请登录后再进入'})
    else:
        count = util.count_cookies(request)  # 当前购物车中的商品数量
        goods_list = Goods.objects.all()      # 获得所有商品信息
        #翻页操作
        pageinator = Paginator(goods_list, 3)
        page = request.GET.get('page','')
        contacts = pageinator.get_page(page)
        return render(request, 'goods_view.html', {'user':username,'count':count, 'goodss':contacts})

# 商品搜索
def search_name(request):
    # 检查用户是否登录
    util = Util()
    username = util.check_user(request)
    if username == '':
        uf = LoginForm()
        return render(request, 'index.html', {'uf': uf, 'error': '请登录后再进入'})
    else:
        count = util.count_cookies(request)  # 当前购物车中的商品数量
        search_name = request.POST.get('good','')
        good_list = Goods.objects.filter(goods_name__contains=search_name)
        pageinator = Paginator(good_list, 3)    #对查询结果进行分页显示
        page = request.GET.get('page', '')
        contacts = pageinator.get_page(page)
        return render(request, 'goods_view.html', {'user':username, 'count':count, 'goodss':contacts})

# 查看商品详细信息
def good_detail(request,good_id):
    # 检查用户是否登录
    util = Util()
    username = util.check_user(request)
    if username == '':
        uf = LoginForm()
        return render(request, 'index.html', {'uf': uf, 'error': '请登录后再进入'})
    else:
        count = util.count_cookies(request)  # 当前购物车中的商品数量
        good_detail = get_object_or_404(Goods, id=good_id)
        return render(request, 'good_details.html', {'user': username, 'count': count, 'good': good_detail})

# 加入购物车
def add_chart(request,good_id,sign):
    # 检查用户是否登录
    util = Util()
    username = util.check_user(request)
    if username == '':
        uf = LoginForm()
        return render(request, 'index.html', {'uf': uf, 'error': '请登录后再进入'})
    else:
        good = get_object_or_404(Goods, id=good_id)
        if sign=='1':
            response = HttpResponseRedirect('/goods_view/')
        else:
            response = HttpResponseRedirect('/view_goods/'+good_id)
        response.set_cookie(str(good.id), 1, 60 * 60 * 24 * 365)
        return response

# 查看购物车
def view_chart(request):
    # 检查用户是否登录
    util = Util()
    username = util.check_user(request)
    if username == '':
        uf = LoginForm()
        return render(request, 'index.html', {'uf': uf, 'error': '请登录后再进入'})
    else:
        count = util.count_cookies(request)  # 当前购物车中的商品数量
        # 返回所有cookie的内容
        my_chart_list = util.my_chart(request)
        return render(request, 'view_chart.html', {'user':username, 'count':count, 'goodss':my_chart_list})

# 修改购物车中的商品数量
def update_chart(request, good_id):
    # 检查用户是否登录
    util = Util()
    username = util.check_user(request)
    if username == '':
        uf = LoginForm()
        return render(request, 'index.html', {'uf': uf, 'error': '请登录后再进入'})
    else:
        good = get_object_or_404(Goods, id=good_id)   # 获取对应的商品
        count = request.POST.get('count'+good_id,'')    # 获取修改的数量
        if int(count)<=0:
            my_chart_list = util.my_chart(request)
            return render(request, 'view_chart.html', {'user':username, 'error':'个数不能小于等于0',
                                                       'goodss':my_chart_list})
        else:
            response = HttpResponseRedirect('/view_chart/')
            response.set_cookie(str(good.id), count, 365*24*60*60)
            return response

# 删除购物车中的某种商品
def remove_chart(request, good_id):
    # 检查用户是否登录
    util = Util()
    username = util.check_user(request)
    if username == '':
        uf = LoginForm()
        return render(request, 'index.html', {'uf': uf, 'error': '请登录后再进入'})
    else:
        good = get_object_or_404(Goods, id=good_id)  # 获取对应的商品
        response = HttpResponseRedirect('/view_chart/')
        response.set_cookie(str(good.id), 1, 0)
        return response

# 移除购物车中的所有商品
def remove_chart_all(request):
    # 检查用户是否登录
    util = Util()
    username = util.check_user(request)
    if username == '':
        uf = LoginForm()
        return render(request, 'index.html', {'uf': uf, 'error': '请登录后再进入'})
    else:
        my_chart_list = util.deal_cookes(request)
        response = HttpResponseRedirect('/view_chart/')
        for key in my_chart_list:
            response.set_cookie(str(key), 1, 0)
        return response
