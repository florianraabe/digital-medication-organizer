from calendar import HTMLCalendar
from datetime import datetime

from django.template.loader import render_to_string

from .models import Medication


class MedicationCalendar(HTMLCalendar):
    def __init__(self, events=None):
        super(MedicationCalendar, self).__init__()
        self.events = events
        self.month = None
        self.year = None

    def formatday(self, day, weekday, events):
        """
        Return a day as a table cell.
        """

        if day == 0:
            return '<td class="noday">&nbsp;</td>'  # day outside month
        else:
            date = datetime(self.year, self.month, day=day)
            variables = {
                "weekday": self.cssclasses[weekday],
                "day": day,
                "date": date,
                "today": date.date() == datetime.now().date(),
                "medication": events.filter(day=weekday)
            }
            template = render_to_string("calendar-day.html", variables)
            return template

    def formatweek(self, theweek, events):
        """
        Return a complete week as a table row.
        """
        s = ''.join(self.formatday(d, wd, events) for (d, wd) in theweek)
        return '<tr>%s</tr>' % s
 
    def formatmonth(self, theyear, themonth, withyear=True):
        """
        Return a formatted month as a table.
        """
 
        events = Medication.objects.all()
        self.month = themonth
        self.year = theyear
 
        v = []
        a = v.append
        a('<table class="table table-borderless month">')
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week, events))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)