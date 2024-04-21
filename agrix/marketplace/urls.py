from django.urls import path
from . import views

app_name = 'marketplace'

urlpatterns = [
    path('', views.marketplace, name='marketplace'),
    # path('products/', views.product_list, name='products'),
    path('products/<pid>/', views.product_detail, name='product-detail'),
    path('products/tag/<slug:tag_slug>/', views.tag_list, name='tags'),
    path('category/', views.category_list, name='category'),
    path('category/<cid>/', views.category_product_list, name='category-product-list'),
    #Search
    path('search/', views.search, name='search'),
    #cart
    path('cart/', views.cart, name='cart'),
    # Add to Cart
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    # Increase cart
    path('increase-quantity/', views.increase_cart_quantity, name='increase-quantity'),
    # Decrease cart
    path('decrease-quantity/', views.decrease_cart_quantity, name='decrease-quantity'),
    # Delete from cart
    path('delete-from-cart/', views.delete_from_cart, name='delete-from-cart'),
    # TODO : ROUTE fILTERING
    # path('marketplace/products/filter-product/', views.filter_product, name='filter-product'),
]