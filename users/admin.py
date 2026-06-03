from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Questo permette di vedere il campo "role" e "bio" nel pannello Admin
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ('Informazioni Ruolo', {'fields': ('role', 'bio')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)