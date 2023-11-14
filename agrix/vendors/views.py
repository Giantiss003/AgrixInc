from django.shortcuts import render
from .models import Vendor

def vendors(request):
    vendors = Vendor.objects.all()
    
    context = {
        'vendors': vendors
    }
    return render(request, 'vendors/vendors.html', context)
