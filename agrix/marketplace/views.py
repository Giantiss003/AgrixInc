from django.contrib import messages
import logging
import json
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import Product, Category
# from vendors.models import Vendor
from taggit.models import Tag
from django.contrib.auth.decorators import login_required
# from django.template.loader import render_to_string
def marketplace(request):
    popular = Product.objects.filter(featured=True, product_status="published").order_by('-id')[:5]
    products = Product.objects.all().order_by('-id')
    
    context = {
        'popular': popular,
        'products': products,
    }
    return render(request, 'marketplace/marketplace.html', context)

def search(request):
    query = request.GET.get("q")
    
    products = Product.objects.filter(title__icontains=query).order_by("-date")

    context = {
        'products': products,
        'query': query,
    }
    return render(request, 'marketplace/search.html', context)
# TODO: FIGURE OUT HOW TO USE PRODUCT LIST(REDUNDANT CODE, SEE MARKETPLACE VIEW)
# def product_list(request):
#     products = Product.objects.all().order_by('-id')
#     Categories = Category.objects.all().order_by('-id')[:10]
#     vendors = Vendor.objects.all().order_by('-id')[:10]
#     context = {
#         'products': products,
#         'categories': Categories,
#         'vendors': vendors,
#     }
#     return render(request, 'marketplace/product-list.html', context)

def product_detail(request, pid):
    product = Product.objects.get(pid=pid)
    p_images = product.p_images.all()
    products = Product.objects.filter(category=product.category).exclude(pid=pid).order_by('-id')
    context = {
        'product': product,
        'p_images': p_images,
        'products': products,
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


def tag_list(request, tag_slug=None):
    """
    Retrieves a list of products based on a given tag.
    
    Args:
        request (object): The HTTP request object.
        tag_slug (string, optional): The slug of the tag to filter the products by.
    
    Returns:
        Rendered HTML template with the filtered products as the context.
    """
    products = Product.objects.filter(product_status="published").order_by('-id')
    
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])
    
    context = {
        'products': products,
        'tag': tag,
    }
    return render(request, 'marketplace/tag.html', context)

# TODO: FILTERING PRODUCT USING AJAX REQUESTS
# def filter_product(request):
#     """
#     Retrieves a list of products based on a given filter.
    
#     Args:
#         request (object): The HTTP request object.
    
#     Returns:
#         Rendered HTML template with the filtered products as the context.
#     """
#     categories = request.GET.getlist('category[]')
#     vendors = request.GET.getlist('vendor[]')
#     products = Product.objects.filter(product_status="published").order_by('-id').distinct()

#     if len(categories) > 0:
#         products = products.filter(category__id__in=categories).distinct()

#     if len(vendors) > 0:
#         products = products.filter(vendor__id__in=vendors).distinct()

    
#     data = render_to_string('marketplace/async/product-list.html', {'products': products})
#     return JsonResponse({'data': data})

######################################CART###########################################
    
def add_to_cart(request):
    cart_product = {}
    cart_product[str(request.GET.get('id'))] = {
        'title': request.GET.get('title'),
        'qty': request.GET.get('qty'),
        'price': request.GET.get('price'),
        'pid': request.GET.get('pid'),
        'image': request.GET.get('image'),
    }
    
    if 'cart_data_obj' in request.session:
        if str(request.GET.get('id')) in request.session['cart_data_obj']:
            # check if product is already in cart
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET.get('id'))]['qty'] = cart_product[str(request.GET.get('id'))]['qty']
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
            return JsonResponse({'status': 'info',
                                 'message': 'Product Already in cart!',
                                 'data': request.session['cart_data_obj'],
                                 'totalcartitems': len(request.session['cart_data_obj'])
                                 })
        else:
            # add product to cart
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
            return JsonResponse({'status': 'success',
                                 'message': 'Product added to cart successfully!',
                                 'data': request.session['cart_data_obj'],
                                 'totalcartitems': len(request.session['cart_data_obj'])
                                 })
    else:
        # add product to cart
        request.session['cart_data_obj'] = cart_product
        return JsonResponse({'status': 'success',
                             'message': 'Product added to cart successfully!',
                             'data': request.session['cart_data_obj'],
                             'totalcartitems': len(request.session['cart_data_obj'])
                             })        