from django.contrib import admin

from .models import Contact, Site


@admin.register(Site)
class Admin(admin.ModelAdmin):
    list_display = ['name', 'url', 'client_id']
    search_fields = ['name', 'url', 'client_id']
    search_help_text = "Search by name, url, or client_id"


@admin.register(Contact)
class Admin(admin.ModelAdmin):
    list_display = ['name', 'email', 'site', 'created_at']
    search_fields = ['name', 'email', 'site']
    search_help_text = "Search by name, email, or site"
    list_filter = ['site']
    list_per_page = 10
    list_select_related = ['site']
    list_display_links = ['name']
    list_editable = ['email']
