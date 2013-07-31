from django.contrib import admin
from goals.models import GoalCategory, Goal

admin.site.register(GoalCategory)
admin.site.register(Goal)