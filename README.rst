===============================
Snippets application for Django
===============================


Depending
#########

Python >= 2.6

Django >= 1.3


Installation
############

1. ``snippets`` add INSTALLED_APPS
2. Run ``python manage.py syncdb``


Settings
########

Edit settings.py::

    SNIPPETS_PREFIX = 'snippet_'

    SNIPPETS = (
        'snippets.container.StringSnippet',
        'snippets.container.TextSnippet',
        'snippets.container.HTMLSnippet',
        'snippets.container.CSVSnippet',
        'snippets.container.MarkdownSnippet',
    )


Formats
#######

* String
* Text
* HTML
* CSV
* Markdown

CSV Snippet
***********

Text::

    1, Hello world!
    2, Language: Python\, Ruby
    3, Escape use \,

In template::

    <h2>{{ snippet_language.title }}</h2>
    <ul>
    {% for num, text in snippet_language.content %}
        <li>{{ num }}) {{ text }}</li>
    {% endfor %}
    </ul>

Result::

    1) Hello world!
    2) Language: Python, Ruby
    3) Escape use ,

Templatetags
############

Load tags::

    {% load snippets_tags %}

Snippet in template context::

    {{ mysnippet.title }}
    {{ mysnippet.content }} {# or #} {{ mysnippet }}
    {{ mysnippet.raw_content }}


Snippet::

    {% snippet "copyright" %} {# show copyright #}

    {% snippet "copyright" as copyright %} {# add to context #}


Snippets group::

    {% snippets_group "phone" %} {# add to context #}
    {{ phone_jon }}, {{ phone_mark }}.


    {% snippets_group "phone" as phone_list %}
    {% for object in phone_list %}
        <li>{{ object.title }}: {{ object.content }}</li>
    {% endfor %}


Snippet use Shortcode
##################

Use the shortcode in the text ``[snippet name]``.

In the template, add a filter::

    {{ object.text|snippet_shortcode }}


Changelog
#########

16.04.2012 — Release Snippets version 0.1.4

09.04.2012 — Release Snippets version 0.1.3

07.04.2012 — Release Snippets version 0.1.2

27.03.2012 — Release Snippets version 0.1.0