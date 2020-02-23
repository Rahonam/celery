from django.urls import path
from .views import generic_sync_task, single_async_task

urlpatterns = [
    path('sync/', generic_sync_task, name="generic_sync_task"),
    path('async/', single_async_task, name="single_async_task")
]