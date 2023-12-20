from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Contestant
from hexdle.models import Contestant

class CustomerInline(admin.StackedInline):
    model = Contestant
    can_delete = False
    verbose_name_plural = 'contestants'

class UserAdmin(BaseUserAdmin):
    inlines = (CustomerInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Contestant)
class AuthorAdmin(admin.ModelAdmin):
    pass
