from django.urls import path
from .views import generic_sync_task, single_async_task, task_link, task_link_error, time_out_task, retry_task_view, chain_task, chain_task_si, group_task, group_in_chain

urlpatterns = [
    path('sync/', generic_sync_task, name="generic_sync_task"),
    path('async/', single_async_task, name="single_async_task"),
    path('link/', task_link, name="task_link"),
    path('link_error/', task_link_error, name="task_link_error"),
    path('time_out/', time_out_task, name="time_out_task"),
    path('retry_task/', retry_task_view, name="retry_task_view"),
    path('chain/', chain_task, name="chain_task"),
    path('chain_si/', chain_task_si, name="chain_task_si"),
    path('group/', group_task, name="group_task"),
    path('group_in_chain/', group_in_chain, name="group_in_chain"),
]