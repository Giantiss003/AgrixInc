from allauth.account.forms import SignupForm
from django import forms
from .models import CustomUser

class CustomSignupForm(SignupForm):
    is_vendor = forms.BooleanField(required=False)

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        is_vendor = self.cleaned_data.get('is_vendor', False)
        
        if is_vendor:
            # If the checkbox for 'is_vendor' is selected, set the user as a vendor
            custom_user = CustomUser.objects.get(pk=user.pk)
            custom_user.is_vendor = True
            custom_user.save()
        
        return user
