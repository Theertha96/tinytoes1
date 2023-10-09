import queue
from django.contrib import messages
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.cache import never_cache
from adminapp.forms import *

from adminapp.models import *
from accounts.models import CustomUser
from adminapp.models import Banner
from cart.models import Cartitem
from cart.models import *
from django.urls import reverse
from django.db.models import Q



from cart.models import Orders
from django.db.models import Count
import calendar
from django.db.models.functions import ExtractMonth,ExtractYear
# Create your views here.

@login_required(login_url="admin_login")
def admin_home(request):
    return render(request,"admin-temp/index.html")

def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_home')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request,email=email,password=password)
        if user.is_superuser:
           login(request,user)
           return redirect('admin_home')
        else:
            messages.error(request,"User name or password is incorect")
            return redirect('admin_login')

    return render(request,"admin-temp/admin_login.html")

@login_required(login_url='admin_login')
def admin_home(request):
    delivered_orders = Orders.objects.filter(status='Delivered')
    print(delivered_orders)
    delivered_orders_by_months = delivered_orders.annotate(delivered_month=ExtractMonth('created_at')).values('delivered_month').annotate(delivered_count=Count('id')).values('delivered_month', 'delivered_count')
    print( delivered_orders_by_months)
    delivered_orders_month = []
    delivered_orders_number = []
    for d in delivered_orders_by_months:
         delivered_orders_month.append(calendar.month_name[d['delivered_month']])
         delivered_orders_number.append(list(d.values())[1])

    cancelled_orders = Orders.objects.filter(status='cancelled')
    cancelled_orders_number=len(cancelled_orders)

    new_orders = Orders.objects.filter(status='New')
    new_orders_number=len(new_orders)


    
    

    order_by_months = Orders.objects.annotate(month=ExtractMonth('created_at')).values('month').annotate(count=Count('id')).values('month', 'count')
    monthNumber = []
    totalOrders = []
   

    for o in order_by_months:
        monthNumber.append(calendar.month_name[o['month']])
        totalOrders.append(list(o.values())[1])
        
    order_by_year = Orders.objects.annotate(year=ExtractYear('created_at')).values('year').annotate(count=Count('id')).values('year', 'count')
    total_amount=Payment.objects.aggregate(total_amount=models.Sum('amount'))
    amount = float(total_amount['total_amount'])
    print(amount)
    yearNumber = []
    total_Orders = []

    for o in order_by_year:
        yearNumber.append(o['year'])
        total_Orders.append(o['count'])    

    context = {
        'monthNumber': monthNumber,
        'totalOrders': totalOrders,
        'yearNumber': yearNumber,
        'total_Orders': total_Orders,
        'delivered_orders':delivered_orders,
        'order_by_months':order_by_months,
        'cancelled_orders':cancelled_orders_number,
        'new_orders':new_orders_number,
        'total_amount':amount,
        
        'totalOrders':totalOrders,
        'delivered_orders_number':delivered_orders_number,
        'delivered_orders_month':delivered_orders_month,
        'delivered_orders_by_months':delivered_orders_by_months,

    }
    return render(request, "admin-temp/index.html",context)

@never_cache
def admin_logout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('admin_login')

@never_cache
@login_required(login_url='admin_login')
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        # print('hi')
        if form.is_valid():
            # print("hello")
            form.save()
            return redirect('display_category')
    else:
        form = CategoryForm()
        # print('h')
    return render(request, "admin-temp/add-category.html",{'form':form})
 
@never_cache
@login_required(login_url='admin_login')
def display_category(request):
    categories = Category.objects.all()
    return render(request, "admin-temp/display-category.html", {'categories': categories})

@never_cache
@login_required(login_url='admin_login')
def update_category(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            category = form.save()
            return redirect('display_category')
    else:
        form = CategoryForm(instance = category)
    return render(request, "admin-temp/update-category.html",{'form':form})



@never_cache
@login_required(login_url='admin_login')
def delete_category(request, id):
    get_object_or_404(Category, id=id).delete()
    return redirect('display_category')









# def product_index(request):
#     return render(request,"admin-templates/products-list-index.html")



@login_required(login_url='admin_login')
def display_product(request):
    products = Product.objects.all()
    return render(request, 'admin-temp/display-product.html',{'products':products})
    



ImageFormSet = ProductImageFormSet = inlineformset_factory(Product, Picture, form=ProductImageForm, extra=5)
@never_cache
@login_required(login_url='admin_login')
def add_product(request):
    print("add product")
    if request.method == 'POST':   
        print("request hit")
        form = ProductForm(request.POST, request.FILES)
        print(form)
        images = request.FILES.getlist('product_image')
        print(images)
        if form.is_valid():
            print("form valied")
            try:
                # update product table
                product = form.save()
                print("form saved")
                # update picture table
                for img in images: 
                    print(img)
                    new_image = Picture(product = product, image = img)
                    new_image.save()
            except Exception as e:
                print(e)
            
            return redirect('display_product')
       
    else:
        form = ProductForm()
        # image_form = ProductImageFormSet(instance=Product())
    return render(request, 'admin-temp/add-product.html', {'form': form})



@never_cache
@login_required(login_url='admin_login')
def update_product(request,id):
    print("request hit")
    product = get_object_or_404(Product, id= id)
    print(product)
    image_form = ImageFormSet(request.POST or None, request.FILES or None, instance=product)
    print(image_form)
    if request.method == "POST":
        print("requested")
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid() and image_form.is_valid():
            product = form.save()
            image_form.save()
            return redirect('display_product')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'admin-temp/update-product.html', {'form': form, 'image_form':image_form})





@never_cache
@login_required(login_url='admin_login')
def delete_product(request, id):
    product = get_object_or_404(Product, id=id)

    # Soft delete by setting is_active to False
    product.is_active = False
    product.save()

    return redirect('display_product')


@never_cache
@login_required(login_url='admin_login')
def undodelete_product(request, id):
    product = get_object_or_404(Product, id=id)

    # Soft delete by setting is_active to False
    product.is_active = True
    product.save()

    return redirect('display_product')




@login_required(login_url='admin_login')
def display_user(request):
    user = CustomUser.objects.all()
    return render(request, 'admin-temp/display-user.html', {'user':user})




@never_cache
@login_required(login_url='admin_login')
def block_user(request, id):
        user = get_object_or_404(CustomUser, id=id)
        user.is_active = False
        user.save()
        return redirect('display_user')
    
    
    
@never_cache
@login_required(login_url='admin_login')
def unblock_user(request, id):
       user = get_object_or_404(CustomUser, id = id)
       user.is_active = True
       user.save()
       return redirect('display_user')

@never_cache
@login_required(login_url='admin_login')
def banner_view(request):
    active_banners = Banner.objects.filter(is_active=True)
    context = {'active_banners': active_banners}
    return render(request, 'accounts/index.html', context)



@never_cache
@login_required(login_url='admin_login')
def add_banner(request):
    print("add banner")
    if request.method == 'POST':
        print("request hit")
        form = BannerForm(request.POST, request.FILES)
        if form.is_valid():
            print("form valid")
            form.save()
            print("banner saved")
            return redirect('display_banner')
    else:
        form = BannerForm()
    
    return render(request, 'admin-temp/add-banner.html', {'form': form})

@never_cache
@login_required(login_url='admin_login')
def add_coupons(request):
    print("add add_coupons")
    if request.method == 'POST':
        print("request hit")
        form = CouponForm(request.POST, request.FILES)
        if form.is_valid():
            print("form valid")
            form.save()
            print("banner saved")
            return redirect('display_coupon')
    else:
        form = CouponForm()
    
    return render(request, 'admin-temp/add-coupon.html', {'form': form})



@login_required(login_url='admin_login')
def display_banner(request):
    banners = Banner.objects.all()
    return render(request, 'admin-temp/display-banner.html',{'banners':banners})

@login_required(login_url='admin_login')
def display_coupon(request):
    coupons = Coupons.objects.all()
    return render(request, 'admin-temp/coupon.html',{'coupons':coupons})

@login_required(login_url='admin_login')
def deactivate_banner(request,id):
    banner = get_object_or_404(Banner, id=id)
    banner.is_active = False
    banner.save()
    return redirect('display_banner')

@login_required(login_url='admin_login')
def activate_banner(request,id):
    banner = get_object_or_404(Banner, id=id)
    banner.is_active = True
    banner.save()
    return redirect('display_banner')

@login_required(login_url='admin_login')
def delete_banner(request, id):
    banner = get_object_or_404(Banner, id=id)
    banner.delete()
    return redirect('display_banner') 

@login_required(login_url='admin_login')
def deactivate_coupon(request,id):
    coupon = get_object_or_404(Coupons, id=id)
    coupon.active = False
    coupon.save()
    return redirect('display_coupon')

@login_required(login_url='admin_login')
def activate_coupon(request,id):
    coupon = get_object_or_404(Coupons, id=id)
    coupon.active = True
    coupon.save()
    return redirect('display_coupon')

@login_required(login_url='admin_login')
def delete_coupon(request, id):
    coupon = get_object_or_404(Coupons, id=id)
    coupon.delete()
    return redirect('display_coupon') 

@login_required
def product_individual(request, id):
    user=request.user
    product = Product.objects.get(pk=id)
    variants = product.productsize_set.all()
    cartitems= Cartitem.objects.filter(user=user)
    print(variants)
    images = Picture.objects.filter(product_id = id)
    
    # categories = Category.objects.get(pk=id)
    return render(request,'user/product-individual.html',{'product':product, 'images':images,'variants':variants,'cartitems':cartitems})



#produc size mangement

def show_varient(request,id):
    product=get_object_or_404(Product, pk=id)
    varient=ProductSize.objects.filter(product=product)
    return render(request ,'admin-temp/view-varient.html',{'varient':varient,'products':product})

def add_variant(request, id):
    product = get_object_or_404(Product, pk=id)

    if request.method == 'POST':
        form = ProductSizeForm(request.POST)
        prod=Product.objects.get(pk=id)
        
        
        if prod.quantity == None:
            prod.quantity=0
        stock_value = int(request.POST['stock'])
        prodt_size = request.POST['size']
        if form.is_valid():
            varient ,variant= ProductSize.objects.get_or_create(product=product,size=prodt_size)
            
            if varient:
                varient.stock+=stock_value
                print(varient.stock,"ff")
                varient.save()
                prod.quantity = prod.quantity + stock_value
                prod.save()
                return redirect('display_product')
            else:
                variant = form.save(commit=False)
                variant.product = product
                variant.save()
                prod.quantity = prod.quantity + stock_value
                prod.save()
                return redirect('display_product')
    else:
        form = ProductSizeForm()
    return render(request, 'admin-temp/add-varient.html', {'product': product, 'form': form})



def del_product_variant(request, id,p_id):
        prod = ProductSize.objects.get(pk=id)
        prod.delete()
        url = reverse('show_varient', args=[p_id])
        return redirect(url)

def display_salesreport(request):
    
    orders = Orders.objects.all().order_by("-created_at")
    return render(request,'admin-temp/salesreport.html',{"order": orders})