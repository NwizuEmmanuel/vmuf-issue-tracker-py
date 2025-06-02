from django.contrib import admin
from .models import Building,Professional,Issue, Department
# Register your models here.

admin.site.register(Building)
admin.site.register(Professional)
admin.site.register(Issue)
admin.site.register(Department)
