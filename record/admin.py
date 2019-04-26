from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Pharmacist)
admin.site.register(OnCall)
admin.site.register(Call)