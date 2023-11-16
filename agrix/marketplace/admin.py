from django.contrib import admin
from .models import Category, Product, ProductImages, CartOrder, CartOrderItems, Wishlist, Address
from .forms import ProductAdminForm, ProductImagesAdminForm

class ProductImagesAdmin(admin.TabularInline):
    def get_form(self, request, obj=None, **kwargs):
        if obj is None:  # If it's a new object (adding), set the vendor based on the logged-in user's vendor
            defaults = {
                'form': ProductImagesAdminForm,
            }
            kwargs.update(defaults)
        return super().get_form(request, obj, **kwargs)
    
    model = ProductImages


class ProductAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        if obj is None:  # If it's a new object (adding), set the vendor based on the logged-in user's vendor
            defaults = {
                'form': ProductAdminForm,
            }
            kwargs.update(defaults)
        return super().get_form(request, obj, **kwargs)

    def vendor_callback(self, db_field, **kwargs):
        if db_field.name == 'vendor':
            kwargs['initial'] = self.request.user.customuser.vendor
            kwargs['widget'].attrs['readonly'] = True  # Make the field read-only
        return db_field.formfield(**kwargs)
    
    inlines = [ProductImagesAdmin]
    list_display = ('title', 'product_image', 'category','vendor', 'price', 'featured', 'product_status', 'date')
    list_filter = ['category', 'date', 'featured', 'product_status']
    search_fields = ['title', 'category']
    list_editable = ['featured', 'product_status']
    list_per_page = 10
    
    class Meta:
        model = Product

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'category_image')
    list_filter = ['title']
    search_fields = ['title']
    list_per_page = 10
    
    class Meta:
        model = Category
        
class CartOrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'price', 'paid_status', 'order_date', 'product_status')
    list_filter = ['paid_status', 'order_date', 'product_status']
    search_fields = ['user', 'price']
    list_editable = ['paid_status', 'product_status']
    list_per_page = 10
    
    class Meta:
        model = CartOrder
        
class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display = ('order', 'invoice_no', 'item', 'image', 'qty', 'Price', 'total')
    list_filter = ['order', 'invoice_no', 'item', 'Price', 'total']
    search_fields = ['order', 'invoice_no', 'item', 'Price', 'total']
    list_per_page = 10
    
    class Meta:
        model = CartOrderItems

class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'date')
    list_filter = ['date']
    search_fields = ['user', 'product']
    list_per_page = 10
    
    class Meta:
        model = Wishlist                                

class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'status')
    list_filter = ['user', 'status']
    search_fields = ['user', 'status']
    list_per_page = 10
    
    class Meta:
        model = Address


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(CartOrderItems, CartOrderItemsAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Address, AddressAdmin)
        