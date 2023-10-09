from adminapp import views
from django.urls import path
from django.contrib.auth import views as auth_views


urlpatterns = [
   path('admin_login', views.admin_login, name='admin_login'),
   path('admin_home',views.admin_home,name='admin_home'),
   path('admin_logout',views.admin_logout,name='admin_logout'),


    path('add_category',views.add_category,name='add_category'),
    path('display_category',views.display_category, name="display_category"),
    path('update_category/<str:id>',views.update_category, name="update_category"),
    path('delete_category/<str:id>',views.delete_category, name="delete_category"),


    # path('product_index',views.product_index,name='product_index'),
    path('add_product',views.add_product,name='add_product'),
    path('display_product',views.display_product,name='display_product'),
    path('update_product/<int:id>',views.update_product,name='update_product'),
    path('delete_product/<int:id>',views.delete_product, name="delete_product"),
    path('undodelete_product/<int:id>',views.undodelete_product, name="undodelete_product"),


    path('display_user',views.display_user,name="display_user"),
    path('block_user/<int:id>',views.block_user, name="block_user"),
    path('unblock_user/<int:id>',views.unblock_user, name="unblock_user"),
   


    path('product_individual/<int:id>',views.product_individual,name="product_individual"),
    path('add_varient/<int:id>/',views.add_variant,name='varient'),
    path('delete_varient/<int:id>/<int:p_id>/',views.del_product_variant,name='delete_varient'),
    path('show_varient/<int:id>/',views.show_varient,name='show_varient'),




    path('banners/', views.banner_view, name='banner_view'),
    path('add_banner',views.add_banner,name='add_banner'),
    path('add_coupons',views.add_coupons,name='add_coupons'),
    path('display_banner',views.display_banner,name='display_banner'),
    path('display_coupon',views.display_coupon,name='display_coupon'),
    path('deactivate_banner/<int:id>',views.deactivate_banner,name='deactivate_banner'),
    path('activate_banner<int:id>',views.activate_banner,name='activate_banner'),
    path('delete_banner<int:id>',views.delete_banner,name='delete_banner'),
    path('deactivate_coupon/<int:id>',views.deactivate_coupon,name='deactivate_coupon'),
    path('activate_coupon<int:id>',views.activate_coupon,name='activate_coupon'),
    path('delete_coupon<int:id>',views.delete_coupon,name='delete_coupon'),


    path('display_salesreport',views.display_salesreport,name='display_salesreport')
    

    


    

]