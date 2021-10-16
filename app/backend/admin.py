from django.contrib import admin

from .models import Template, BotUser, CashLink, Review


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ['title', 'body']


@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ['chat_id', 'is_active']


@admin.register(CashLink)
class CashLinkAdmin(admin.ModelAdmin):
    list_display = ['type', 'title', 'url']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'text']
