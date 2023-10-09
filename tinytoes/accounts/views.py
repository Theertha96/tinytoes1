from django.shortcuts import redirect, render
from accounts.models import CustomUser
from django.contrib.auth import authenticate,login as auth_login,logout
from django.contrib import messages
from django.views.decorators.cache import never_cache
from . import verify

from adminapp.models import Product
from adminapp.models import Category,Banner
from accounts.models import Address
from cart.models import Cart,Orders




# Create your views here.

@never_cache
def home(request):
    products = Product.objects.all().filter(is_available=True)
    categories = Category.objects.all()
    banners=Banner.objects.all()
    return render(request,'user/index.html',{'products':products,'categories':categories,'active_banners':banners})



def signup(request):
    print("signup")
    if request.method == "POST":
        
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number='+91'+request.POST.get('phone')
        pass1 = request.POST.get('password')
        pass2 = request.POST.get('confirmpassword')
        
        if pass1 != pass2:
            return render(request,"user/signup.html",{"error":"password missmach"})
        
        try:
            print("post creatre")
            myuser = CustomUser.objects.create_user(name=name,email=email,password=pass1,phone_number=phone_number)
            print("user created")
        except Exception as e:
            print("exception found!")
            return render(request,"user/signup.html",{"error":"email already exist!"})
        
        return redirect("user_login")
    return render(request,"user/signup.html")



def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['register-email']
        password = request.POST['register-password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
           auth_login(request,user)
           return redirect('home')
        else:
            messages.error(request,"User name or password is incorect")
    return render(request,"user/login.html")




def user_logout(request):
    logout(request)
    return redirect('user_login')





def verify_code(request):
    if request.method == 'POST':
        # form = VerifyForm(request.POST)
        # if form.is_valid():
            # code = form.cleaned_data.get('code')
            code =  request.POST['otp']
            phone_no = request.session.get('phone')
            
            if verify.check(phone_no, code):
                user = CustomUser.objects.get(email=request.session.get('email')) 
                userobj = CustomUser.objects.filter(email=request.session.get('email')) 
                print(user)
                print(user.is_authenticated)
                print(user.is_active)
                print(user.is_superuser)
                if userobj.exists() and user.is_active and not user.is_superuser: 
                    print(user.is_authenticated)
                    auth_login(request, user)
                    return redirect('home')  
                # print(user)
                return redirect('home') 
            else:
                print("error")
    else:
        # form = VerifyForm()
     return render(request, 'user/verify.html')



def check_phone_number(phone_number):
    return CustomUser.objects.filter(phone_number=phone_number).first()

def username_password(phone):
    user = CustomUser.objects.filter(phone_number=phone).first()
    return user

def phone_verify(request):
    print("in phn")
    if request.method == "POST":
        
        phone = '+91'+  str(request.POST['phone_number'])
        if check_phone_number(phone):
            
            verify.send(phone)
            
            user = username_password(phone)
            request.session['email'] = user.email 
            print(user.email)  
            user.is_verified = True
            user.is_active = True
            user.save()
            request.session['phone'] = phone
            return redirect('verify_code') 
        else:
            context = "Please register first"
            return render(request, 'user/phone_verify.html', {'context': context})
    return render(request, 'user/phone_verify.html')



def user_profile(request):
    user = request.user
    address = Address.objects.filter(user=user)
    orders = Orders.objects.filter(user=request.user).order_by("-created_at")
    # orders = Orders.objects.filter(user=request.user).order_by("-created_at")
    # orders = Orders.objects.all().order_by("-created_at")
    return render(request,'user/dashboard.html',{'user':user,'address':address,'orders':orders})

def edit_profile(request):
    print("edit_user")
    user_id = request.user.id
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('mail')
        new_password = request.POST.get('pass')

        try:
            user = CustomUser.objects.get(id=user_id)
            user.name = name
            user.email = email

            if new_password:
                user.set_password(new_password)
            
            user.save()
            print("user updated")
        except CustomUser.DoesNotExist:
            return render(request, "user/edit_profile.html", {"error": "User not found"})
        
        return redirect("user_login")  # Redirect to user profile page
    else:
        try:
            user = CustomUser.objects.get(id=user_id)
            return render(request, "user/edit_user.html", {"user": user})
        except CustomUser.DoesNotExist:
            return render(request, "user/edit_user.html", {"error": "User not found"})

# In your urls.py
# path('edit_user/<int:user_id>/', edit_user, name='edit_user')


