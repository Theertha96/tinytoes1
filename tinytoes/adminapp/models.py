import datetime
import os
from django.db import models
from django.utils.text import slugify

# Create your models here.

  
def getFileName(request, filename):
        now_time = datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
        new_filename = "%s%s"%(now_time, filename)
        return os.path.join('uploads/',new_filename)



class Category(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    # slug = models.SlugField(max_length=100,default='')
    image = models.ImageField(upload_to=getFileName,null=True,blank=True)
    description = models.TextField(max_length=150, null=False, blank=False)
    status = models.BooleanField(default=False,help_text="0-show,1-Hidden",blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return self.name
    
    
class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE,default='')
    name = models.CharField(max_length=100, null=False, blank=False)
    # slug = models.SlugField(max_length=255, null=True, blank=True,default='')
    # vendor = models.CharField(max_length=100, null=False, blank=False)
    product_image = models.ImageField(upload_to='product/',null=False,blank=False)
    quantity = models.PositiveIntegerField(default=0,null=True,blank=True)
    original_price = models.FloatField(null=False,blank=False,default=0)
    selling_price = models.FloatField(null=False,blank=False,default=0)
    offer_price = models.FloatField(null=True,blank=True)
    description = models.TextField(max_length=350, null=False,blank=False,default='')
    status = models.BooleanField(default=False,help_text="0-show,1-Hidden",blank=True)
    # trending = models.BooleanField(default=False,help_text="0-default,1-Trending",blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=datetime.datetime.now)
    offer_status = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['id']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def _str_(self):
        return self.name
    
    
class Picture(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_pictures")
    image = models.ImageField(upload_to='product/', blank=True)
    

    def str(self):
        return self.image.url
    

class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=20)
    stock = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.product.name} - {self.size}"

class Banner(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='banners/')
    link = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0, help_text="Order in which the banner should be displayed")
    is_active = models.BooleanField(default=True, help_text="Set to 'True' to display the banner")

    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title
