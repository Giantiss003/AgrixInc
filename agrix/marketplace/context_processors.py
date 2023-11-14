from marketplace.models import Category, Product, CartOrder, CartOrderItems, Wishlist, Address

def default(request):
    categories = Category.objects.all()
    return {
        'categories': categories,
    }