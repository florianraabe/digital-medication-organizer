from calendar import HTMLCalendar
from datetime import datetime

from django.db.models import Q, F
from django.template.loader import render_to_string

from .forms import CalendarDayForm
from .models import CalendarDay, Medication


class MedicationCalendar(HTMLCalendar):
    def __init__(self, token, events=None):
        super(MedicationCalendar, self).__init__()
        self.events = events
        self.month = None
        self.year = None
        self.token = token

    def formatday(self, day, weekday, events):
        """
        Return a day as a table cell.
        """

        if day == 0:
            return '<td class="noday">&nbsp;</td>'  # day outside month
        else:
            date = datetime(self.year, self.month, day=day)
            calendar_day = CalendarDay.objects.filter(date=date).first()
            taken_part = False
            taken_all = False
            if calendar_day == None:
                form = CalendarDayForm(date)
            else:
                form = CalendarDayForm(date, instance=calendar_day)
                taken_part = True
                taken_all = set(events.filter(days__number=weekday)) == set(calendar_day.medication.all())

            f1 = Q( days__number=weekday )
            f_enddate_is_none = Q( enddate__isnull = True )
            f_enddate_is_not_none = Q( enddate__gt=date.date() )

            medication = events.filter( f1 & ( f_enddate_is_none | f_enddate_is_not_none ) )

            variables = {
                "weekday": self.cssclasses[weekday],
                "day": day,
                "date": date,
                "today": date.date() == datetime.now().date(),
                "medication": medication,
                "form": form,
                "token": self.token,
                "taken_part": taken_part,
                "taken_all": taken_all,
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