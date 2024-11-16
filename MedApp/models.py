import uuid

from django.db import models
from django.urls import reverse
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

    class Weekdays(models.IntegerChoices):
        MONDAY = 0, _("Monday")
        TUESDAY = 1, _("Tuesday")
        WEDNESDAY = 2, _("Wednesday")
        THURSDAY = 3, _("Thursday")
        FRIDAY = 4, _("Friday")
        SATURDAY = 5, _("Saturday")
        SUNDAY = 6, _("Sunday")

    def __str__(self):
        return f"{self.name}"
    
    def get_absolute_url(self):
        return reverse("detail-medication", kwargs={"pk": self.pk})
    

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
    day = models.IntegerField(
        choices=Weekdays.choices,
        default=0,
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

    def __str__(self):
        return f"{self.date} : {self.health}"
    

    date = models.DateTimeField(
        default=now
    )
    health = models.IntegerField()