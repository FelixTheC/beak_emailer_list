from django.contrib import admin

from scheduler.models import ScheduleCommander
from scheduler.models import ScheduleResult


@admin.register(ScheduleCommander)
class ScheduleCommanderAdminModel(admin.ModelAdmin):
    list_display = ('module', 'func', 'earliest_execution_date')
    list_filter = ('module', 'func')
    search_fields = ('module__icontains', 'func__icontains')


@admin.register(ScheduleResult)
class ScheduleResultAdminModel(admin.ModelAdmin):
    list_display = ('created_at', 'result')
    list_filter = ('result', )
