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

def search(request):
    query = request.GET.get("q")
    
    vendors = Vendor.objects.filter(title__icontains=query).order_by("-id")

    context = {
        'vendors': vendors,
        'query': query,
    }
    return render(request, 'vendors/search.html', context)