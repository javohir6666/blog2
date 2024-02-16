from django.contrib import admin
from .models import Category, News, Tag

admin.site.register(Category)
admin.site.register(Tag)

class AdminNews(admin.ModelAdmin):
    list_display=('title', 'category', 'add_time')
admin.site.register(News, AdminNews)
