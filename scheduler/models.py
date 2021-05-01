import uuid

from django.db import models

from additonal_utils.models import UUIDPrimaryKeyModel


class ScheduleCommander(UUIDPrimaryKeyModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    earliest_execution_date = models.DateTimeField()
    module = models.CharField(max_length=255)
    func = models.CharField(max_length=255)
    args = models.CharField(max_length=255)
    kwargs = models.CharField(max_length=255)

    class Meta(UUIDPrimaryKeyModel.Meta):
        get_latest_by = 'earliest_execution_date'
        ordering = ['earliest_execution_date', ]

    def __str__(self):
        return f'{self.module}.{self.func} - {self.earliest_execution_date}'


class ScheduleResult(UUIDPrimaryKeyModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, editable=False)
    result = models.JSONField()

    class Meta(UUIDPrimaryKeyModel.Meta):
        get_latest_by = 'created_at'
        ordering = ['-created_at', ]

    def __str__(self):
        result_info = 'Success' if self.result["success"] else 'Failed'
        return f'{result_info} at {self.created_at}'
