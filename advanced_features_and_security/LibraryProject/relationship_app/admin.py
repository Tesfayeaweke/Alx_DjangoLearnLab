from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from django.contrib.auth import get_user_model 

CustomUser = get_user_model()

class CustomUserAdmin(UserAdmin):
    
    list_display = UserAdmin.list_display + ('date_of_birth', 'profile_photo',)

    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('date_of_birth', 'profile_photo',)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('date_of_birth', 'profile_photo',)}),
    )

    
try:
    admin.site.unregister(CustomUser) # Tries to unregister the default UserAdmin if it was already registered
except admin.sites.NotRegistered:
    pass # Ignore if it's not registered (e.g., on first run)

admin.site.register(CustomUser, CustomUserAdmin)

