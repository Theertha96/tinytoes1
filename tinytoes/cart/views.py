from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.forms.models import model_to_dict
import razorpay
from django.conf import settings
from cart.models import Cartitem
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from adminapp.models import *
from cart.models import *
from accounts.models import Address
from datetime import date
import json
from django.views.decorators.http import require_POST


def calculate_total(request):
    cart_items = Cartitem.objects.filter(user=request.user)  # Assuming you have a CartItem model with a user field
    print(cart_items)
   
    # Calculate the subtotal for each cart item
    subtotal_list = [item.quantity * item.total for item in cart_items]
    print(subtotal_list , 'sdhgvsghdvshgvdmasvdh')

    # Calculate the total by summing up the subtotals
    total = sum(subtotal_list)
   
    return total

@login_required
def add_to_cart(request):
    # Fetch product_id from the request
    product_id = request.GET.get('product_id')
    print(product_id)
    product = Product.objects.get(pk=product_id)
    variant_size = request.GET.get('size')
    print(variant_size)
   

    if request.user.is_authenticated:
        # If the user is logged in, add the item to their cart
        user = request.user
        cart, _ = Cart.objects.get_or_create(user=user)
        
        # Check if a variant price is selected
        if variant_size :
            # Get the variant based on the selected price
            variant = ProductSize.objects.get(product=product, size=variant_size)
            print(variant)
            
            if product.offer_price :
                price = product.offer_price
            else :
                price = product.selling_price

            cart_item, item_created = Cartitem.objects.get_or_create(user=user, Product=product, varient=variant, cart=cart,total=price*1)
            if not item_created and variant.stock > 1:
                cart_item.quantity += 1
           
        else:
            if product.offer_price :
                price = product.offer_price
            else :
                price = product.selling_price
            # If no variant is selected, add the base product to the cart
            cart_item, item_created = Cartitem.objects.get_or_create(user=user, Product=product, cart=cart,total=price*1)
            if not item_created and product.quantity > 1:
                cart_item.quantity += 1
        
        
        cart_item.save()
        if 'total' in request.session:
            del request.session['total']
        
        
        return JsonResponse({"status": 200, "message": "added"})
  
def update_cart_item_quantity(request):
        cart_item_id = request.GET.get('cart_item_id')
        action = request.GET.get('action')
       

        try:
           cart_item = Cartitem.objects.get(id=cart_item_id) 
           print(cart_item)
        except cart_item.DoesNotExist:
            return JsonResponse({'status': 404, 'error': 'Cart item not found'})

        if action == 'increase':
            if cart_item.quantity < cart_item.Product.quantity:
                cart_item.quantity += 1
        elif action == 'decrease':
            cart_item.quantity -= 1 if cart_item.quantity > 1 else 0
        
        cart_item.save()
           
        print("deleted",request.session.get('total'))
        subtotal=calculate_total(request)
        print(subtotal)


        # if 'total' in request.session:
        #     del request.session['total']
        #     print("deleted")
        #     print(request.session.get('total'))
  

        return JsonResponse({'status': 200,'quantity': cart_item.quantity,'subtotal': cart_item.sub_total(),"total_total":subtotal })

# @login_required(login_url="user_login")
def display_cart(request):
    

    cart = Cart.objects.filter(user=request.user).first()
    coupons = Coupons.objects.all()
  
    cart_items = Cartitem.objects.filter(cart=cart)

    print(cart_items)


    if(request.session.get('total')):
            subtotal=request.session.get('total')
            print("hell",request.session.get('total'))
            discount=request.session.get('discount')
    else:
        subtotal=calculate_total(request)
        discount=0
    sub_total=calculate_total(request)

    print(subtotal)
    # Calculate the subtotal for each cart item
    # if User.is_not_authenticated:
    #     return redirect('user_login')
    
    return render(request, 'user/cart.html',{'cart': cart,'cart_items': cart_items,"total_total":subtotal,"coupons":coupons,"discount":discount,"sub_total":sub_total})

@login_required
def remove_cart(request, id):
    print("rrr")
    user = request.user
    cart_item = Cartitem.objects.get(id=id, user=user)
    
    # Remove the cart item from the cart
    cart_item.delete()
    print("itshere",request.session.get('total'))
    if 'total' in request.session:
            del request.session['total']
    print("itsdeleted",request.session.get('total'))
    


    return redirect('display_cart')

class CheckoutView(View):

    def get(self, request):
        cart=Cart.objects.get(user=request.user)
        cart_items = Cartitem.objects.filter(user=request.user)
        # subtotal=cart_items.aggregate(total=Sum('total'))
        # subtotal=calculate_total(request)
        subtotal=request.session['total']

        print(request.body)
        address = Address.objects.filter(user=request.user)
        # print(address)
        
        context = {
            'cart_items': cart_items,
            # 'subtotal':subtotal['total'],
            'address': address,
            "total_total":subtotal,
             'cart':cart.cart_id,
             
        }

        return render(request, 'user/checkout.html',context)

def add_address(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state= request.POST.get('state')
        pincode = request.POST.get('pincode')
        phone = request.POST.get('phonenumber')
        # print(request.body)
        # print(name, city, pincode, phone,address)

        address = Address.objects.create(
            user=request.user,
            name=name,
            city=city,
            state=state,
            pincode=pincode,
            phone=phone,
            address=address,
        )
        address.save()
        return redirect('checkout')  
    return render(request, 'user/add-address.html')

class DeleteAddressView(View):
    def get(self, request, id):
        prod = Address.objects.get(id=id)
        print(prod)
        prod.delete()
        return redirect('checkout')

def home(request):
    return render(request,"user/index.html")

def order(request):
    if request.method == 'POST':
        payment_method = request.POST.get('paymentmethod')
        
        if payment_method == "Razor Payment":
            client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
            amount=request.POST.get('grandPriceText')
            print(client,amount)
            grand_total = int(amount)
            

# Print the datatype
            print(amount)
            razor_payment = client.order.create({ "amount": grand_total*100, "currency": "INR", "receipt": "order_rcptid_11" })
            
            cart_items = Cartitem.objects.filter(user=request.user)
            address = request.POST.get('address')
            address_details = Address.objects.get(id=address)

            payment = Payment.objects.create(
                user=request.user,
                payment_method=request.POST.get('paymentmethod'),
                amount=request.POST.get('grandPriceText'),
            )
            payment.save()
            

            order = Orders.objects.create(
                user=request.user,
                payment=payment,
                address=address_details,
                ordered=False,
                status="New",
                quantity=False,
            )
            order.save()

            for cart_item in cart_items:
                ordered_product = OrderProduct.objects.create(
                    order=order,
                    product=cart_item.Product,
                    quantity=cart_item.quantity,
                    product_price=cart_item.Product.selling_price,
                    ordered=False,
                    is_paid=False,
                    payment=payment,
                    user=request.user,
                    address=address_details,
                )

                if isinstance(cart_item.varient, ProductSize):
                    variant = cart_item.varient
                    variant.stock -= cart_item.quantity
                    variant.save()
                elif isinstance(cart_item.Product, Product):
                    product = cart_item.Product
                    product.quantity -= cart_item.quantity
                    product.save()
                cart_items.delete()
                
            response_data = {'order_id': ordered_product.id,
                             'payment_id': razor_payment['id'],
                             'amount_paid': razor_payment['amount'],
                             'key': settings.KEY,
                             'orders_id':order.id
                             }
          
            return JsonResponse({'response': response_data})
        else:
            cart_items = Cartitem.objects.filter(user=request.user)
            address = request.POST.get('address')
            address_details = Address.objects.get(id=address)

            payment = Payment.objects.create(
                user=request.user,
                payment_method=request.POST.get('paymentmethod'),
                amount=request.POST.get('grandPriceText'),
            )
            payment.save()

            order = Orders.objects.create(
                user=request.user,
                payment=payment,
                address=address_details,
                ordered=False,
                status="New",
                quantity=False,
            )
            order.save()

            for cart_item in cart_items:
                ordered_product = OrderProduct.objects.create(
                    order=order,
                    product=cart_item.Product,
                    quantity=cart_item.quantity,
                    product_price=cart_item.sub_total(),
                    ordered=False,
                    is_paid=False,
                    payment=payment,
                    user=request.user,
                    address=address_details,
                )

                if isinstance(cart_item.varient, ProductSize):
                    variant = cart_item.varient
                    variant.stock -= cart_item.quantity
                    variant.save()
                elif isinstance(cart_item.Product, Product):
                    product = cart_item.Product
                    product.quantity -= cart_item.quantity
                    product.save()
                cart_items.delete()
                

            response_data = {'order_id': ordered_product.id,
                             'orders_id':order.id,
                             }
            return JsonResponse({'response': response_data})
    else:
        return JsonResponse({'message': "failed"})

def order_success(request):
    order_id = request.GET.get('order_id')
  
    orders1 = request.GET.get('orders')
    print(orders1)
    ordered_products = OrderProduct.objects.filter(order_id=orders1)  
    orders = Orders.objects.filter()           
    # order = get_object_or_404(Orders, id=order_id)
    order = OrderProduct.objects.get(id=order_id)
    print(order)
    product = order.product
    product_dict = model_to_dict(product)    
    # Access the fields from the related Product model
    product_image = product_dict['product_image'].url
    selling_price = product_dict['selling_price']
    # Retrieve other fields from the OrderProduct model
    user = order.user
    address = order.address
    ordered = order.ordered
    is_paid = order.is_paid
    status = order.status
    quantity = order.quantity
    payment = order.payment      
    context = {
        'order_id': order_id,
        'quantity': quantity,
        'product_price':selling_price,
        'product_name': product_dict['name'],
        'ordered':ordered,
        'is_paid':is_paid,
        'user': str(user),
        'address':address,
        'status':status,
        'product':product,
        'payment':payment,
        'image_url':product_image,
        'ordered_products': ordered_products,
    }                                    
    return render(request,'user/success1.html',context)

def cancel_order(request,id):
    order = Orders.objects.get(pk = id)
    
    user = request.user
    wallet = user.wallet
    print('sdsd',order.payment.amount)
    print('the sum is' , wallet + order.payment.amount)
    if order.payment.payment_method == 'Razor Payment':
        print('aaa rzor' ,  )
        wallet += order.payment.amount
        user.wallet = wallet
        print(wallet)
        user.save()

    order.status="cancelled"
    order.save()
    return redirect('user_profile')

def orderpage(request):
    orders = Orders.objects.all().order_by("-created_at")
    print(orders)
    return render(request, "admin-temp/page-orders.html", {"orders": orders})

def edit_order(request, id):
    user=request.user
    
    if request.method == "POST":
        status = request.POST.get("status")
        try:
        
            order = Orders.objects.get(pk=id)
            order.status = status
            order.save()
            if status == 'Delivered':
                pyment=order.payment
                pyment.status='Success'
                pyment.save()
            if status == 'return accepted':
                user = request.user
                wallet = user.wallet
                wallet += order.payment.amount
                user.wallet = wallet
                print(wallet)
                user.save()

        except Orders.DoesNotExist:
            pass
    return redirect("orderpage")

def return_product(request,id):
    if request.method == "POST":

     print(id)
     order = Orders.objects.get(pk=id)
     order.status = 'Return requested'
     order.save()
    return redirect("user_profile")

    






def order_detail(request,id):
    main_order = Orders.objects.get(pk = id)
    print(main_order)
    orders = OrderProduct.objects.filter(order = main_order)
   
    return render(request,'admin-temp/orders-detail.html',{"orders": orders,"id":id,"main_order":main_order})



@require_POST
def apply_coupon(request):
        body = json.loads(request.body)
        grand_total = int(body['grand_total'])
        coupon_code = body['coupon']
        try:
            coupon = Coupons.objects.get(code__iexact=coupon_code)
        except Coupons.DoesNotExist:
            data = {
                "total": grand_total,
                "message": "Not a Valid Coupon"
            }
        else:
            today = date.today()
            valid_from = coupon.valid_from.date()
            valid_to = coupon.valid_to.date()
            discount=int(coupon.discount)
            min_amount = int(coupon.min_amount)
            if min_amount < grand_total and valid_from <= today <= valid_to:
                grand_total = grand_total - discount
                request.session['total'] = grand_total  # Update the session variable
                request.session['discount']=discount
                data = {
                    'discount':discount,
                    "total": grand_total,
                    "message": f"{coupon.code} Applied"
                }
            else:
                data = {
                    
                    "total": grand_total,
                    "message": "Not a Valid Coupon"
                }
        print(data.get('total'))
        return JsonResponse(data)