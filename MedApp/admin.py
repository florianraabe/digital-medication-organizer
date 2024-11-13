from django.apps import apps
from django.contrib import admin

# Register your models here.

app = apps.get_app_config('MedApp').get_models()

for model in app:
    admin.site.register(model)
