from django.contrib import admin
from django.utils.html import format_html

from .models import Contact, Site, Resume


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


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['name', 'site', 'key', 'open_resume']
    search_fields = ['name', 'site__user__email', 'key']
    search_help_text = "Search by name, site, email, or key"
    list_filter = ['site']
    list_per_page = 20

    def open_resume(self, obj):
        return format_html(f'<a style="color:skyblue" href="{obj.url}" target="_blank">Open Resume</a>')

    open_resume.short_description = 'URL'
