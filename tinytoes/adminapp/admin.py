
from django.contrib import admin
from .models import Product,Category,Picture,ProductSize

# Category,Subcategory,ProductVariation,size,ProductSize

# Register your models here.


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Picture)
admin.site.register(ProductSize)


# @admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    fields = ('name', 'image','description', 'price')
    
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description','status')
