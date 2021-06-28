from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()


class AdvancedUserAdmin(UserAdmin):
    model = User
    list_display = list(UserAdmin.list_display) + ['can_upload']
    list_editable = ['can_upload']


admin.site.register(User, AdvancedUserAdmin)
