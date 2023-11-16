from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'is_vendor', 'is_staff',)
    list_filter = ('email', 'username', 'is_vendor', 'is_staff',)
    search_fields = ('email', 'username', 'is_vendor', 'is_staff',)
    ordering = ('email', 'username', 'is_vendor', 'is_staff',)
    list_editable = ('is_vendor',)

admin.site.register(CustomUser, CustomUserAdmin)
