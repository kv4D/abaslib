"""For 'users' app's models registration"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . models import User


class ModifiedUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Profile info and stats', {
            'fields': (
                'user_avatar',
                'titles_read_amount',
                'favorite_text_titles',
                'favorite_graphic_titles'
                ),
        }),
    )
    filter_horizontal = ('favorite_text_titles', 'favorite_graphic_titles')

# Register your models here.
admin.site.register(User, ModifiedUserAdmin)
