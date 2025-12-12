from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, MemberProfile

class MemberProfileInline(admin.StackedInline):
    model = MemberProfile
    can_delete = False
    verbose_name_plural = 'Member Profile'

class CustomUserAdmin(UserAdmin):
    inlines = (MemberProfileInline,)
    list_display = ('username', 'email', 'is_staff', 'is_member', 'is_student')
    list_filter = ('is_staff', 'is_superuser', 'is_member', 'is_student', 'groups')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_member', 'is_student')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
