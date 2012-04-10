# coding: utf-8
import sys
from django.utils.datastructures import SortedDict
from snippets.conf.defaults import SNIPPETS, PREFIX
    
class SnippetFactory(object):
    def __init__(self, snippets=None, name_prefix=None):
        if not snippets:
            raise ValueError
        self._formats = SortedDict()
        for path_import in snippets:
            cls = self.import_snippet_cls(path_import)
            if not cls:
                raise ValueError('Can not import `%s`' % path_import)
            if cls.format_data_type in self._formats:
                raise ValueError('This type of format already exists `%s`' % cls.format_data_type)
            self._formats[cls.format_data_type] = cls
        self.name_prefix = name_prefix

    def import_snippet_cls(self, path_import):
        if not '.' in path_import:
            raise ValueError('Invalid path import class `%s`' % path_import)
        cls_name = path_import.split('.')[-1]
        module_path = '.'.join(path_import.split('.')[:-1])
        __import__(module_path)
        module = sys.modules[module_path]
        return getattr(module, cls_name, None)

    def get_snippet_cls(self, data_type=None):
        data_type = data_type or 'str'
        cls = self._formats.get(data_type)
        if cls is None:
            raise ValueError('`%r` not found snippet `%s`' % (self, data_type))
        return cls

    def get_snippet(self, data_type, name, title, content):
        cls = self.get_snippet_cls(data_type)
        snippet = cls(name, title, content)
        snippet.context_name = self.get_context_name(name)
        return snippet

    def get_snippet_for_obj(self, obj):
        return self.get_snippet(obj.data_type, obj.slug, obj.title, obj.content)

    def get_model_choices(self):
        return tuple([(t, f.format_name) for t, f in self._formats.items()])

    def get_context_name(self, name):
        if self.name_prefix:
            name = self.name_prefix + name
        return name

snippet_factory = SnippetFactory(snippets=SNIPPETS, name_prefix=PREFIX)