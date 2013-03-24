#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup


setup(
    name="django-snippets",
    version=__import__('snippets').__version__,
    description="Snippets application for Django",
    author="Pavel Koltyshev",
    author_email="pkoltyshev@gmail.com",
    url="https://github.com/pkolt/django-snippets",
    license="BSD",
    packages=['snippets', 'snippets.conf', 'snippets.templatetags'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Languagr :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Internet :: WWW/HTTP"],
)
