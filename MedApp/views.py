from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import MedicationForm, PerceptionForm
from .models import Medication, Perception

# Create your views here.

def index(request):

    return render(request, "index.html", {})


### Medication ###

class MedicationListView(ListView):
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


# class MedicationDeleteView(DeleteView):
#     model = Medication
#     template_name = "form.html"

#     def get_success_url(self):
#         return reverse_lazy("medication")


### Perception ###

class PerceptionListView(ListView):
    model = Perception
    template_name = 'perception.html'

class PerceptionCreateView(CreateView):
    model = Perception
    form_class = PerceptionForm
    template_name = 'form.html'
  
    def get_success_url(self):
        return reverse_lazy("perception")