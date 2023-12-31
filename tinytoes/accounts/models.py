from django.db import models

# Create your models here.


from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField 
from accounts.manager import CustomUserManager
from django.contrib.auth import get_user_model
# from cart.models import User

# from django.contib.auth.models import user 
# Create your models here.


class CustomUser(AbstractUser):
    username = None
    name=models.CharField(max_length=50,default=None)
    phone_number = PhoneNumberField(max_length=15, blank=True)
    email = models.EmailField(null=True, blank=True, max_length=255, unique=True)
    password=models.CharField(max_length=100)
    is_verified = models.BooleanField(default= True)                                        
    is_active = models.BooleanField(default= True)
    wallet=models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','password']

    objects = CustomUserManager()
    

class profile(models.Model):
    # user = models.OneToOneField(user, on_delete=models.CASCADE)
    forget_password_token=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def _str_(self):
        return self.user.username
    


User = get_user_model()

class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True) 
    name = models.CharField(max_length=100,null=True)
    address = models.CharField(max_length=100,null=True)
    city = models.CharField(max_length=50) 
    state = models.CharField(max_length=50,default='') 
    pincode = models.IntegerField(blank=True)
    phone = models.CharField(max_length=15,null=True)

    def str(self):
       return self.name
