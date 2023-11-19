from django.shortcuts import render
from marketplace.models import Product


# Create your views here.
def home(request):
    products = Product.objects.filter(featured=True,product_status="published").order_by('-id')[:10]
    
    context = {
        'products': products
    }
    return render(request, 'home/home.html', context)

def about(request):
    return render(request, 'home/about.html')

def contact(request):
    return render(request, 'home/contact.html')

def faq(request):
    return render(request, 'home/faq.html')

def privacy(request):
    return render(request, 'home/privacy.html')

def terms(request):
    return render(request, 'home/terms.html')

