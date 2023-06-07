from django.db import models
from django.contrib.auth.models import User


class AdvUser(models.Model):
    is_activated = models.BooleanField(
        default=True,
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


class SMS(models.Model):
    comment = models.CharField(max_length=120)

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sender"
    )

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="receiver"
    )
