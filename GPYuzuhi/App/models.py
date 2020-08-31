from django.db import models

from App.views_constant import ORDER_STATUS_NOT_PAY


class Main(models.Model):
    img = models.CharField(max_length=255)
    name = models.CharField(max_length=64)
    trackid = models.IntegerField(default=1)

    class Meta:
        abstract = True


# Create your models here.


class MainWheel(Main):
    """
    yuzuhi_wheel(img,name,trackid)
    """

    class Meta:
        db_table = 'yuzuhi_wheel'


class MainNav(Main):
    """
    yuzuhi_nav(img,name,trackid)
    """

    class Meta:
        db_table = 'yuzuhi_nav'


class MainMustBuy(Main):
    """
    yuzuhi_mustbuy(img.name.trackid
    """

    class Meta:
        db_table = 'yuzuhi_mustbuy'


class MainShop(Main):
    """
    yuzuhi_shop(img,name,trackid)
    """

    class Meta:
        db_table = 'yuzuhi_shop'


class MainShow(models.Model):
    """
    yuzuhi_mainshow(trackid,name,img,categoryid,brandname,img1,childcid1,productid1,
    longname1,price1,marketprice1,img2,childcid2,productid2,longname2,price2,
    marketprice2,img3,childcid3,productid3,longname3,price3,marketprice3)
    """

    img = models.CharField(max_length=255,default='darksoulsimg/main_show.jpg')
    productimg1 = models.CharField(max_length=255)
    productlongname1 = models.CharField(max_length=512,null=True)
    price1 = models.FloatField(default=1)
    marketprice1 = models.FloatField(default=0)
    productimg2 = models.CharField(max_length=255)
    productlongname2 = models.CharField(max_length=512,null=True)
    price2 = models.FloatField(default=1)
    marketprice2 = models.FloatField(default=0)
    productimg3 = models.CharField(max_length=255)
    productlongname3 = models.CharField(max_length=512,null=True)
    price3 = models.FloatField(default=1)
    marketprice3 = models.FloatField(default=0)

    class Meta:
        db_table = 'yuzuhi_mainshow'


class FoodType(models.Model):
    """
    yuzuhi_foodtypes(typeid,typename,childtypenames,typesort)
    """

    typeid = models.IntegerField(default=1)
    typename = models.CharField(max_length=32)
    childtypenames = models.CharField(max_length=512)
    typesort = models.IntegerField(default=1)

    class Meta:
        db_table = "yuzuhi_foodtype"


class Goods(models.Model):
    """
    yuzuhi_goods(productid,productimg,description,productlongname,isxf,pmdesc,
    specifics,price,marketprice,categoryid,childcid,childcidname,dealerid,
    storenums,productnum)
    """
    productid = models.IntegerField(default=1)
    productimg = models.CharField(max_length=255)
    productname = models.CharField(max_length=128,null=True)
    productlongname = models.CharField(max_length=2048,null=True)
    specifics = models.CharField(max_length=64)
    price = models.FloatField(default=0)
    marketprice = models.FloatField(default=1)
    categoryid = models.IntegerField(default=1)
    childcid = models.IntegerField(default=1)
    childcidname = models.CharField(max_length=128)
    productnum = models.IntegerField(default=1)
    location = models.CharField(max_length=2048,null=True)

    class Meta:
        db_table = "dark_souls_goods"


class YuzuhiUser(models.Model):
    u_username = models.CharField(max_length=32, unique=True)
    u_password = models.CharField(max_length=256)
    u_email = models.CharField(max_length=64, unique=True)
    u_icon = models.ImageField(upload_to="icons/%Y/%m/%d/")
    is_active = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)

    class Meta:
        db_table = 'yuzuhi_user'


class Cart(models.Model):
    c_user = models.ForeignKey(YuzuhiUser)
    c_goods = models.ForeignKey(Goods)
    c_goods_num = models.IntegerField(default=1)
    c_is_select = models.BooleanField(default=True)

    class Meta:
        db_table = 'yuzuhi_cart'


class Order(models.Model):
    o_user = models.ForeignKey(YuzuhiUser)
    o_price = models.FloatField(default=0)
    o_time = models.DateTimeField(auto_now=True)
    o_status = models.IntegerField(default=ORDER_STATUS_NOT_PAY)

    class Meta:
        db_table = 'yuzuhi_order'


class OrderGoods(models.Model):
    o_order = models.ForeignKey(Order)
    o_goods = models.ForeignKey(Goods)
    o_goods_num = models.IntegerField(default=1)

    class Meta:
        db_table = 'yuzuhi_ordergoods'
