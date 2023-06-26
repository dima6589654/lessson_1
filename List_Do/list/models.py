from django.db import models


class List_do(models.Model):
    comment = models.CharField(max_length=120)

    sender = models.ForeignKey(
        on_delete=models.CASCADE,
        related_name="sender"
    )

    receiver = models.ForeignKey(
        on_delete=models.CASCADE,
        related_name="receiver"
    )
