from django.core.paginator import Paginator, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from goods.forms import *
from goods.util import Util

# Create your views here.
from goods.models import *


# 首页
def index(request):
    uf = LoginForm()
    return render(request,'index.html',{'uf':uf})

# 用户登录
def login_action(request):
    util = Util()
    if request.method=="POST":
        uf = LoginForm(request.POST)
        if uf.is_valid():
            username = request.POST.get('username','')
            password = request.POST.get('password','')
            password = util.md5(password)
            if username=='' or password=='':
                render(request, 'index.html', {'uf':uf, 'error':'用户名或者密码不能为空'})
            else:
                is_usr = User.objects.filter(username=username)
                if not is_usr :
                    return render(request, 'index.html',{'uf':uf, 'error': '用户名不存在，请注册'})
                else:
                    user_info = User.objects.filter(username=username, password=password)
                    if user_info:
                        request.session['username'] = username
                        return redirect('/goods_view/')
                        # return render(request, 'index.html', {'uf': uf, 'error': '查看购物车'})
                    else:
                        return render(request, 'index.html', {'uf': uf, 'error': '用户名或密码错误'})
    else:
        uf = LoginForm()
        return render(request, 'index.html',{'uf':uf})

# 用户注册
def register(request):
    util = Util()
    if request.method=='POST':
        uf = UserForm(request.POST)
        if uf.is_valid():
            # 获取表单信息
            username = request.POST.get('username','')  # 获取用户名
            password = request.POST.get('password','')   #获取密码
            email = request.POST.get('email','')
            password = util.md5(password)
            user_list = User.objects.filter(username=username)
            if user_list:
                # 当前用户存在
                return render(request,'register.html', {'uf':uf, 'error':'用户名已存在！'})
            else:
                User.objects.create(username=username,password=password,email=email)
                # 返回登录界面
                uf = LoginForm()
                return render(request, 'index.html', {'uf': uf, 'error':'用户名已注册！请登录'})
    else:
        uf = UserForm()
        return render(request,'register.html', {'uf':uf})

# 用户信息展示
def user_info(request):
    # 检查用户是否登录
    util = Util()
    username = util.check_user(request)
    if username=='':
        uf = LoginForm()
        return render(request, 'index.html',{'uf':uf, 'error':'请登录后再进入'})
    else:
        count = util.count_cookies(request)   #当前购物车中的商品数量
        # 获取登录的用户信息
        user_list = get_object_or_404(User,username=username)
        # 获取登录用户收货地址的所有信息
        address_list = Address.objects.filter(user_id=user_list.id)
        return render(request, 'view_user.html', {"user":username, 'user_info':user_list,
                                                 'address':address_list, 'count':count})

# 修改用户密码
def change_password(request):
    # 检查用户是否登录
    util = Util()
    username = util.check_user(request)
    if username == '':
        uf = LoginForm()
        return render(request, 'index.html', {'uf': uf, 'error': '请登录后再进入'})
    else:
        count = util.count_cookies(request)  # 当前购物车中的商品数量
        uf = ChangePasswordForm()
        user_list = get_object_or_404(User, username=username)  # 获取登录的用户信息
        if request.method=='POST':
            uf = ChangePasswordForm(request.POST)
            if uf.is_valid():
                oldpassword = util.md5(request.POST.get('oldpassword',''))   # 获取旧密码
                newpassword = util.md5(request.POST.get('newpassword','') )  # 获取新密码
                checkpassword = util.md5(request.POST.get('checkpassword',''))   # 获取确认密码
                if oldpassword != user_list.password:
                    return render(request, 'change_password.html', {'uf':uf,'user':username, 'error':'旧密码不正确',
                                                                    'count':count})
                elif newpassword == oldpassword:
                    return render(request, 'change_password.html', {'uf':uf,'user':username, 'error':'新密码不能与旧密码相同',
                                                                    'count':count})
                elif newpassword != checkpassword:
                    return render(request, 'change_password.html', {'uf':uf,'user':username, 'error':'确认密码与新密码不匹配',
                                                                    'count':count})
                else:
                    User.objects.filter(username=username).update(password=newpassword)
                    return render(request, 'change_password.html',{'uf':uf,'user':username, 'error':'密码修改成功',
                                                                   'count':count})
        else:
            return render(request, 'change_password.html', {'uf':uf,'user':username, 'count':count})

#用户登出
def logout(request):
    del request.session['username']  # 将session 信息写到服务器
    return redirect('/index/')