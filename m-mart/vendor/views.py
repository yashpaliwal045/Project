from django.shortcuts import render
# for current directory forms
from . import forms
# it is for sucess or error alets
from django.contrib.messages import success,error
# for redirection
from django.shortcuts import HttpResponseRedirect
# it use database
from django.db.models import Q

from django.contrib.auth.forms import User
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.core.mail import send_mail
# to give page no.
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
# to get all  things from app
from vendor.models import *
from automobile import settings
from datetime import date


def home(request):
    cat = Category.objects.all()
    siz = Size.objects.all()
# this function is for serach when we clicked on that it give data there by using post fuction
    if (request.method == 'POST'):
        sr = request.POST.get('search')
        # its for search its filter for search data and send the data to front end,filter give us automatic so it help in search and it show data in which type you enter
        data = Product.objects.filter(Q(description__icontains=sr) | Q(name__icontains=sr)| Q(pid__contains=sr),size__sname=sr)
        # if it search and it found nothng so it show no foutnd
        datacount=data.count()
        noData = ""
        if(datacount == 0):
            noData="No Such product found"
            data=Product.objects.all()
            # if it found lots of product because of paginator it show only 8 data on one page and it give to another site
        paginator = Paginator(data, 8)
        page = request.GET.get('page')
        try:
            product_list = paginator.page(page)
        except PageNotAnInteger:
            product_list = paginator.page(1)
        except EmptyPage:
            product_list = paginator.page(paginator.num_pages)

        return render(request,'shop.html',{"Data":data,"Cat":cat,"Siz":siz,"posts":product_list,"No":noData})
# it is for slider , 6 for images we put 6 image in slie
# abc contain onlydata for slider
# data contain all data of product

    data = Product.objects.filter(size__sname="S")
    abc = [None] * 6
    count = 0
    for i in data:
        ids=i.pid+"_S"
        if ids in abc:
            ids=i.pid+"_S"
        else:
            abc[count] = i.pid + "_S"
            count = count + 1
            if (count > 5):
                break



    cat = Category.objects.all()
    return render(request, 'index.html', {"Data":data,"Cat":cat,"Abc":abc})



def addProduct(request):
    if(request.method=='POST'):
        # files if we have old file we get this if notso simply send normal data
        data = forms.ProductForm(request.POST, request.FILES)
        if(data.is_valid()):
            data.save()
            success(request,"Product Added")
            return HttpResponseRedirect('/addproduct/')
        else:
            error(request,'Invalid Product Detail')
            return HttpResponseRedirect('/addproduct/')
    else:
        return render(request,'addproduct.html', {'Form' : forms.ProductForm})

def addCategory(request):
    if(request.method=='POST'):
        data = forms.ProductForm(request.POST, request.FILES)
        if(data.is_valid()):
            data.save()
            success(request,"Product Added")
            return HttpResponseRedirect('/addproduct/')
        else:
            error(request,'Invalid Product Detail')
            return HttpResponseRedirect('/addproduct/')
    else:
        return render(request,'addproduct.html', {'Form' : forms.ProductForm})



# after registration it send mail to user
def email_send(request,email,name):
    subject = 'Thanks '+name+' for registering to our site'
    message = ' it  means a lot to us '
    # it get email from setting forsending mails
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email,]
    # it is predefinned fuction
    send_mail( subject, message, email_from, recipient_list )

def dispatch_email(request,data):

    subject = 'Order Dispached'
    message = 'Dear '+data.order_address.chname+',\n       Your Product is being dispatched for our side and will reached soon.\nAt address: \n'+data.order_address.address+"\n"+data.order_address.pin
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [data.order_address.email,]
    send_mail( subject, message, email_from, recipient_list )


def Cancel_email(request,data):

    subject = 'Order Dispached'
    message = 'Dear '+data.order_address.chname+",\n       Your Request of Product Cancelation is registered "
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [data.order_address.email,]
    send_mail( subject, message, email_from, recipient_list )

def register(request):
    if(request.method=='POST'):
        lname=request.POST.get('usernam')
        lpward=request.POST.get('passwrd')
        user=auth.authenticate(username=lname,password=lpward)
        if(user is not None):
            auth.login(request,user)
            if(user.is_superuser):
                return HttpResponseRedirect('/')
            else:
                return HttpResponseRedirect('/')
        else:
            error(request,"Invalid User")
    return render(request,'Login.html')

def SignUp(request):
    if(request.method=='POST'):
        unam=request.POST.get('uname')
        try:
            match = User.objects.get(username=str(unam))
            if (match):
                error(request, "Username Already Exist")

        except:
            fnam = request.POST.get('first_name')
            lnam = request.POST.get('last_name')
            mail = request.POST.get('email')
            pward = request.POST.get('pward')
            cpward = request.POST.get('cpward')
            if (pward == cpward):
                User.objects.create_user(username=str(unam),
                                         first_name=str(fnam),
                                         last_name=str(lnam),
                                         email=mail,
                                         password=pward
                                         )
                success(request, "Account is created")
                try:
                    email_send(request, mail, unam)
                except:
                    error(request, " ")
                return HttpResponseRedirect('/register/')
            else:
                error(request, "Password and Confirm Password not Matched")
    return render(request, "signup.html")

# it is for category when a user see through caterory
def Shop(request,cn):

    cat = Category.objects.all()
    siz = Size.objects.all()
    noData = ""
    if (request.method == 'POST'):
        sr = request.POST.get('search')
        data = Product.objects.filter(Q(description__icontains=sr) | Q(name__icontains=sr)| Q(pid__contains=sr),size__sname=sr)
        datacount = data.count()
        noData = ""
        if (datacount == 0):
            noData = "No Such product found"
            data = Product.objects.all()
        paginator = Paginator(data, 8)
        page = request.GET.get('page')
        try:
            product_list = paginator.page(page)
        except PageNotAnInteger:
            product_list = paginator.page(1)
        except EmptyPage:
            product_list = paginator.page(paginator.num_pages)

        return render(request,'shop.html',{"Data":data,"Cat":cat,"Siz":siz,"posts":product_list,"No":noData})

    if (cn == "sample"):
        data = Product.objects.filter(size__sname="S")
    else:
        data = Product.objects.filter(cat__cname=cn)
# len is for if  product n category is null so it show msg
    if(len(data)==0):
        noData="Product In This Category Is Not Available"
        data = Product.objects.filter(size__sname="S")



   # post = Product.objects.all()

    paginator = Paginator(data, 8)
    page = request.GET.get('page')
    try:
        product_list = paginator.page(page)
    except PageNotAnInteger:
        product_list = paginator.page(1)
    except EmptyPage:
        product_list = paginator.page(paginator.num_pages)
    return render(request,"shop.html",{"Cat":cat,"Data":data,"Siz":siz,
                                       "No":noData,"posts":product_list,})
# it is for size when a user see through size
def Shop2(request,si):
    cat = Category.objects.all()
    siz = Size.objects.all()
    if (request.method == 'POST'):
        sr = request.POST.get('search')
        data = Product.objects.filter(Q(description__icontains=sr) | Q(name__icontains=sr) | Q(pid__contains=sr),
                                      size__sname=sr)
        datacount = data.count()
        noData = ""
        if (datacount == 0):
            noData = "No Such product found"
            data = Product.objects.all()
        paginator = Paginator(data, 8)
        page = request.GET.get('page')
        try:
            product_list = paginator.page(page)
        except PageNotAnInteger:
            product_list = paginator.page(1)
        except EmptyPage:
            product_list = paginator.page(paginator.num_pages)

        return render(request, 'shop.html', {"Data": data, "Cat": cat, "Siz": siz, "posts": product_list,"No":noData})

    noData = ""
    if (si == "sample"):
        data = Product.objects.filter(size__sname="S")
    else:
        data = Product.objects.filter(size__sname=si)
    if (len(data)==0):
        noData ="Product In This Size Is Not Available"
        data = Product.objects.all()
    paginator = Paginator(data, 8)
    page = request.GET.get('page')
    try:
        product_list = paginator.page(page)
    except PageNotAnInteger:
        product_list = paginator.page(1)
    except EmptyPage:
        product_list = paginator.page(paginator.num_pages)
    return render(request,"shop.html",{"Cat":cat,"Data":data,"Siz":siz,"No":noData,"posts":product_list})

#only show product
@login_required(login_url='/register/')
def ProductDetails(request,num):
    data = Product.objects.get(id=num)
    dat = Product.objects.filter(pid=data.pid)
    car = Cart.objects.all();
    avail = ""
    sicount = dat.count()
    if (sicount == 0):
        avail = "Out Of Stock"
    else:
        avail = "In Stock"

    if (request.method == 'POST'):
        form = forms.CartForm(request.POST)
        q = request.POST['count']
        z=0
        if (request.user == None):
            HttpResponseRedirect('/register/')
        if (form.is_valid()):
# loop for if we add same thing twice it increase our quantity
            for x in car:

                if (data.id == x.cart_product.id):
                    x.count = x.count + 1
                    z = 1
                    x.save()
                    return HttpResponseRedirect('/cart/')
            if (z == 0):
                f = form.save(commit=False)
                f.cart_user = request.user
                f.cart_product = data
                f.count = 1
                f.total = int(data.price) * float(q)
                f.save()
                return HttpResponseRedirect('/cart/')
    else:
        form = forms.CartForm()
    car = Cart.objects.all();
    siz = Size.objects.all();

    return render(request, 'productdetails.html', {"Data": data,"Siz":siz,"Form":form,"Dat":dat,"Avail":avail,"Count":sicount})

# for particular sizze
@login_required(login_url='/register/')
def ProductDetails2(request,num,s):
    dat = Product.objects.filter(pid=num)
    avail = ""
    sicount = dat.count()
    if (sicount == 1):
        avail = "Out Of Stock"
    else:
        avail = "In Stock"
    data = Product.objects.get(id=num)
    num=str(num)+"-"+str(s)
    dat = Product.objects.filter(pid=s)
    car = Cart.objects.all();
    siz = Size.objects.filter(sname=s)
    if (request.method == 'POST'):
        form = forms.CartForm(request.POST)
        q = request.POST['count']
        z=0
        if(request.user == None):

            HttpResponseRedirect('/register/')
        if (form.is_valid()):
            for x in car:

                if (data.id == x.cart_product.id):
                    x.count = x.count + 1
                    z = 1
                    x.save()
                    return HttpResponseRedirect('/cart/')
            if (z == 0):

                f = form.save(commit=False)
                f.cart_user = request.user
                f.cart_product = data
                f.count = q
                f.total = int(data.price) * float(q)
                f.save()
                return HttpResponseRedirect('/cart/')
    else:
        form = forms.CartForm()
    return render(request, 'productdetails.html', {"Data": data, "Siz": siz,"Dat":dat, "Form": form,"Avail":avail})
def logOut(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def addProduct(request):
    cat = Category.objects.all()
    siz = Size.objects.all()
    if (request.method == 'POST'):
        try:

            data = Product()
            s = request.POST.get('size')
            st = Size.objects.get(sname=s)
            data.size = st
            data.pid = request.POST.get('id')

            data.id = request.POST.get('id')+"_"+str(st)
            cn = request.POST.get('cat')
            ct = Category.objects.get(cname=cn)
            data.cat = ct



            data.name = request.POST.get('name')
            data.description = request.POST.get('description')
            data.basicPrice = request.POST.get('basicPrice')
            data.discount = request.POST.get('discount')
            data.brand = request.POST.get('brand')

            bp = int(data.basicPrice)
            d = int(data.discount)

            data.price = int(bp - (bp * d / 100))
            data.img1 = request.FILES.get('img1')
            data.img2 = request.FILES.get('img2')

            data.save()
            success(request, 'Product Inserted')
            return HttpResponseRedirect('/addproduct/')
        except:
            error(request, "Invalid Record")
    return render(request, "addproduct.html", {"Cat": cat,"Siz": siz})

def AdminPage(request):
    cat = Category.objects.all()
    siz = Size.objects.all()
    if (request.method == 'POST'):
        sr = request.POST.get('search')
        data = Product.objects.filter(Q(description__icontains=sr) | Q(name__icontains=sr) | Q(pid__contains=sr),
                                      size__sname=sr)
        datacount = data.count()
        noData = ""
        if (datacount == 0):
            noData = "No Such product found"
            data = Product.objects.all()
        paginator = Paginator(data, 8)
        page = request.GET.get('page')
        try:
            product_list = paginator.page(page)
        except PageNotAnInteger:
            product_list = paginator.page(1)
        except EmptyPage:
            product_list = paginator.page(paginator.num_pages)

        return render(request, 'shop.html', {"Data": data, "Cat": cat, "Siz": siz, "posts": product_list,"No":noData})

    data=Product.objects.filter(size__sname="S")
    return render(request,"admins.html",{"Data":data})
# it show size availiblity for particular product by pid
def Sizeavi(request,num):
    dat = Product.objects.filter(pid=num)
    print(dat)
    return render(request,"sizeavi.html",{"Data":dat})

def addCategory(request):
    if (request.method == 'POST'):
        try:

            data = Category()
            data.cname= request.POST.get('name')
            data.save()
            success(request, 'Product Inserted')
            return HttpResponseRedirect('/addcategory/')
        except:
            error(request, "Invalid Record")
    return render(request, "addcategory.html")

# for particular product it is basically for size
def SizeAdd(request,num):
    data = Product.objects.get(id=num)
    siz = Size.objects.all()
    cat = Category.objects.all()

    if (request.method == 'POST'):
        try:

            s = request.POST.get('size')
            st = Size.objects.get(sname=s)
            data.size = st

            data.id=str(request.POST.get('id'))+"_"+str(st)
            data.name = request.POST.get('name')
            data.description = request.POST.get('description')
            data.basicPrice = request.POST.get('basicPrice')
            data.discount = request.POST.get('discount')

            bp = int(data.basicPrice)
            d = int(data.discount)

            data.price = bp - bp * d / 100
            data.color = request.POST.get('color')
            data.save()
            success(request, 'Size Is Added')
            data = Product.objects.get(id=num)
        except:
            error(request, "Invalid Record")
    return render(request, "sizeadd.html", {"Data": data,"Siz":siz})

def editProduct(request,num):
    data=Product.objects.get(id=num)
    cat=Category.objects.all()
    if (request.method == 'POST'):
        try:

            data.name = request.POST.get('name')
            data.description = request.POST.get('description')
            data.basicPrice = request.POST.get('basicPrice')
            data.discount = request.POST.get('discount')
            bp = int(data.basicPrice)
            d = int(data.discount)

            data.price = bp - bp * d / 100
            data.save()
            success(request, 'Product Edited')
            data = Product.objects.get(id=num)
        except:
            error(request, "Invalid Record")
    return render(request,"edit.html",{"Data":data})

def DeleteProduct(request,num):
    data=Product.objects.filter(id=num)
    # search and delete
    for i in data:
        i.delete()
    return HttpResponseRedirect("/adminpage/")
def DeleteAddress(request,num):
    adata=Checkout.objects.get(checkid=num)
    adata.delete()
    adata = Checkout.objects.filter(checkout_user=request.user)
    # it is for if in address page their is no data it give to the other  page
    if (len(adata) == 0):
        return HttpResponseRedirect('/addaddress/')
    return render(request, "selectaddress.html", {"Data": adata})


@login_required(login_url='/register/')
def CartDetails(request):
    cat = Category.objects.all()
    siz = Size.objects.all()
    if (request.method == 'POST'):
        sr = request.POST.get('search')
        data = Product.objects.filter(Q(description__icontains=sr) | Q(name__icontains=sr) | Q(pid__contains=sr),
                                      size__sname=sr)
        datacount = data.count()
        noData = ""
        if (datacount == 0):
            noData = "No Such product found"
            data = Product.objects.filter(size__sname=sr)
        paginator = Paginator(data, 8)
        page = request.GET.get('page')
        try:
            product_list = paginator.page(page)
        except PageNotAnInteger:
            product_list = paginator.page(1)
        except EmptyPage:
            product_list = paginator.page(paginator.num_pages)

        return render(request, 'shop.html', {"Data": data, "Cat": cat, "Siz": siz, "posts": product_list})

    data=Cart.objects.filter(cart_user=request.user)
    coun=data.count();
    t=0
    # total amount of cart
    for i in data:
        t=t+i.cart_product.price*i.count
    return render(request,"cart.html",{"Data":data,"Total":t,"length":coun})
# it is for when we placed order but not dispatched
@login_required(login_url='/register/')
def PastOrders(request):
    cat = Category.objects.all()
    siz = Size.objects.all()
    if (request.method == 'POST'):
        sr = request.POST.get('search')
        data = Product.objects.filter(Q(description__icontains=sr) | Q(name__icontains=sr) | Q(pid__contains=sr),
                                      size__sname=sr)
        datacount = data.count()
        noData = ""
        if (datacount == 0):
            noData = "No Such product found"
            data = Product.objects.all()
            paginator = Paginator(data, 8)
        page = request.GET.get('page')
        try:
            product_list = paginator.page(page)
        except PageNotAnInteger:
            product_list = paginator.page(1)
        except EmptyPage:
            product_list = paginator.page(paginator.num_pages)

        return render(request, 'shop.html', {"Data": data, "Cat": cat, "Siz": siz, "posts": product_list,"No":noData})

    data=Order.objects.filter(order_user=request.user)
    cdata=CancelOrder.objects.filter(order_user=request.user)
    datacount = cdata.count()
    return render(request,"placedorder.html",{"Data":data,"CData":cdata,"datacount":datacount})
# it is for when we placed order dispatched
@login_required(login_url='/register/')
def PastOrders2(request):
    cat = Category.objects.all()
    siz = Size.objects.all()
    if (request.method == 'POST'):
        sr = request.POST.get('search')
        data = Product.objects.filter(Q(description__icontains=sr) | Q(name__icontains=sr) | Q(pid__contains=sr),
                                      size__sname=sr)
        datacount = data.count()
        noData = ""
        if (datacount == 0):
            noData = "No Such product found"
            data = Product.objects.all()
        paginator = Paginator(data, 8)
        page = request.GET.get('page')
        try:
            product_list = paginator.page(page)
        except PageNotAnInteger:
            product_list = paginator.page(1)
        except EmptyPage:
            product_list = paginator.page(paginator.num_pages)

        return render(request, 'shop.html', {"Data": data, "Cat": cat, "Siz": siz, "posts": product_list,"No":noData})
    rdata = ReturnOrder.objects.filter(order_user=request.user)
    length = rdata.count()
    data=PreviousOrder.objects.filter(order_user=request.user)
    return render(request,"pastorders.html",{"Data":data,"RData":rdata,"length":length})

def CartDelete(request,num):
    data=Cart.objects.get(cart_product__id=num)
    data.delete()
    return HttpResponseRedirect('/cart/')
# it is for decrement
def CartEdit1(request,num):
    data=Cart.objects.get(cart_product__id=num)
    data.count= int(data.count)-1
    if(int(data.count)==0):
        data.count=1
    data.save()
    return HttpResponseRedirect("/cart/")
# admin side function
def OrderPlaced(request,num):
    cat = Category.objects.all()
    siz = Size.objects.all()
    if (request.method == 'POST'):
        sr = request.POST.get('search')
        data = Product.objects.filter(Q(description__icontains=sr) | Q(name__icontains=sr) | Q(pid__contains=sr),
                                     size__sname=sr)
        orderdate=date.today()
        datacount = data.count()
        noData = ""
        if (datacount == 0):
            noData = "No Such product found"
            data = Product.objects.all()
        paginator = Paginator(data, 8)
        page = request.GET.get('page')
        try:
            product_list = paginator.page(page)
        except PageNotAnInteger:
            product_list = paginator.page(1)
        except EmptyPage:
            product_list = paginator.page(paginator.num_pages)

        return render(request, 'shop.html', {"Data": data, "Cat": cat, "Siz": siz, "posts": product_list,"No":noData,"date":orderdate})

    data = Cart.objects.filter(cart_user=request.user)
    adata = Checkout.objects.filter(checkid=num)
    orderdate = date.today()
    t=0
    for i in data:
        i.total=i.cart_product.price * i.count
    for i in data:
        t = t + i.cart_product.price * i.count
    return render(request,"orderplace.html",{"Data": data, "Adata": adata, "total": t, "date": orderdate})
    # these all function is for delete the cart
def homedelete(request):
    data = Cart.objects.filter(cart_user=request.user)
    data.delete()
    return HttpResponseRedirect('/')
def deletecart(request):
    data = Cart.objects.filter(cart_user=request.user)
    data.delete()
    return HttpResponseRedirect('/cart/')
def deleteabout(request):
    data = Cart.objects.filter(cart_user=request.user)
    data.delete()
    return HttpResponseRedirect('/about/')
def deleteshop(request):
    data = Cart.objects.filter(cart_user=request.user)
    data.delete()
    return HttpResponseRedirect('/shop/sample/')

def deletePreviousorders(request):
    data = Cart.objects.filter(cart_user=request.user)
    data.delete()
    return HttpResponseRedirect('/Previousorders/')

def deletepastorder(request):
    data = Cart.objects.filter(cart_user=request.user)
    data.delete()
    return HttpResponseRedirect('/pastorder/')
def deletelogout(request):
    data = Cart.objects.filter(cart_user=request.user)
    data.delete()
    return HttpResponseRedirect('/logout/')
def deleteadminpage(request):
    data = Cart.objects.filter(cart_user=request.user)
    data.delete()
    return HttpResponseRedirect('/adminpage/')

# admin side
def OrderPlaced2(request):
    data=PreviousOrder.objects.filter(order_user=request.user)
    return render(request,"orderplace.html",{"Data":data})
# it is for incretment
def CartEdit(request,num):
    data=Cart.objects.get(cart_product__id=num)
    data.count= int(data.count)+1
    data.save()
    return HttpResponseRedirect("/cart/")
# when adress is for fresh id
@login_required(login_url='/register/')
def AddAddress(request):
    i=None
    x=""
    if (request.method == 'POST'):
         try:
            check = Checkout()
            check.checkid= request.user
            x=request.user
            check.chname = request.POST.get('name')
            check.checkout_user = request.user
            check.mobile = request.POST.get('mobile')
            check.email = request.POST.get('email')
            check.state = request.POST.get('state')
            check.city = request.POST.get('city')
            x=request.POST.get('pin')
            check.address = request.POST.get('address')
            check.pin = request.POST.get('pin')
            check.save()
            y = "/checkout/" + str(x) + "/"
            return HttpResponseRedirect(y)
         except:
            error(request, "Invalid Record")
    return render(request, "addaddress.html")
# for add multiple adress
@login_required(login_url='/register/')
def AddAddress2(request):
    i=None
    nam=None
    x=""
    data = Checkout.objects.filter(checkout_user=request.user)
    for i in data:
        nam=i.checkid
    x=int(len(nam))
    if (request.method == 'POST'):
        try:
            check = Checkout()
            names=str(request.user)
            y = x-int(len(names))
            y=y+1
            subname=names[:y]
            check.checkid= names+str(subname)
            x= check.checkid
            check.chname = request.POST.get('name')
            check.checkout_user = request.user
            check.mobile = request.POST.get('mobile')
            check.email = request.POST.get('email')
            check.state = request.POST.get('state')
            check.city = request.POST.get('city')
            check.address = request.POST.get('address')
            check.pin = request.POST.get('pin')
            check.save()
            success(request, "Address is added")
            y="/checkout/"+x+"/"
            return HttpResponseRedirect(y)
        except:
            error(request, "Invalid Record")
    return render(request, "addaddress.html")
@login_required(login_url='/register/')
def SelectAddress(request):
    adata=Checkout.objects.filter(checkout_user=request.user)
    if(len(adata)==0):
        return HttpResponseRedirect('/addaddress/')
    return render(request,"selectaddress.html",{"Data":adata})

MERCHANT_KEY='sample'
@login_required(login_url='/register/')

def CheckoutForm(request,num):
    data = Cart.objects.filter(cart_user=request.user)
    temp=0
    t = 0
    orderr=0
    for i in data:
        t = t + i.cart_product.price * i.count

    adata=Checkout.objects.filter(checkid=num)
    orde=Order.objects.all()
    if(orde != None):
        for z in orde:
            orderr= int(z.ordernumber)
    O = Order()
    print(request.user)
    if(request.method=='POST'):
        try:
            choice = request.POST.get('choice')
            if(choice=='COD'):
                for i in data:
                    O = Order()
                    O.ordernumber = orderr+1
                    orderr=orderr+1
                    O.order_user = request.user
                    d = Product.objects.get(id=i.cart_product.id)
                    O.order_product = d
                    for x in adata:
                        O.order_address = x
                    O.count = i.count
                    O.save()
                x='/orderplaced/'+num+"/"
                return HttpResponseRedirect(x)
            # elif\
            #         (choice=='Paypal'):
            #     success(request, "pay with paypal")
            #     return HttpResponseRedirect('/payment/process/')
        except:
            error(request, "Invalid Record")

    return render(request,"checkout.html",{"Total":t,"Data":adata})

def About(request):
    return render(request,'about.html')

def OrderAdmin(request):
    count=len(PreviousOrder.objects.all())
    data=Order.objects.all()
    return render(request,'orderadmin.html',{"Data":data})

def CancelOrderAdmin(request):
    data=CancelOrder.objects.all()
    return render(request,'canceladmin.html',{"Data":data})

# it is for admin side
def DispatchedOrder(request,num):
    data = Order.objects.get(ordernumber=num)
    try:

        p = PreviousOrder()
        p.ordernumber = data.ordernumber
        p.order_user = data.order_user
        p.order_product = data.order_product
        p.count=data.count
        p.order_address = data.order_address
        p.save()
        try:
            dispatch_email(request,data)
        except:
            error(request, " ")
        data.delete()
    except:
        error(request, "Invalid Record")
    data=Order.objects.all()
    return render(request,'orderadmin.html',{"Data":data})

def Cancelorder(request,num):

    data = Order.objects.get(ordernumber=num)
    try:
        p = CancelOrder()
        p.ordernumber = data.ordernumber
        p.order_user = data.order_user
        p.order_product = data.order_product
        p.count=data.count
        p.order_address = data.order_address
        p.save()
        try:
            Cancel_email(request,data)
        except:
            error(request," ")
        data.delete()
    except:
        error(request, "Invalid Record")
    data=Order.objects.filter(order_user=request.user)
    return render(request,'placedorder.html',{"Data":data})

def Returnorder(request,num):

    data = PreviousOrder.objects.get(ordernumber=num)
    try:
        p = ReturnOrder()
        p.ordernumber = data.ordernumber
        p.order_user = data.order_user
        p.order_product = data.order_product
        p.count=data.count
        p.order_address = data.order_address
        p.save()
        try:
            Return_email(request, data)
        except:
            error(request," ")

    except:
        error(request, "Invalid Record")
    data.delete()
    data=PreviousOrder.objects.filter(order_user=request.user)
    return HttpResponseRedirect("/Previousorders/")

def Return_email(request,data):

    subject = 'Return Request'
    message = 'Dear '+data.order_address.chname+",\n       Your Request of Product Return is registered "
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [data.order_address.email,]
    send_mail( subject, message, email_from, recipient_list )

def ReturnOrderAdmin(request):
    data=ReturnOrder.objects.all()
    return render(request,'returnorder.html',{"Data":data})

def CancelReturn(request,num):

    try:
        subject = 'Return Request'
        message = 'Dear ' + data.order_address.chname + ",\n       Your Request of Product Return is Decline "
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [data.order_address.email, ]
        send_mail(subject, message, email_from, recipient_list)
    except:
        error(request, " ")
    data=ReturnOrder.objects.get(ordernumber=num)
    try:

        p = PreviousOrder()
        p.ordernumber = data.ordernumber
        p.order_user = data.order_user
        p.order_product = data.order_product
        p.count = data.count
        p.order_address = data.order_address
        p.save()
        data.delete()
    except:
        error(request, "Invalid Record")
    adata = ReturnOrder.objects.all()
    return render(request, 'returnorder.html', {"Data": adata})

def ConfirmReturn(request,num):
    data=ReturnOrder.objects.get(ordernumber=num)
    try:
        subject = 'Return Request'
        message = 'Dear ' + data.order_address.chname + ",\n       Your Request of Product Return is confirmed and your order will be picked soon by our executive from your delivered address "
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [data.order_address.email, ]
        send_mail(subject, message, email_from, recipient_list)
    except:
        error(request," ")

    try:

        data.delete()
    except:
        error(request, "Invalid Record")
    adata = ReturnOrder.objects.all()
    return render(request, 'returnorder.html', {"Data": adata})
def Deletecancel(request,num):
    data=CancelOrder.objects.get(ordernumber=num)
    try:
        subject = 'Return Request'
        message = 'Dear ' + data.order_address.chname + ",\n       Your Request of Product Cancelation is confirmed and if you have paid for this order than the money will we returned as soon as possible "
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [data.order_address.email, ]
        send_mail(subject, message, email_from, recipient_list)
    except:
        error(request," ")
    try:
        data.delete()
    except:
        error(request,"Data is not deleted ")
    data = CancelOrder.objects.all()
    return render(request,'canceladmin.html',{"Data":data})
