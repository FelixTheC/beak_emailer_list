#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@created: 15.04.21
@author: felix
"""
import datetime
from functools import wraps
import inspect

import ujson

from scheduler.models import ScheduleCommander


def should_register() -> bool:
    """
    we need to check in the `stack-trace` if the execution of a schedule job is called
    to not do re-register them again and again
    """
    file_partial_name = 'management/commands/run_schedule.py'
    file_trace = inspect.getframeinfo(inspect.currentframe().f_back).filename
    file_trace_2 = inspect.getframeinfo(inspect.currentframe().f_back.f_back).filename
    return file_partial_name not in file_trace and file_partial_name not in file_trace_2


def create_schedule_entry(earliest_execution_date: datetime, args: tuple, kwargs: dict,
                          module: str, func_name: str) -> None:
    ScheduleCommander.objects.create(
        earliest_execution_date=earliest_execution_date,
        args=str(args),
        kwargs=ujson.dumps(kwargs),
        module=module,
        func=func_name
    )


def schedule_me(_func=None, *, max_per_round: int, wait_seconds: int, total_runs: callable):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if should_register():
                module = func.__module__
                func_name = func.__name__
                dt_now = datetime.datetime.now()
                tr = total_runs()
                if tr <= max_per_round:
                    for _ in range(tr):
                        create_schedule_entry(dt_now, args, kwargs, module, func_name)
                else:
                    prev = max_per_round * -1
                    for i in range(0, tr, max_per_round):
                        for _ in range(i - prev):
                            create_schedule_entry(dt_now, args, kwargs, module, func_name)
                        prev = i
                        dt_now += datetime.timedelta(seconds=wait_seconds)

            return func(*args, **kwargs)
        return inner

    if _func:
        return wrapper(_func)
    else:
        return wrapper
