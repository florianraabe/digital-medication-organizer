import uuid

from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from django.core.validators import MinValueValidator

# Create your models here.

class Weekdays(models.Model):
    class Meta:
        unique_together = [['number']]
        ordering = ["number"]
        verbose_name = "Weekday"
        verbose_name_plural = "Weekdays"

    def __str__(self):
        return f"{self.name}"

    name = models.CharField(
        max_length=64,
        verbose_name="Name",
    )
    number = models.IntegerField()


class DosingTime(models.Model):
    class Meta:
        unique_together = [['time']]
        ordering = ["time"]
        verbose_name = "Dosing Time"
        verbose_name_plural = "Dosing Times"

    def __str__(self):
        return f"{self.name}"

    name = models.CharField(
        max_length=64,
        verbose_name="Name",
    )
    time = models.TimeField(
        verbose_name="Time"
    )


class Medication(models.Model):
    class Meta:
        unique_together = [['name']]
        ordering = ["-creation_date"]
        verbose_name = "Medication"
        verbose_name_plural = "Medication"

    class Type(models.IntegerChoices):
        PILL = 1, _("Pill")
        LIQUID = 2, _("ml")

    def __str__(self):
        name = f"{self.name}: {self.dosage} {self.get_type_display()}" + ("s" if self.dosage > 1 and self.type == 1 else "")
        name += f" - {self.get_times()}"
        return name
    
    def get_times(self):
        return ", ".join([str(t) for t in self.time.all()])
    
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
        validators=[MinValueValidator(0)],
        verbose_name="Amount of pills in stock",
    )
    dosage = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name="Dosage to take",
    )
    days = models.ManyToManyField(
        Weekdays,
        verbose_name=_("Weekdays"),
    )
    time = models.ManyToManyField(
        DosingTime,
        verbose_name=_("Dosing Times"),
    )
    enddate = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Date until the medication needs to be taken"),
    )
    creation_date = models.DateTimeField(
        default=now,
    )


class CalendarDay(models.Model):
    class Meta:
        unique_together = [['date']]
        ordering = ["date"]
        verbose_name = "Calendar Day"
        verbose_name_plural = "Calendar Days"

    def __str__(self):
        return f"{self.date}"

    date = models.DateField(
        default=now,
    )
    medication = models.ManyToManyField(
        Medication,
        verbose_name="Medication",
        blank=True,
    )


class Perception(models.Model):
    class Meta:
        ordering = ["-date"]
        verbose_name = "Perception"
        verbose_name_plural = "Perceptions"

    def __str__(self):
        return f"{self.date} : {self.health}"
    

    date = models.DateTimeField(
        default=now
    )
    health = models.IntegerField()