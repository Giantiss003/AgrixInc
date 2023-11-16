from django.urls import path
from . import views

app_name = 'marketplace'

urlpatterns = [
    path('', views.marketplace, name='marketplace'),
    path('products/', views.product_list, name='products'),
    path('products/<pid>/', views.product_detail, name='product-detail'),
    path('category/', views.category_list, name='category'),
    path('category/<cid>/', views.category_product_list, name='category-product-list'),
]