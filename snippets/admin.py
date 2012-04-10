# coding: utf-8
from django.contrib import admin
from snippets.models import Snippet, SnippetGroup
from snippets.factory import snippet_factory

class SnippetAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'slug', 'data_type', 'publish', 'display_context_varname', 'display_bbcode']
    list_filter = ['data_type', 'snippet_groups']
    search_fields = ['title', 'slug']

    def display_context_varname(self, obj):
        context_name = snippet_factory.get_context_name(obj.slug)
        return '{{ %s }}' % context_name
    display_context_varname.short_description = u"В шаблоне"

    def display_bbcode(self, obj):
        return '[snippet %s]' % obj.slug
    display_bbcode.short_description = 'BBcode'

class SnippetGroupAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'slug']
    search_fields = ['title', 'slug']

admin.site.register(Snippet, SnippetAdmin)
admin.site.register(SnippetGroup, SnippetGroupAdmin)