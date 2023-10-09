from accounts import views
from django.urls import path
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('',views.home,name='home'),
    path('signup',views.signup,name='signup'),
    path('user_login',views.user_login,name='user_login'),
    path('user_logout',views.user_logout,name='user_logout'),
    path('phone_verify',views.phone_verify, name="phone_verify"),
    path('verify_code/', views.verify_code, name="verify_code"),
    path('user_profile',views.user_profile,name='user_profile'),
    path('edit_profile',views.edit_profile,name="edit_profile"),




]