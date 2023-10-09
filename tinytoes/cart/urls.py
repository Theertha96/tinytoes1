from cart import views
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import CheckoutView,DeleteAddressView

 
urlpatterns = [
   path('add_to_cart',views.add_to_cart,name='add_to_cart'),
   path('display_cart',views.display_cart,name='display_cart'),
   path('remove_cart/<int:id>',views.remove_cart,name='remove_cart'),
   path('update_cart_item_quantity',views.update_cart_item_quantity,name='update_cart_item_quantity'),
   path('checkout',CheckoutView.as_view(),name='checkout'),
  
   path('order',views.order,name='order'),
   path('order_success',views.order_success,name='order_success'),
   path('cancel_order/<int:id>/',views.cancel_order,name="cancel_order"),
   path('orderpage',views.orderpage,name="orderpage"),
   path('order_detail/<int:id>/',views.order_detail,name="order_detail"),
   path('edit_order/<int:id>/',views.edit_order,name="edit_order"),
   path('return_product/<int:id>/',views.return_product,name="return_product"),
   path('applycoupon',views.apply_coupon,name="apply_coupon"),

   




   path('add_address',views.add_address,name='add_address'),
   # path('display_address',views.display_address,name='display_address'),
   path('delete_address/<int:id>/', DeleteAddressView.as_view(), name='delete_address'),
]