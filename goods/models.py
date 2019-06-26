from django.db import models

# Create your models here.
# 用户信息
class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.username
# 收货地址
class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)     # 外键
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.address

# 商品
class Goods(models.Model):
    goods_name = models.CharField(max_length=100)   # 字符串类型，必须设置max_length属性，而且时正整数
    goods_price = models.FloatField()               # 浮点类型
    picture = models.FileField(upload_to='./upload/')      # 文件类型，必须设置upload_to
    description = models.TextField()                # 文本类型

    def __str__(self):
        return self.goods_name

# 总订单
class Orders(models.Model):
    address = models.ForeignKey(Address,on_delete=models.CASCADE)
    creat_time = models.DateTimeField(auto_now=True)   # 时间字段
    status = models.BooleanField()     #订单状态

    def __str__(self):
        return self.creat_time

# 单个订单
class Order(models.Model):
    order = models.ForeignKey(Orders,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    count = models.IntegerField()
