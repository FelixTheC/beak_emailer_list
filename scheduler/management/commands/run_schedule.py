#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@created: 15.04.21
@author: felix
"""
import datetime
import inspect
import importlib

from django.core.management.base import BaseCommand
import ujson

from scheduler.models import ScheduleCommander
from scheduler.models import ScheduleResult


def get_current_time() -> datetime:
    """
    for mocking and testing purposes
    """
    return datetime.datetime.utcnow()


def pos_only(func: callable) -> bool:
    return all(val.kind == val.POSITIONAL_ONLY
               for val in inspect.signature(func).parameters.values())


def keyword_only(func: callable) -> bool:
    return all(val.kind == val.KEYWORD_ONLY
               for val in inspect.signature(func).parameters.values())


def contains_var_args(func: callable) -> bool:
    return any(val.kind == val.VAR_POSITIONAL
               for val in inspect.signature(func).parameters.values())


def contains_var_kwargs(func: callable) -> bool:
    return any(val.kind == val.VAR_KEYWORD
               for val in inspect.signature(func).parameters.values())


def run_scheduled_jobs():
    current_objs = ScheduleCommander.objects.filter(earliest_execution_date__lte=get_current_time())
    for obj in current_objs:
        func__module__ = obj.module
        func__name__ = obj.func
        module = importlib.import_module(func__module__)
        try:
            func = getattr(module, func__name__)
            signature = inspect.signature(func)
            if len(signature.parameters) == 0:
                func_result = func()
            elif pos_only(func):
                func_result = func(*eval(obj.args))
            elif keyword_only(func):
                func_result = func(**ujson.loads(obj.kwargs))
            else:
                if contains_var_args(func) and not contains_var_kwargs(func):
                    func_result = getattr(module, func__name__)(*eval(obj.args))
                else:
                    func_result = getattr(module, func__name__)(*eval(obj.args), **ujson.loads(obj.kwargs))
        except Exception as err:
            ScheduleResult.objects.create(result={"success": False, "result": err.args})
        else:
            ScheduleResult.objects.create(result={"success": True, "result": func_result})
        obj.delete()

    earliest_next_job = ScheduleCommander.objects.filter(earliest_execution_date__gte=get_current_time()
                                                         ).order_by('earliest_execution_date').first()
    if earliest_next_job:
        print(int(earliest_next_job.earliest_execution_date.timestamp()))
    else:
        # the script will now sleep for 10min
        print(int((get_current_time() + datetime.timedelta(minutes=10)).timestamp()))


class Command(BaseCommand):
    help = 'Runs schedules if there are ones'

    def handle(self, *args, **options):
        run_scheduled_jobs()
