from datetime import datetime, timedelta
from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .calendar import MedicationCalendar
from .forms import MedicationForm, PerceptionForm
from .models import Medication, Perception

# Create your views here.

def index(request):

    return redirect(calendar_month)

    #return render(request, "index.html", context)


def calendar_month(request, year=datetime.now().year, month=datetime.now().month):

    cal = MedicationCalendar()
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

def render_to_pdf(template, context={}):
    template = get_template(template)
    html = template.render(context)
    result = BytesIO()
    return HttpResponse(result.getvalue(), content_type='application/pdf')
    # pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    # if not pdf.err:
    #     return HttpResponse(result.getvalue(), content_type='application/pdf')
    # return None

def export(request):
    
    context = { "user": request.user }
    pdf = render_to_pdf("calendar.html", context)
    return HttpResponse(pdf, content_type='application/pdf')

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