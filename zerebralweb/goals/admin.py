from django.contrib import admin
from goals.models import ActionPlan,GoalCategory,Goal

admin.site.register(ActionPlan)
admin.site.register(GoalCategory)
admin.site.register(Goal)