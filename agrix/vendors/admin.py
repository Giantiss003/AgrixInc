from django.contrib import admin

from .models import Vendor

class VendorAdmin(admin.ModelAdmin):
    list_display = ('title', 'vendor_image')
    list_filter = ['title', 'address', 'contact']
    search_fields = ['title', 'address', 'contact']
    list_per_page = 10
    
    class Meta:
        model = Vendor
        
admin.site.register(Vendor, VendorAdmin)        
