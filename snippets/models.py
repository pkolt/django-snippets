# coding: utf-8
from django.db import models
from snippets.factory import snippet_factory

SLUG_HELP_TEXT = u"Имя которое будет присвоено переменной в контексте шаблона"

class SnippetManager(models.Manager):
    def get_query_set(self):
        return super(SnippetManager, self).get_query_set().filter(publish=True)


class SnippetGroup(models.Model):
    name = models.CharField(u"Название группы", max_length=200)
    slug = models.SlugField(u"Кодовое имя", unique=True, db_index=True, help_text=SLUG_HELP_TEXT)
    objects = models.Manager()
    objects_pub = SnippetManager()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"Группа сниппетов"
        verbose_name_plural = u"Группы сниппетов"


class Snippet(models.Model):
    DATA_TYPE_CHOICES = snippet_factory.get_model_choices()

    publish = models.BooleanField(u"Опубликовать", default=True)
    name = models.CharField(u"Название", max_length=200)
    slug = models.SlugField(u"Кодовое имя", unique=True, db_index=True, help_text=SLUG_HELP_TEXT)
    data_type = models.CharField(u"Тип данных", choices=DATA_TYPE_CHOICES, max_length=4, default='str')
    title = models.CharField(u"Заголовок", max_length=250, blank=True)
    content = models.TextField(u"Контент", blank=True)
    snippet_groups = models.ManyToManyField(SnippetGroup, verbose_name=u"Группа сниппетов", blank=True, null=True)
    objects = models.Manager()
    objects_pub = SnippetManager()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"Сниппет"
        verbose_name_plural = u"Сниппеты"