from django.contrib.auth.models import User
from django.db import models


class AdvUser(models.Model):
    is_activated = models.BooleanField(
        default=True
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )


class Spare(models.Model):
    name = models.CharField(max_length=30)


class Machine(models.Model):
    name = models.CharField(max_length=30)
    spares = models.ManyToManyField(Spare)


class Rubric(models.Model):
    name = models.CharField(
        max_length=20,
        db_index=True,
        verbose_name="Название", )

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        # return "/bboard/%s/"%self.pk
        # return f"/bboard/{self.pk}/"
        return f"/{self.pk}/"

    class Meta:
        verbose_name = 'Рубрика'
        verbose_name_plural = 'Рубрики'
        ordering = ['name']


class Bb(models.Model):
    rubric = models.ForeignKey(
        'Rubric',
        null=True,
        on_delete=models.PROTECT,
        verbose_name='Рубрика',
    )

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

    published = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name="Опубликовано",
    )

    def __str__(self):
        return f'Объявление: {self.title}'

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ['-published',]


class Human(models.Model):
    name = models.CharField(
        max_length=50,
    )


class Child(models.Model):
    name = models.CharField(max_length=30)


class IceCream(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name="Товар",
    )
    content = models.TextField(
        null=True,
        blank=True,
        verbose_name="Описание", )


class IceCreamShop(models.Model):
    name = models.CharField(max_length=30)
    price = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Цена",)
