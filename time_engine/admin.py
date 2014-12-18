from django.contrib import admin
from time_engine.models import Plan, PlanResult

class ChoiceInline(admin.StackedInline):
    model = PlanResult
    extra = 3

class PlanAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Basic information',               {'fields': ['name', 'user', 'lesson_count'],'classes': ['collapse']}),
        ('Date information', {'fields': ['start_date', 'end_date'],'classes': ['collapse']}),
        ('Available days',   {'fields': ['has_saturday', 'has_monday', 'has_tuesday', 'has_wednesday', 'has_thursday', 'has_friday', 'has_sunday'], 'classes': ['collapse']})
    ]
    inlines = [ChoiceInline]




# class PlanResultAdmin(admin.ModelAdmin):
#     fieldsets = [
#         (None, {'fields': ['plan', 'lesson_no', 'lesson_date']})
#     ]
#     list_display = ('plan', 'lesson_no', 'lesson_date')

admin.site.register(Plan, PlanAdmin)
#admin.site.register(PlanResult)