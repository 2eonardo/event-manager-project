from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import SignupForm

class CustomUserAdmin(UserAdmin):
    model = CustomUser

    add_form = SignupForm

    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_staff']

    fieldsets = UserAdmin.fieldsets + (
        ('Informazioni Ruolo e Bio', {'fields': ('role', 'bio')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name','password1', 'password2', 'role', 'bio'),
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)