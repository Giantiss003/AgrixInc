from django.urls import path
from .views import CustomSignupView

urlpatterns = [
    # ... other URL patterns
    path('accounts/signup/', CustomSignupView.as_view(), name='custom_signup'),
    # 'accounts/signup/' is the URL path for your custom signup view
]