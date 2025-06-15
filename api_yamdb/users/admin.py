from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

UserAdmin.fieldsets += (
    ('Роли', {'fields': ('role',)}),
    ('Биография', {'fields': ('bio',)}),
)
UserAdmin.list_editable += (
    'role',
)
UserAdmin.list_display += (
    'role',
)

admin.site.register(User, UserAdmin)
