from django.contrib.auth.models import User
from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from precise_bbcode.fields import BBCodeTextField
from datetime import datetime
from os.path import splitext


def get_min_length():
    min_length = 3
    return min_length


def validate_even(val):
    if val % 2 != 0:
        raise ValidationError('Число %(value)s нечётное', code='odd',
                              params={'value': val})


def get_timestamp_path(instance, filename):
    return '%s%s%s' % (splitext(filename)[0],
                       datetime.now().timestamp(),
                       splitext(filename)[1])


class RubricQuerySet(models.QuerySet):
    def order_by_bb_count(self):
        return self.annotate(cnt=models.Count('bb')).order_by('-cnt')


class RubricManager(models.Manager):
    def get_queryset(self):
        # return super().get_queryset().order_by('name')
        return RubricQuerySet(self.model, using=self._db)

    def order_by_bb_count(self):
        # return super().get_queryset().annotate(
        #     cnt=models.Count('bb')).order_by('-cnt')
        return self.get_queryset().order_by_bb_count()


class BbManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('price')


class Rubric(models.Model):
    name = models.CharField(
        max_length=20,
        db_index=True,
        verbose_name="Название",
    )

    objects = RubricManager()

    # bbs = RubricManager()

    # objects = models.Manager()
    # bbs = RubricManager()

    # objects = RubricQuerySet.as_manager()
    # objects = models.Manager.from_queryset(RubricQuerySet)()

    def __str__(self):
        return self.name

    # def save(self, *args, **kwargs):
    #     # Выполняем какие-то действия до сохранения
    #     if True:
    #         super().save(*args, **kwargs)
    #     # Выполняем какие-то действия после сохранения
    #
    # def delete(self, *args, **kwargs):
    #     # Выполняем какие-то действия до удаления
    #     if True:
    #         super().delete(*args, **kwargs)
    #     # Выполняем какие-то действия после удаления

    def get_absolute_url(self):
        # return "/bboard/%s/" % self.pk
        # return f"/bboard/{self.pk}/"
        return f"/{self.pk}/"

    class Meta:
        verbose_name = 'Рубрика'
        verbose_name_plural = 'Рубрики'
        ordering = ['name']


class Bb(models.Model):
    KINDS = (
        ('b', 'Куплю'),
        ('s', 'Продам'),
        ('c', 'Поменяю')
    )

    rubric = models.ForeignKey(
        'Rubric',
        null=True,
        on_delete=models.PROTECT,
        verbose_name='Рубрика',
    )

    title = models.CharField(
        max_length=50,
        verbose_name="Товар",
        validators=[validators.MinLengthValidator(get_min_length)],
        # validators=[validators.RegexValidator(regex='^.{4,}$',
        # inverse_match=True)]
        # validators=[validators.ProhibitNullCharactersValidator()]  # \x00
        error_messages={'min_length': 'Слишком мало символов'},
    )

    kind = models.CharField(
        max_length=1,
        choices=KINDS,
        default='s'
    )

    # content = models.TextField(
    content = BBCodeTextField(
        null=True,
        blank=True,
        verbose_name="Описание",
    )

    price = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Цена",
        # validators=[validate_even]  # , MinMaxValueValidator(50, 60_000_000)]
    )

    published = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name="Опубликовано",
    )

    archive = models.FileField(
        # upload_to='archive/',
        blank=True,
        upload_to=get_timestamp_path),

    objects = models.Manager()
    by_price = BbManager()

    def __str__(self):
        return f'Объявление: {self.title}'

    def title_and_price(self):
        if self.price:
            # return '%s (%.2f)' % (self.title, self.price)
            return f'{self.title} ({self.price:.2f})'
        return self.title

    class Meta:
        # order_with_respect_to = 'rubric'
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ['-published', 'title']
