from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from django.contrib.auth.models import User
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'vendor/{0}/{1}'.format(instance.user.id, filename)

class Vendor (models.Model):
    vid = ShortUUIDField(unique=True, length=10, max_length=30, prefix='ven_', alphabet='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=user_directory_path, default='vendor.jpg')
    description = models.TextField(null=True, blank=True, default='Hi am using Agrix')
    
    address = models.CharField(max_length=100, default='address')
    contact = models.CharField(max_length=100, default='contact')
    chat_resp_time = models.CharField(max_length=100, default='100')
    shipping_on_time = models.CharField(max_length=100, default='100')
    authentic_rating = models.CharField(max_length=100, default='100')
    days_return = models.CharField(max_length=100, default='90')
    warranty = models.CharField(max_length=100, default='90')
    
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    
    class Meta:
        verbose_name_plural = 'Vendors'
        
    def vendor_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % self.image.url)
    
    def __str__(self):
        return self.title