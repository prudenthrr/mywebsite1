from django import forms

from goods.models import Address


class UserForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=100)
    # widget=forms.PasswordInput() 表示文本信息为密码格式
    password = forms.CharField(label='密码', widget=forms.PasswordInput())
    email = forms.EmailField(label='电子邮箱')

class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=100)
    password = forms.CharField(label='密码', widget=forms.PasswordInput())

class ChangePasswordForm(forms.Form):
    oldpassword = forms.CharField(label='旧密码', widget=forms.PasswordInput())
    newpassword = forms.CharField(label='新密码', widget=forms.PasswordInput())
    checkpassword = forms.CharField(label='确认密码', widget=forms.PasswordInput())

class AddressForm(forms.Form):
    address = forms.CharField(label='地址', max_length=100)
    phone = forms.CharField(label='电话', max_length=15)