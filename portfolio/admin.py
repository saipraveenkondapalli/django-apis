from django.contrib import admin
from django.utils.html import format_html

from .models import Contact, Site, Resume, JobApplication


@admin.register(Site)
class Admin(admin.ModelAdmin):
    list_display = ['name', 'url', 'client_id', 'user']
    search_fields = ['name', 'url', 'client_id', 'user__username', 'user__email']
    search_help_text = "Search by name, url, username, user email or client_id"


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
    search_help_text = "Search by name,  site, email, or key"
    list_filter = ['site']
    list_per_page = 20

    def open_resume(self, obj):
        return format_html(f'<a style="color:skyblue" href="{obj.url}" target="_blank">Open Resume</a>')

    open_resume.short_description = 'URL'


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'open_resume', 'message_id', 'created_at']
    search_fields = ['title', 'company', 'resume__name']
    search_help_text = "Search by title, company, or resume"
    list_filter = ['resume']
    list_per_page = 20
    list_select_related = ['resume']
    list_display_links = ['title']

    def open_resume(self, obj):
        return format_html(f'<a style="color:skyblue" href="{obj.resume.url}" target="_blank">Open Resume</a>')

    open_resume.short_description = 'Resume'
