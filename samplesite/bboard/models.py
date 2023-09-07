from django.contrib.auth.models import User
from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from precise_bbcode.fields import BBCodeTextField


def get_min_length():
    min_length = 3
    return min_length


def validate_even(val):
    if val % 2 != 0:
        raise ValidationError('Число %(value)s нечётное', code='odd',
                              params={'value': val})


class RubricQuerySet(models.QuerySet):
    def order_by_bb_count(self):
        return self.annotate(cnt=models.Count('bb')).order_by('-cnt')


class RubricManager(models.Manager):
    def get_queryset(self):
        return RubricQuerySet(self.model, using=self._db)
        # return super().get_queryset().order_by('name')

    def order_by_bb_count(self):
        return self.get_queryset().order_by_bb_count()
        # return super().get_queryset().annotate(cnt=models.Count('bb').order_by('-cnt'))


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
    # objects = RubricQuerySet.as_manager()
    # objects = models.Manager.from_queryset(RubricQuerySet)()

    # bbs = RubricManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
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
        error_messages={'min_length': 'Слишком мало символов'},
    )

    kind = models.CharField(
        max_length=1,
        choices=KINDS,
        default='s'
    )

    # content = models.TextField(
    content =  BBCodeTextField(
        null=True,
        blank=True,
        verbose_name="Описание",
    )

    price = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Цена",
        validators=[validate_even]
    )

    published = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name="Опубликовано",
    )
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
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ['-published', 'title']
