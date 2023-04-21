from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, OtpCode, Profile
from django.contrib.auth.models import User, Group


admin.site.unregister(Group)


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("email", "is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (None, {"fields": ("first_name", "last_name", "address")}),
        ("--", {"fields": ("is_staff", "is_active")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active"
            )}
        ),
    )
    filter_horizontal = []
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'code', 'created']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass

