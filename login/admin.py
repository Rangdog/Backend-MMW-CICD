from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'is_superuser']
    fieldsets = (
        (None, {'fields': ('username', 'password', 'is_active', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_active', 'is_superuser'),
        }),
    )
    search_fields = ('username',)
    ordering = ('username',)

    # Loại bỏ trường is_staff ra khỏi list_filter
    list_filter = ['is_active', 'is_superuser']

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if not obj:
            fieldsets[0][1]['fields'] = tuple(
                field for field in fieldsets[0][1]['fields'] if field != 'is_staff')
        return fieldsets


admin.site.register(CustomUser, CustomUserAdmin)
