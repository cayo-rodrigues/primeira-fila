from django.contrib import admin

from users.models import User

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "first_name", "last_name", "is_staff", "is_superuser"]


admin.site.register(User, UserAdmin)
