from django.contrib import admin

from .models import Template, BotUser, CashLink, Preview


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ['title', 'body']


@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ['chat_id', 'is_active']

@admin.register(CashLink)
class CashLinkAdmin(admin.ModelAdmin):
    list_display = ['url', 'title']

@admin.register(Preview)
class PreviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'text']
