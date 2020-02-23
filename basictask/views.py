from django.shortcuts import render
from django.http import HttpResponse
import time
from .task import heavy_task


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
    heavy_task.delay()

    message = "Response in {} seconds!".format(time.process_time() - start)
    return HttpResponse(message)


