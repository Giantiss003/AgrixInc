# forms.py
from django import forms
from .models import Product, ProductImages

class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('user',)  # Exclude the 'user' field from the form

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # Retrieve the request object from kwargs
        super().__init__(*args, **kwargs)

        if not self.instance.pk and self.request:  # If it's a new object and request exists
            self.instance.user = self.request.user.customuser  # Set the user field in the instance
            self.fields['vendor'].initial = self.request.user.customuser.vendor
            self.fields['vendor'].widget.attrs['readonly'] = True  # Make the field read-only

class ProductImagesAdminForm(forms.ModelForm):
    class Meta:
        model = ProductImages
        exclude = ('user',) # Exclude the 'user' field from the form
        
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
        if not self.instance.pk and self.request:# If it's a new object and request exists
            self.instance.user = self.request.user.customuser # Set the user field in the instance
            self.fields['product'].initial = self.request.user.customuser.vendor
            self.fields['product'].widget.attrs['readonly'] = True # Make the field read-only    