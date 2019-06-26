from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from goods.forms import *
from goods.util import Util
from goods.models import *

# 查看送货地址信息
def view_address(request):
    # 检查用户是否登录
    util = Util()
    username = util.check_user(request)
    if username == '':
        uf = LoginForm()
        return render(request, 'index.html', {'uf': uf, 'error': '请登录后再进入'})
    else:
        user_list = get_object_or_404(User, username=username)  # 获取登录的用户信息
        address_list = Address.objects.filter(user_id=user_list.id)
        return render(request, 'view_address.html', {'user':username, 'address':address_list})

# 添加地址
# sign=1 从用户信息中进行添加
# sign=2 从地址信息页面中进行添加
def add_address(request, sign):
    # 检查用户是否登录
    util = Util()
    username = util.check_user(request)
    if username == '':
        uf = LoginForm()
        return render(request, 'index.html', {'uf': uf, 'error': '请登录后再进入'})
    else:
        user_list = get_object_or_404(User, username=username)  # 获取登录的用户信息
        if request.method=="POST":
            uf = AddressForm(request.POST)
            if uf.is_valid():
                address = request.POST.get('address','')
                phone = request.POST.get('phone', '')
                check_address = Address.objects.filter(address=address, user_id=user_list.id)
                if check_address:
                    return render(request, 'add_address.html', {'uf':uf, 'error':'这个地址已经存在'})
                else:
                    Address.objects.create(user_id=user_list.id, address=address, phone=phone)
                    address_list = Address.objects.filter(user_id=user_list.id)
                    if sign=='2':
                        return render(request, 'view_address.html',{'user':username, 'addresses':address_list})
                    else:
                        return redirect('/user_info/')
            else:
                uf = AddressForm()
                return render(request, 'add_address.html', {'uf':uf})
# 修改地址
def update_address(request, address_id, sign):
    # 检查用户是否登录
    util = Util()
    username = util.check_user(request)
    if username == '':
        uf = LoginForm()
        return render(request, 'index.html', {'uf': uf, 'error': '请登录后再进入'})
    else:
        # 判断修改地址是否为当前登录用户
        if not util.check_User_By_Address(username=username, address_id=address_id):
            return render(request, 'error.html',{'user':username, 'error':'你试图修改不属于你的地址'})
        cur_address = get_object_or_404(Address, id=address_id)
        user_list = get_object_or_404(User, username=username)  # 获取登录的用户信息
        if request.method=='POST':
            uf = AddressForm(request.POST)
            if uf.is_valid():
                new_address = request.POST.get('address','')
                new_phone = request.POST.get('phone', '')
                check_address = Address.objects.filter(address=new_address, user_id=user_list.id)
                if check_address:
                    return render(request, 'update_address.html', {'address':cur_address, 'error':'这个地址已经存在'})
                else:
                    Address.objects.filter(id=address_id).update(address=new_address,phone=new_phone)
                    address_list = Address.objects.filter(user_id=user_list.id)
                    if sign=='2':
                        return render(request, 'view_address.html', {'user': username, 'addresses': address_list})
                    else:
                        return redirect('/user_info/')
        else:
            return render(request,'update_address.html',{'address':cur_address})

# 删除地址
def delete_address(request, address_id, sign):
    # 检查用户是否登录
    util = Util()
    username = util.check_user(request)
    if username == '':
        uf = LoginForm()
        return render(request, 'index.html', {'uf': uf, 'error': '请登录后再进入'})
    else:
        # 判断修改地址是否为当前登录用户
        if not util.check_User_By_Address(username=username, address_id=address_id):
            return render(request, 'error.html', {'user': username, 'error': '你试图修改不属于你的地址'})
        user_list = get_object_or_404(User, username=username)  # 获取登录的用户信息
        Address.objects.filter(id=address_id).delete()
        address_list = Address.objects.filter(user_id=user_list.id)
        if sign=='2':
            return render(request, 'view_address.html', {'user': username, 'addresses': address_list})
        else:
            return redirect('/user_info/')