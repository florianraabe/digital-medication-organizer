import uuid

from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Medication(models.Model):
    class Meta:
        unique_together = [['name']]
        ordering = ["name"]
        verbose_name = "Medication"
        verbose_name_plural = "Medication"

    class Type(models.IntegerChoices):
        PILL = 1, _("Pill")
        LIQUID = 2, _("Liquid")

    class Weekdays(models.TextChoices):
        MONDAY = 'MO', _("Monday")
        TUESDAY = 'TU', _("Tuesday")
        WEDNESDAY = 'WE', _("Wednesday")
        THURSDAY = 'TH', _("Thursday")
        FRIDAY = 'FR', _("Friday")
        SATURDAY = 'SA', _("Saturday")
        SUNDAY = 'SU', _("Sunday")

    def __str__(self):
        return f"{self.name}"

    name = models.CharField(
        max_length=64,
        verbose_name="Name",
    )
    type = models.IntegerField(
        choices=Type.choices,
        default=1,
    )
    amount = models.IntegerField(
        verbose_name="Amount of pills",
    )
    dosage = models.IntegerField(
        verbose_name="Dosage",
    )
    day = models.CharField(
        choices=Weekdays.choices,
        max_length=2,
        default="MO",
    )
    interval = models.DurationField(
        verbose_name="Interval"
    )


class Perception(models.Model):
    class Meta:
        #unique_together = [[]]
        ordering = []
        verbose_name = "Perception"
        verbose_name_plural = "Perceptions"

    date = models.DateTimeField(
        default=now
    )
    health = models.IntegerField()