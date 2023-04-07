from django.db import models
from django.contrib.auth.forms import User
from django.contrib.auth.models import User
# Create your models here.





class Category(models.Model):
    cid = models.AutoField
    cname = models.CharField(max_length=30)
    def __str__(self):
        return self.cname

class Size(models.Model):
    sid = models.AutoField
    sname = models.CharField(max_length=5)
    def __str__(self):
        return self.sname

class Product(models.Model):
    id = models.CharField(max_length=30,primary_key=True)
    pid = models.CharField(max_length=30)
    brand = models.CharField(max_length=30,default=None)
    cat = models.ForeignKey(Category,on_delete=models.CASCADE,default=None)
    name = models.CharField(max_length=100)
    description = models.TextField()
    basicPrice = models.IntegerField()
    discount = models.IntegerField()
    price = models.IntegerField()
    size = models.ForeignKey(Size,on_delete=models.CASCADE,default=None)

    img1 = models.ImageField(upload_to='images')
    img2 = models.ImageField(upload_to='images',default=None)
    date = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id

class Cart(models.Model):
    cartid=models.AutoField
    cart_user=models.ForeignKey(User,on_delete=models.CASCADE,default=None)
    cart_product=models.ForeignKey(Product,on_delete=models.CASCADE,default=None)
    count=models.IntegerField(default=1)
    total=models.IntegerField()
    date=models.DateTimeField(auto_now_add=True)
    update=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_product.id

class Checkout(models.Model):
    checkid=models.CharField(max_length=30,primary_key=True,default=None)
    checkout_user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    chname=models.CharField(max_length=30)
    mobile=models.IntegerField()
    email=models.EmailField(max_length=50)
    state=models.CharField(max_length=30)
    city=models.CharField(max_length=30)
    address=models.CharField(max_length=50)
    pin=models.CharField(max_length=10)

    def __str__(self):
        return self.checkid

class Order(models.Model):
    orderid =  models.AutoField
    ordernumber = models.IntegerField()
    order_user=models.ForeignKey(User,on_delete=models.CASCADE,default=None)
    order_product=models.ForeignKey(Product,on_delete=models.CASCADE,default=None)
    count=models.IntegerField(default=1)
    order_address=models.ForeignKey(Checkout,on_delete=models.CASCADE,default=None)
    def __str__(self):
        return self.order_address.chname

class PreviousOrder(models.Model):
    orderid =  models.AutoField
    ordernumber = models.IntegerField()
    order_user=models.ForeignKey(User,on_delete=models.CASCADE,default=None)
    order_product=models.ForeignKey(Product,on_delete=models.CASCADE,default=None)
    count=models.IntegerField(default=1)
    order_address=models.ForeignKey(Checkout,on_delete=models.CASCADE,default=None)
    def __str__(self):
        return self.order_address.chname

class CancelOrder(models.Model):
    orderid =  models.AutoField
    ordernumber = models.IntegerField()
    order_user=models.ForeignKey(User,on_delete=models.CASCADE,default=None)
    order_product=models.ForeignKey(Product,on_delete=models.CASCADE,default=None)
    count=models.IntegerField(default=1)
    order_address=models.ForeignKey(Checkout,on_delete=models.CASCADE,default=None)

    def __str__(self):
        return self.order_address.chname

class ReturnOrder(models.Model):
    orderid =  models.AutoField
    ordernumber = models.IntegerField()
    order_user=models.ForeignKey(User,on_delete=models.CASCADE,default=None)
    order_product=models.ForeignKey(Product,on_delete=models.CASCADE,default=None)
    count=models.IntegerField(default=1)
    order_address=models.ForeignKey(Checkout,on_delete=models.CASCADE,default=None)

    def __str__(self):
        return self.order_address.chname
