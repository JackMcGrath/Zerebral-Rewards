from django.contrib import admin
from auth.models import ZerebralUser,TeacherParentInvite,StudentInvite

admin.site.register(ZerebralUser)
admin.site.register(TeacherParentInvite)
admin.site.register(StudentInvite)