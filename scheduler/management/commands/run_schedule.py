#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@created: 15.04.21
@author: felix
"""
import datetime
import importlib

from django.core.management.base import BaseCommand

from scheduler.models import ScheduleCommander
from scheduler.models import ScheduleResult


def get_current_time() -> datetime:
    return datetime.datetime.now()


def run_scheduled_jobs():
    current_objs = ScheduleCommander.objects.filter(earliest_execution_date__lte=get_current_time())
    for obj in current_objs:
        func__module__ = obj.module
        func__name__ = obj.func
        module = importlib.import_module(func__module__)
        try:
            func_result = getattr(module, func__name__,)()
        except Exception as err:
            ScheduleResult.objects.create(result={"success": False, "result": err.args})
        else:
            ScheduleResult.objects.create(result={"success": True, "result": func_result})
        obj.delete()

    earliest_next_job = ScheduleCommander.objects.filter(earliest_execution_date__gte=datetime.datetime.now()
                                                         ).order_by('earliest_execution_date').first()
    if earliest_next_job:
        print(int(earliest_next_job.earliest_execution_date.timestamp()))
    else:
        # the script will now sleep for 10min
        print(int((datetime.datetime.now() + datetime.timedelta(minutes=10)).timestamp()))


class Command(BaseCommand):
    help = 'Runs schedules if there are ones'

    def handle(self, *args, **options):
        run_scheduled_jobs()
