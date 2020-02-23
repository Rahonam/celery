from celery import shared_task
import time

#@shared_task decorator lets us create tasks
#naming our task using name kwargs is a good practice

@shared_task(name="heavyTask")
def heavy_task():

    #simulating a time consuming process
    time.sleep(5)

    return "executed!"
