import os
from datetime import datetime, timedelta
from io import BytesIO

from django.conf import settings
from django.http import HttpResponse
from django.middleware.csrf import get_token
from django.shortcuts import redirect, render
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from xhtml2pdf import pisa

from .calendar import MedicationCalendar
from .forms import CalendarDayForm, MedicationForm, PerceptionForm
from .models import CalendarDay, Medication, Perception

# Create your views here.


def track_mouse(request, time, click, x, y, w, h, src):
    print(time, click, x, y, w, h, src)

    with open("tracking.csv", "a") as fd:
        fd.write(f"{time},{click},{x},{y},{w},{h},{src}\n")

    return HttpResponse("a", content_type='image/jpeg')


def index(request):

    return redirect(calendar_month)

    #return render(request, "index.html", context)


def calendar_month(request, year=datetime.now().year, month=datetime.now().month):

    cal = MedicationCalendar(get_token(request))
    html_calendar = cal.formatmonth(year, month, withyear=True)
    date = datetime(year=year, month=month, day=1)

    context = {
        "user": request.user,
        "calendar": html_calendar,
        "month": date,
        "previous": date - timedelta(days=1),
        "next": date + timedelta(days=31),
    }

    return render(request, "calendar.html", context)


def export(request):

    context = {
        "user": request.user,
        "today": datetime.now(),
        "medication": Medication.objects.all(),
        "days": CalendarDay.objects.all(),
        "perceptions": Perception.objects.all(),
    }

    template = get_template("export.html")
    html = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def mark_calendar_day(request, year, month, day):
    
    if request.method == "POST":
        date = datetime(year=year, month=month, day=day)
        calendar_day = CalendarDay.objects.filter(date=date).first()
        if calendar_day == None:
            form = CalendarDayForm(date, request.POST)
        else:
            form = CalendarDayForm(date, request.POST, instance=calendar_day)
        if form.is_valid():
            calendar_day = form.save()
            for med in calendar_day.medication.all():
                if med.amount < med.dosage:
                    med.amount = 0
                else:
                    med.amount -= med.dosage
                med.save()

    return redirect(calendar_month)
    

### Medication ###

class MedicationListView(ListView):
    model = Medication
    template_name = 'medication.html'


class MedicationDetailView(DetailView):
    model = Medication
    template_name = 'medication.html'


class MedicationCreateView(CreateView):
    model = Medication
    form_class = MedicationForm
    template_name = 'form.html'
  
    def get_success_url(self):
        return reverse_lazy("medication")


class MedicationUpdateView(UpdateView): 
    model = Medication
    form_class = MedicationForm
    template_name = 'form.html'
    slug_url_kwarg = 'pk'

    def get_success_url(self):
        return reverse_lazy("medication")


class MedicationDeleteView(DeleteView):
    model = Medication
    template_name = "form.html"

    def get_success_url(self):
        return reverse_lazy("medication")


### Perception ###

class PerceptionListView(ListView):
    model = Perception
    template_name = 'perception.html'

class PerceptionCreateView(CreateView):
    model = Perception
    form_class = PerceptionForm
    template_name = 'perception-form.html'
  
    def get_success_url(self):
        return reverse_lazy("perception")