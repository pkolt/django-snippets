from django.conf import settings

DEFAULT_PREFIX = 'snippet_'
DEFAULT_SNIPPETS = (
    'snippets.container.StringSnippet',
    'snippets.container.TextSnippet',
    'snippets.container.HTMLSnippet',
    'snippets.container.CSVSnippet',
    'snippets.container.MarkdownSnippet',
)

SNIPPETS = getattr(settings, 'SNIPPETS', DEFAULT_SNIPPETS)
PREFIX = getattr(settings, 'SNIPPETS_PREFIX', DEFAULT_PREFIX)