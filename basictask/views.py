from django.shortcuts import render
from django.http import HttpResponse
import time
from celery import chain, group
from .task import heavy_task, add_num, multiply_num, divide_num, time_out, retry_task, execute_on_failure, execute_on_success

#function execution can be sent to celery using either of these: delay OR apply_async
#my_function.delay(parameters of my_function)
#my_function.apply_async((parameters of my_function), additional parameters as a celery task)

#Below is a normal view/function calling heavy_task() normally/synchronously
def generic_sync_task(request):
    start = time.time()

    heavy_task()
    
    message = "Response in {} seconds!".format(time.time() - start)
    return HttpResponse(message)


#Now we're sending heavy_task() to celery using delay/apply_async
#celery will consume/execute it asynchronously
def single_async_task(request):
    start = time.process_time()

    #heavy_task is sent to celery
    #and the execution control will shift to next line of code instantly
    task = heavy_task.delay()

    print("Task ID: ",task.task_id)

    message = "Response in {} seconds! </br> Observe the celery logs for task execution.".format(time.process_time() - start)
    return HttpResponse(message)


#link and error link
#link executes if the current Task executed successfully
def task_link(request):
    task = add_num.apply_async((4, 5), link=execute_on_success.s())

    return HttpResponse("Task ID: {} </br> Observe the celery logs for task execution.".format(task.task_id))


#error link executes if the current Task execution failed
#passing invalid str type argument "five" for failure
def task_link_error(request):
    task = add_num.apply_async((4, "five"), link_error=execute_on_failure.s())

    return HttpResponse("Task ID: {} </br> Observe the celery logs for task execution.".format(task.task_id))


#time out will occur here
def time_out_task(request):
    task = time_out.apply_async()

    return HttpResponse("Task ID: {} </br> Observe the celery logs for task execution.".format(task.task_id))


#task retry will occur here
def retry_task_view(request):
    task = retry_task.apply_async()

    return HttpResponse("Task ID: {} </br> Observe the celery logs for task execution.".format(task.task_id))


#chaining Task, execute sequentially
#signature .s() allows to pass, return of previous, as 1st argument
def chain_task(request):
    task = chain(add_num.s(4, 5), multiply_num.s(7), divide_num.s(3)).apply_async()

    return HttpResponse("Last child Task ID: {} </br> Observe the celery logs for task execution.".format(task.task_id))


#chain Task, execute sequentially, with immutable signature
#immutable signature .si() allows to have independent arguments
def chain_task_si(request):
    task = chain(add_num.si(4, 5), multiply_num.si(4, 3), divide_num.si(4, 2)).apply_async()

    return HttpResponse("Last child Task ID: {} </br> Observe the celery logs for task execution.".format(task.task_id))


#group Task, execute parallelly
def group_task(request):
    task = group(add_num.s(4, 5), multiply_num.s(4, 3), divide_num.s(4, 2)).apply_async()
    
    return HttpResponse("Last child Task ID: {} </br> Observe the celery logs for task execution.".format(task.id))


#group in chain Task
def group_in_chain(request):
    task = chain(add_num.s(4, 5), group(multiply_num.s(7), divide_num.s(3))).apply_async()

    return HttpResponse("Last child Task ID: {} </br> Observe the celery logs for task execution.".format(task.id))
