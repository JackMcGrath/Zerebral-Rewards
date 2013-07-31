from django.contrib import admin
from students.models import EnrolledStudent, Student


admin.site.register(EnrolledStudent)
admin.site.register(Student)