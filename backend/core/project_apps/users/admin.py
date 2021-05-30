from django.contrib import admin
from .models import CustomUser as User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'plan', 'is_staff', 'is_active')
