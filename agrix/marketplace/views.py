from django.shortcuts import render
from .models import Product, Category
def marketplace(request):
    popular = Product.objects.filter(featured=True, product_status="published").order_by('-id')[:5]
    products = Product.objects.all().order_by('-id')
    
    context = {
        'popular': popular,
        'products': products,
    }
    return render(request, 'marketplace/marketplace.html', context)

def product_list(request):
    products = Product.objects.all().order_by('-id')
    context = {
        'products': products,
    }
    return render(request, 'marketplace/product-list.html', context)

def product_detail(request, pid):
    product = Product.objects.get(pid=pid)
    p_images = product.p_images.all()
    context = {
        'product': product,
        'p_images': p_images,
    }
    return render(request, 'marketplace/product-detail.html', context)




def category_product_list(request, cid):
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(product_status="published",category=category).order_by('-id')
    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'marketplace/category-product-list.html', context)



def category_list(request):
    category = Category.objects.all()
    context = {
        'category': category,
    }
    return render(request, 'marketplace/category-list.html', context)
