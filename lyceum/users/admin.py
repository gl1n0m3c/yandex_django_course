from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from users.models import Profile


class ProfileInline(admin.TabularInline):
    model = Profile
    can_delete = False


class ProfileAdmin(UserAdmin):
    inlines = [ProfileInline]


admin.site.unregister(User)
admin.site.register(User, ProfileAdmin)
