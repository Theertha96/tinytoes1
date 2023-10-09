from django import forms
# from.models import Amodel
from accounts.models import *
from django.contrib.auth.models import User

from adminapp.models import  *


class CategoryForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'name'}))
    #offer = forms.ModelChoiceField(required = False,queryset=Offer.objects.all() ,widget=forms.Select(attrs={'class':'form-select'}))
    # image = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control','id':'formFile'}),required=False)
    description = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'description'}))
    status = forms.BooleanField(required=False)

    class Meta:
        model = Category
        fields = ['name','image', 'description','status']


class ProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(),widget=forms.Select(attrs={'class':'form-select'}))
    # brand = forms.ModelChoiceField(queryset=Brand.objects.all(),widget=forms.Select(attrs={'class':'form-select'}))
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control' ,'id':'name'}))
    product_image = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control','id':'formFile',}))
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control','id':'quantity'}),required=False)
    selling_price = forms.FloatField(widget=forms.NumberInput(attrs={'class':'form-control','id':'selling_price'}))
    original_price = forms.FloatField(widget=forms.NumberInput(attrs={'class':'form-control','id':'original_price'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'description'}))
    status = forms.BooleanField(required=False)
    is_available = forms.BooleanField(required=False)
    is_active = forms.BooleanField(required=False)
    offer_price=forms.FloatField(widget=forms.NumberInput(attrs={'class':'form-control','id':'offer_price'}),required=False)
    
    
    class Meta:
        model = Product
        fields = ['category','name', 'product_image', 'quantity','selling_price','original_price','offer_price', 'description','status',  'is_available',]

class ProductImageForm(forms.ModelForm):
    
    class Meta:
        model = Picture
        fields = ['image']


from .models import Banner
from cart.models import Coupons

class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ['title', 'image', 'link', 'order', 'is_active']

class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupons
        fields = ['code','discount','valid_from','valid_to','min_amount','active']

class ProductSizeForm(forms.ModelForm):
    class Meta:
        model = ProductSize
        fields = [ 'size', 'stock']
