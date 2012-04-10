# coding: utf-8
import re
import csv
import markdown
from django.template.defaultfilters import safe, linebreaks
from django.utils.encoding import smart_unicode, smart_str

class SnippetMeta(type):
    def __new__(cls, name, bases, dct):
        if name != 'SnippetBase':
            for attr_name in ['format_name', 'format_data_type']:
                if dct.get(attr_name) is None:
                    raise ValueError('Class `%s` set value `%s`' % (name, attr_name))
        return type.__new__(cls, name, bases, dct)

class SnippetBase(object):
    __metaclass__ = SnippetMeta
    format_name = None
    format_data_type = None

    def __init__(self, context_name, title=None, content=None):
        self.context_name = context_name
        self.title = title or ''
        self.raw_content = content or ''
        self.content = self.make_content(content or '')

    def __unicode__(self):
        return smart_unicode(self.content)

    def __str__(self):
        return smart_str(self.content)

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self.context_name)

    def make_content(self, content):
        raise NotImplementedError('Not found method `make_content`')


class StringSnippet(SnippetBase):
    format_name = u'Строка'
    format_data_type = 'str'

    def make_content(self, content):
        return re.sub(r'[\r\n\t]+', '', content)


class TextSnippet(SnippetBase):
    format_name = u"Текст"
    format_data_type = 'text'

    def make_content(self, content):
        return safe(linebreaks(content))


class HTMLSnippet(SnippetBase):
    format_name = u"HTML"
    format_data_type = 'html'

    def make_content(self, content):
        return safe(content)


class CSVSnippet(SnippetBase):
    format_name = 'CSV'
    format_data_type = 'csv'

    def __unicode__(self):
        return smart_unicode(self.title)

    def __str__(self):
        return smart_str(self.title)

    def make_content(self, content):
        row = re.split(r'[\r\n]{1,2}', content)
        row = map(lambda s: s.strip().encode('utf-8'), row)
        row = filter(lambda s: bool(s), row)
        return list(csv.reader(row, escapechar='\\'))


class MarkdownSnippet(SnippetBase):
    format_name = 'Markdown'
    format_data_type = 'mrkd'

    def make_content(self, content):
        return markdown.markdown(content)