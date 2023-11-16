from django.shortcuts import render
from .models import Vendor
from marketplace.models import Product
def vendors(request):
    vendors = Vendor.objects.all()
    
    context = {
        'vendors': vendors,
    }
    return render(request, 'vendors/vendors.html', context)


def vendor_detail(request, vid):
    vendor = Vendor.objects.get(vid=vid)
    products = Product.objects.filter(vendor=vendor,product_status="published")
    
    context = {
        'vendor': vendor,
        'products': products,
    }
    return render(request, 'vendors/vendor-detail.html', context)