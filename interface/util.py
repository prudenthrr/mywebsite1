import hashlib
import sqlite3
from xml.dom import minidom
import os
import requests


class GetXML:
    def __init__(self,myXmlFile):
        '''
        xml.dom.minidom.parse() 用于打开一个xml文件，并将这个文件对象dom变量。
        documentElement 用于得到dom对象的文档元素，并把获得的对象给root
        :param myXmlFile:
        '''
        dom = minidom.parse(myXmlFile)
        self.root = dom.documentElement

    # 获取xml文件中测试用例的测试数据
    def gettestxmldata(self):
        TestIds = self.root.getElementsByTagName('TestId')
        Titles = self.root.getElementsByTagName('Title')
        Methods = self.root.getElementsByTagName('Method')
        Descs = self.root.getElementsByTagName('Desc')
        Urls = self.root.getElementsByTagName('Url')
        InptArgs = self.root.getElementsByTagName('InptArg')
        Results = self.root.getElementsByTagName('Result')
        CheckWords = self.root.getElementsByTagName('CheckWord')
        mylist = []     # 存储每个测试用例的字典形式
        for i,TestId in enumerate(TestIds):
            # 获得标签对之间的数据
            mydicts = {}
            mydicts['TestId'] = (TestIds[i].firstChild.data).strip()
            mydicts['Title'] = (Titles[i].firstChild.data).strip()
            mydicts['Method'] = (Methods[i].firstChild.data).strip()
            mydicts['Desc'] = (Descs[i].firstChild.data).strip()
            mydicts['Url'] = (Urls[i].firstChild.data).strip()
            if InptArgs[i].firstChild is not None :
                mydicts['InptArg'] = (InptArgs[i].firstChild.data).strip()
            else:
                mydicts['InptArg'] = ''
            mydicts['Result'] = (Results[i].firstChild.data).strip()
            mydicts['CheckWord'] = (CheckWords[i].firstChild.data).strip()
            mylist.append(mydicts)
        return mylist

    # 获取用户的初始化数据
    def getUserInitInfo(self):
        InitInfos = []
        ids = self.root.getElementsByTagName('id')
        usernames = self.root.getElementsByTagName('username')
        passwords = self.root.getElementsByTagName('password')
        emails = self.root.getElementsByTagName('email')
        for i,username in enumerate(usernames):
            id = (str(ids[i].firstChild.data)).strip()
            username = "\""+(usernames[i].firstChild.data).strip()+"\""
            password = "\""+(passwords[i].firstChild.data).strip()+"\""
            password = Util.md5(password)
            email = "\""+(emails[i].firstChild.data).strip()+"\""
            values = id+","+username+","+password+","+email
            InitInfos.append(values)
        return InitInfos

    # 获取商品的初始化信息
    def getGoodsInitInfo(self):
        InitInfos = []
        goodids = self.root.getElementsByTagName('goodid')
        names = self.root.getElementsByTagName('name')
        prices = self.root.getElementsByTagName('price')
        pictures = self.root.getElementsByTagName('picture')
        descriptions = self.root.getElementsByTagName('desc')
        for i,username in enumerate(goodids):
            id = (str(goodids[i].firstChild.data)).strip()
            name = "\""+(names[i].firstChild.data).strip()+"\""
            price = "\""+(prices[i].firstChild.data).strip()+"\""
            picture = "\""+(pictures[i].firstChild.data).strip()+"\""
            desc = "\"" + (descriptions[i].firstChild.data).strip() + "\""
            values = id+","+name+","+price+","+picture+","+desc
            InitInfos.append(values)
        return InitInfos

    # 获取地址的初始化信息
    def getAddressInitInfo(self):
        InitInfos = []
        addressids = self.root.getElementsByTagName('addressid')
        addresses = self.root.getElementsByTagName('address')
        phones = self.root.getElementsByTagName('phone')
        userids = self.root.getElementsByTagName('userid')
        for i, username in enumerate(addressids):
            addressid = (str(addressids[i].firstChild.data)).strip()
            address = "\"" + (addresses[i].firstChild.data).strip() + "\""
            phone = "\"" + (phones[i].firstChild.data).strip() + "\""
            userid = (str(userids[i].firstChild.data)).strip()
            values = addressid + "," + address + "," + phone + "," + userid
            InitInfos.append(values)
        return InitInfos

    # 获取总订单的初始化信息
    def getOrdersInitInfo(self):
        InitInfos = []
        ordersids = self.root.getElementsByTagName('ordersid')
        createtimes = self.root.getElementsByTagName('createtime')
        statuses = self.root.getElementsByTagName('status')
        ordersaddressids = self.root.getElementsByTagName('ordersaddressid')
        for i, username in enumerate(ordersids):
            ordersid = (str(ordersids[i].firstChild.data)).strip()
            createtime = "\"" + (createtimes[i].firstChild.data).strip() + "\""
            status = (str(statuses[i].firstChild.data)).strip()
            ordersaddressid = (str(ordersaddressids[i].firstChild.data)).strip()
            values = ordersid + "," + createtime + "," + status + "," + ordersaddressid
            InitInfos.append(values)
        return InitInfos

    # 获取单个订单的初始化信息
    def getOrderInitInfo(self):
        InitInfos = []
        orderids = self.root.getElementsByTagName('orderid')
        counts = self.root.getElementsByTagName('count')
        ordergoodids = self.root.getElementsByTagName('ordergoodid')
        orderorderids = self.root.getElementsByTagName('orderorderid')
        orderuserids = self.root.getElementsByTagName('orderuserid')
        for i, username in enumerate(orderids):
            orderid = (str(orderids[i].firstChild.data)).strip()
            count = (str(counts[i].firstChild.data)).strip()
            ordergoodid = (str(ordergoodids[i].firstChild.data)).strip()
            orderorderid = (str(orderorderids[i].firstChild.data)).strip()
            orderuserid = (str(orderuserids[i].firstChild.data)).strip()
            values = orderid + "," + count + "," + ordergoodid + "," + orderorderid + "," + orderuserid
            InitInfos.append(values)
        return InitInfos

    # 获取测试XML文件中的是否需要登录的信息
    def getIsLogin(self):
        # 从XML中读取数据
        login = self.root.getElementsByTagName('login')
        login = (str(login[0].firstChild.data)).strip()
        return login

class DB:
    #构造方法，获取sqlite3数据库文件的位置
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        #self.url = '/media/gzr/HRR/mywebsite1/db.sqlite3'
        self.url = os.path.join(base_dir,'db.sqlite3')

    # 连接数据库
    def connect(self):
        self.con = sqlite3.connect(self.url)
        self.cur = self.con.cursor()

    # 关闭数据库
    def close(self):
        self.cur.close()
        self.con.close()

    # 通过主键查询数据库表中的内容
    def searchByid(self, tablename, id=None):
        if id== None:
            self.cur.execute("select * from " + tablename)
        else:
            self.cur.execute("select * from " + tablename + " where id=" + str(id))
        re = self.cur.fetchall()
        return re

    # 向tablename表中插入数据values
    def insert(self, tablename, values):
        sql = "insert into " + tablename + " values (" + values + ")"
        self.con.execute(sql)
        self.con.commit()

    # 在talename表中删除某条记录
    def delete(self,tablename,id):
        sql = "delete from "+tablename+" where id=" + str(id)
        self.con.execute(sql)
        self.con.commit()


class Util:
    def __init__(self):
        self.url = "http://127.0.0.1:8000/goods/"
        self.s = requests.session()

    # MD5加密
    def md5(self, mystr):
        if isinstance(mystr, str):
            m = hashlib.md5()
            m.update(mystr.encode('utf8'))
            return m.hexdigest()
        else:
            return ""

    # 初始化信息
    def inivalue(self, dataBase, ordertable, sign):
        # 获得初始化信息
        if sign == "0":
            values = GetXML.getUserInitInfo(self)
        # elif sign == "1":
        #     values = GetXML.getGoodInitInfo(self)
        # elif sign == "2":
        #     values = GetXML.getAddressInitInfo(self)
        # elif sign == "3":
        #     values = GetXML.getOrdersInitInfo(self)
        # elif sign == "4":
        #     values = GetXML.getOrderInitInfo(self)
        else:
            print("sign is error in function inivalue")
        # 建立记录
        if (sign != "0"):
            self.insertTable(dataBase, ordertable, values)
        # 处理在用户注册的时候，需要将密码MD5处理
        else:
            dom = minidom.parse("initInfo.xml")
            self.root = dom.documentElement
            password = self.root.getElementsByTagName('password')
            password = str(password[0].firstChild.data).strip()
            md5password = self.md5(password)
            newvalues = values.replace(password, md5password)
            self.insertTable(dataBase, ordertable, newvalues)
        return values

    # 插入数据
    # dataBase为数据库
    # table为数据库
    # values为值
    def insertTable(self, dataBase, table, values):
        # 获取插入数据的id
        id = values.split(',')[0].strip("\"")
        # 连接数据库
        dataBase.connect()
        # 查询数据库表中是否存在中
        if dataBase.searchByid(table, id):
            # 如果存在，删除这条记录
            dataBase.delete(table, "id=" + id)
        # 插入测试所需要的用户
        dataBase.insert(table, values)

    # 运行测试接口
    # mylist测试数据
    # values登录数据
    def run_test(self, mylist, values, sign):
        # 获取测试URL
        Login_url = self.url + "login_action/"  # login_Url为登录的URL
        run_url = self.url + mylist["Url"]  # run_url为运行测试用例所需的URL
        # 获取csrf_token
        data = self.s.get(Login_url)
        # csrf_token = data.cookies["csrftoken"]
        # 初始化登录变量
        # 获取登录数据
        username = values.split(',')[1].strip("\"")
        password = values.split(',')[2].strip("\"")
        # 判断当前测试是否需要登录
        if sign:
            # 使用当前用户登录系统
            # payload = {"username": username, "password": password, "csrfmiddlewaretoken": csrf_token}
            payload = {"username": username, "password": password}
            try:
                data = self.s.post(Login_url, data=payload)
            except Exception as e:
                print(e)
        # 运行测试接口
        try:
            # 为POST请求,由于post请求参数肯定是存在的，所以这里不判断有无参数
            if mylist["Method"] == "post":
                payload = eval(mylist["InptArg"])
                # 如果不是测试CSRF的
                # if mylist["Result"] != "403":
                #     payload["csrfmiddlewaretoken"] = csrf_token
                data = self.s.post(run_url, data=payload)
            # 为GET请求
            elif mylist["Method"] == "get":
                if mylist["InptArg"] == "":
                    data = self.s.get(run_url)
                else:
                    payload = eval(mylist["InptArg"])
                    data = self.s.get(run_url, params=payload)
        except Exception as e:
            print(e)
        else:
            return data

    def initChart(self):
        data = self.s.get(self.url + "/remove_chart_all/")

    def tearDownByCookie(self):
        data = self.s.get(self.url + "/remove_chart/0/")

    def tearDown(self, dataBase, table, values):
        # 获取初始化数据库中的记录主码
        id = values.split(',')[0]
        # 删除这条记录
        dataBase.delete(table, "id=" + id)
