from django.contrib import messages
import logging
import json
from decimal import Decimal, InvalidOperation
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
    cart_product = {
        str(request.GET.get('id')): {
            'title': request.GET.get('title'),
            'qty': request.GET.get('qty'),
            'price': request.GET.get('price'),
            'pid': request.GET.get('pid'),
            'image': request.GET.get('image'),
        }
    }
    
    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']
        if str(request.GET.get('id')) in cart_data:
            # Update quantity if product is already in cart
            cart_data[str(request.GET.get('id'))]['qty'] = cart_product[str(request.GET.get('id'))]['qty']
            request.session.modified = True  # Flag the session as modified to ensure changes are saved
            return JsonResponse({'status': 'info',
                                 'message': 'Product Quantity Added. Item Already in cart!',
                                 'data': request.session['cart_data_obj'],
                                 'totalcartitems': len(request.session['cart_data_obj'])
                                 })
        else:
            # Add product to cart
            cart_data.update(cart_product)
            request.session.modified = True  # Flag the session as modified to ensure changes are saved
            return JsonResponse({'status': 'success',
                                 'message': 'Product added to cart successfully!',
                                 'data': request.session['cart_data_obj'],
                                 'totalcartitems': len(request.session['cart_data_obj'])
                                 })
    else:
        # Add product to cart
        request.session['cart_data_obj'] = cart_product
        message = 'Product added to cart successfully!'
    
    request.session.modified = True  # Flag the session as modified to ensure changes are saved
    return JsonResponse({
        'status': 'success',
        'message': message,
        'data': request.session['cart_data_obj'],
        'totalcartitems': len(request.session['cart_data_obj'])
    })

def cart(request):
    cart_total_amount = Decimal('0.00')
    cart_data = request.session.get('cart_data_obj', {})

    for p_id, item in cart_data.items():
        try:
            price = Decimal(item.get('price', '0.00'))
        except InvalidOperation:
            # Handle the case where the price is not a valid decimal
            price = Decimal('0.00')

        qty = int(item.get('qty', 0))
        cart_total_amount += price * qty

    context = {
        'cart_data': cart_data,
        'totalcartitems': len(cart_data),
        'cart_total_amount': cart_total_amount,
    }

    return render(request, 'marketplace/cart.html', context)


def delete_from_cart(request):
    if request.method == 'POST':
        product_id = str(request.POST.get('id'))

        cart_data = request.session.get('cart_data_obj', {})
        if product_id in cart_data:
            del cart_data[product_id]
            request.session['cart_data_obj'] = cart_data
            request.session.modified = True
            return JsonResponse({
                'status': 'success',
                'message': 'Product removed from cart successfully!',
                'data': request.session['cart_data_obj'],
                'totalcartitems': len(request.session['cart_data_obj'])
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Product not found in cart!',
            })

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method!',
    })


def increase_cart_quantity(request):
    if request.method == 'POST':
        product_id = request.POST.get('id')
        quantity = int(request.POST.get('qty', 1))  # Default to 1 if qty is not provided
        
        if 'cart_data_obj' in request.session:
            cart_data = request.session['cart_data_obj']
            if product_id in cart_data:
                cart_data[product_id]['qty'] = int(cart_data[product_id]['qty']) + quantity
                request.session['cart_data_obj'] = cart_data
                request.session.modified = True
                return JsonResponse({
                    'status': 'success',
                    'message': 'Quantity increased successfully!',
                    'data': request.session['cart_data_obj'],
                    'totalcartitems': len(request.session['cart_data_obj'])
                })
        return JsonResponse({
            'status': 'error',
            'message': 'Product not found in cart!',
        })
def decrease_cart_quantity(request):
    if request.method == 'POST':
        product_id = request.POST.get('id')
        quantity = int(request.POST.get('qty', 1))  # Default to 1 if qty is not provided
        
        if 'cart_data_obj' in request.session:
            cart_data = request.session['cart_data_obj']
            if product_id in cart_data:
                if int(cart_data[product_id]['qty']) > quantity:
                    cart_data[product_id]['qty'] = int(cart_data[product_id]['qty']) - quantity
                    request.session['cart_data_obj'] = cart_data
                    request.session.modified = True
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Quantity decreased successfully!',
                        'data': request.session['cart_data_obj'],
                        'totalcartitems': len(request.session['cart_data_obj'])
                    })
                else:
                    # If quantity is already 1, remove the item from the cart
                    del cart_data[product_id]
                    request.session['cart_data_obj'] = cart_data
                    request.session.modified = True
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Product removed from cart successfully!',
                        'data': request.session['cart_data_obj'],
                        'totalcartitems': len(request.session['cart_data_obj'])
                    })
        
        return JsonResponse({
            'status': 'error',
            'message': 'Product not found in cart!',
        })
