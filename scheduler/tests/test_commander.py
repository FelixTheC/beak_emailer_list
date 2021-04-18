#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@created: 18.04.21
@author: felix
"""
from unittest import TestCase

from scheduler.commander import schedule_me
from scheduler.management.commands.run_schedule import run_scheduled_jobs
from scheduler.models import ScheduleCommander
from scheduler.models import ScheduleResult


@schedule_me(max_per_round=1, wait_seconds=60, total_runs=lambda: 2)
def say_hello():
    return 'Hello'


class ScheduleCommanderTest(TestCase):

    def setUp(self) -> None:
        super().setUp()
        ScheduleCommander.objects.all().delete()
        ScheduleResult.objects.all().delete()

    def tearDown(self) -> None:
        super().tearDown()
        ScheduleCommander.objects.all().delete()
        ScheduleResult.objects.all().delete()

    def test_schedule_function_call_creates_db_entry(self):
        say_hello()

        objs = ScheduleCommander.objects.all().order_by('-earliest_execution_date')
        self.assertEqual(len(objs), 2)
        self.assertGreater(objs[0].earliest_execution_date, objs[1].earliest_execution_date)
        self.assertTrue(59 <= (objs[0].earliest_execution_date - objs[1].earliest_execution_date
                               ).total_seconds()
                        <= 60
                        )
        self.assertTrue(
            all(obj.func == 'say_hello' for obj in objs)
        )

    def test_run_scheduled_jobs(self):
        say_hello()
        run_scheduled_jobs()
        results = ScheduleResult.objects.all()
        self.assertGreater(results.count(), 0)
        self.assertEqual(results[0].result, {'success': True, 'result': 'Hello'})

    def test_scheduled_jobs_get_cleaned_up(self):
        say_hello()
        self.assertEqual(ScheduleCommander.objects.count(), 2)
        run_scheduled_jobs()
        self.assertEqual(ScheduleCommander.objects.count(), 1)
