from django.contrib import admin

from users.models import User

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = [
        "email",
        "first_name",
        "last_name",
        "age",
        "is_staff",
        "is_superuser",
    ]


admin.site.register(User, UserAdmin)
