from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Sl(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name="Товар",
    )

    content = models.TextField(
        null=True,
        blank=True,
        verbose_name="Описание",
    )

    price = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Цена",
    )

    class Meta:
        abstract = True
        ordering = ['name']



class NewSl(Sl):
    title = models.CharField(max_length=80,
                             verbose_name='Скидочный тавар')
    content = models.TextField(
        null=True,
        blank=True,
        verbose_name="Описание",
    )
    price = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Цена со скидкой", )

    class Meta:
        pass
