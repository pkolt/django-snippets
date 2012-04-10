# coding: utf-8
import re
from django import template
from snippets.models import Snippet
from snippets.factory import snippet_factory

register = template.Library()

@register.filter(name='snippet_bbcode')
def snippet_bbcode(value):
    search = re.findall(r'\[snippet (\w+)\]', value)
    if search:
        names = list(search)
        object_list = Snippet.objects.filter(publish=True, slug__in=names)
        snippet_dict = {}
        for obj in object_list:
            snippet = snippet_factory.get_snippet_for_obj(obj)
            snippet_dict[obj.slug] = snippet
        for name in names:
            bbcode = '[snippet %s]' % name
            text = unicode(snippet_dict.get(name, ''))
            value = value.replace(bbcode, text)
    return value


@register.tag(name="snippet")
def snippet_tag(parser, token):
    result = re.search(r'\w+ ([\'\"])(\w+)(?:\1)(?: as (\w+))?', token.contents)
    if not result:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
    slug, context_name = result.groups()[1:]
    return SnippetNode(slug, context_name)

class SnippetNode(template.Node):
    def __init__(self, slug, context_name):
        self.slug = slug
        self.context_name = context_name

    def get_snippet(self, slug):
        try:
            obj = Snippet.objects_pub.get(slug=slug)
        except Snippet.DoesNotExist:
            return ''
        snippet = snippet_factory.get_snippet_for_obj(obj)
        return snippet

    def render(self, context):
        snippet = self.get_snippet(self.slug)
        if self.context_name:
            context[self.context_name] = snippet
            return ''
        return snippet


@register.tag(name="snippets_group")
def snippets_group(parser, token):
    search = re.search(r'\w+ [\'\"](\w+)[\'\"](?: as (\w+))?', token.contents)
    if not search:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
    name, context_name = search.groups()
    return SnippetsGroupNode(name, context_name)

class SnippetsGroupNode(template.Node):
    def __init__(self, name, context_name):
        self.name = name
        self.context_name = context_name

    def get_snippets(self, name):
        snippets = []
        object_list = Snippet.objects_pub.filter(snippet_groups__slug=name)
        for obj in object_list:
            snippet = snippet_factory.get_snippet_for_obj(obj)
            snippets.append(snippet)
        return snippets

    def render(self, context):
        snippets = self.get_snippets(self.name)
        if self.context_name:
            context[self.context_name] = snippets
        else:
            for snippet in snippets:
                context[snippet.context_name] = snippet
        return ''