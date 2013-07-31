from django.contrib import admin
from schools.models import School, PointCategory, Term

admin.site.register(School)
admin.site.register(PointCategory)
admin.site.register(Term)