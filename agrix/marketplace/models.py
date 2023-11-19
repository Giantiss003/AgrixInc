from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from auths.models import CustomUser
from vendors.models import Vendor
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'vendor/{0}/{1}'.format(instance.user.id, filename)

STATUS_CHOICES = (
    ('processing', 'Processing'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered'),
)

STATUS = (
    ('draft', 'Draft'),
    ('disabled', 'Disabled'),
    ('rejected', 'Rejected'),
    ('in_review', 'In Review'),
    ('published', 'Published'),
)

class Category(models.Model):
    # Categorizes Products based on their cid
    cid = ShortUUIDField(unique=True, length=10, max_length=30, prefix='cat_', alphabet='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category', default='category.jpg')
    
    class Meta:
        verbose_name_plural = 'Categories'

    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % self.image.url)

    def __str__(self):
        return self.title
    
    
class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=30, prefix='prod_', alphabet='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product', default='product.jpg')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True, related_name='product')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name='category')
    description = RichTextUploadingField(null=True, blank=True)
    
    price = models.DecimalField(max_digits=10, decimal_places=2, default=10.00)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, default=5.00)
    specifications = RichTextUploadingField(null=True, blank=True)
    product_status = models.CharField(max_length=100, choices=STATUS, default='in_review')
    tags = TaggableManager(blank=True)
    status = models.BooleanField(default=True)
    stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    
    digital = models.BooleanField(default=False, null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True, default='Organic')
    life = models.CharField(max_length=100, null=True, blank=True, default='7 Days')
    mfg = models.DateField(auto_now_add=False, null=True, blank=True)
    stock_count = models.IntegerField(default=10)
    
    sku = ShortUUIDField(unique=True, length=10, max_length=30, prefix='sku_', alphabet='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        verbose_name_plural = 'Products'
        
    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % self.image.url)
    
    def __str__(self):
        return self.title
    
    def get_percentage(self):
        return int((self.old_price - self.price) / self.old_price * 100)

class ProductImages(models.Model):
    images = models.ImageField(upload_to='product-images', default='product.jpg')    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name='p_images')
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Product Images' 


class CartOrder(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    price = models.DecimalField(max_digits=100, decimal_places=2, default=10.00)
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='processing')
    
    class Meta:
        verbose_name_plural = 'Cart Orders'
        
    def __str__(self):
        return self.item.title


class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE, null=True)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    qty = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=100, decimal_places=2, default=10.00)
    total = models.DecimalField(max_digits=100, decimal_places=2, default=10.00)
    
    class Meta:
        verbose_name_plural = 'Cart Order Items'
    def order_img(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % self.image)      
    
class Tax(models.Model):
    tax_type = models.CharField(max_length=20, unique=True)
    tax_percentage = models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Tax Percentage (%)')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'tax'

    def __str__(self):
        return self.tax_type

    
class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Wishlists'
        
    def __str__(self):
        return self.product.title
    
    
class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=200, null=True)
    status = models.BooleanField(default=False)    
           
        