from django.shortcuts import get_object_or_404, render
from .models import Product, Category
from taggit.models import Tag
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

def product_list(request):
    products = Product.objects.all().order_by('-id')
    context = {
        'products': products,
    }
    return render(request, 'marketplace/product-list.html', context)

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