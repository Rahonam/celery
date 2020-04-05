from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded, MaxRetriesExceededError
import requests
import time
import logging

log = logging.getLogger("celeryguide")

#@shared_task decorator lets us create tasks
#naming our task using name kwargs is a good practice
#bind=True allows to accept self as 1st argument
#trail=True allows to send monitoring events


#simple Task
@shared_task(name="HeavyTask")
def heavy_task():

    #simulating a time consuming process
    time.sleep(5)

    return "executed!"


#add two integers
@shared_task(name="AddNum", bind=True, trail=True)
def add_num(self, num1, num2):
    time.sleep(3)
    sum=num1+num2
    log.info("({}+{}) Sum: {}".format(num1, num2, sum))

    return sum


#multiply two integers
@shared_task(name="MultiplyNum", bind=True, trail=True)
def multiply_num(self, num1, num2):
    time.sleep(3)
    multiply=num1*num2
    log.info("({}*{}) Product: {}".format(num1, num2, multiply))

    return multiply


#divide two integers
@shared_task(name="DivideNum", bind=True, trail=True)
def divide_num(self, num1, num2):
    time.sleep(3)
    quotient=num1/num2
    log.info("({}/{}) Quotient: {}".format(num1, num2, quotient))

    return quotient


#timeout occurs in this task
#soft_time_limit allows to kill a time consuming task
#we are handling with try-except to prevent kill
@shared_task(name="TimeOut", bind=True, trail=True, soft_time_limit=5)
def time_out(self):
    try:
        time.sleep(20)
    except SoftTimeLimitExceeded:
        log.info("Time limit exceeded!")


#retry allows task to be executed again
#helpful for network based tasks
@shared_task(name="RetryTask", bind=True, trail=True, soft_time_limit=3, default_retry_delay=3)
def retry_task(self):
    try:
        time.sleep(5)
    except SoftTimeLimitExceeded:
        try:
            raise self.retry()
        except MaxRetriesExceededError:
            log.info("Max retry exceeded!")


#Execute this on Task Failure
@shared_task(name="ExecuteOnFailure", bind=True, trail=True)
def execute_on_failure(self, previous_result):
    log.info("Current Task ID: {}".format(self.request.id))
    log.info("Previous exception: {}".format(previous_result))

    return "Task Failed!"


#Execute this on Task Success
@shared_task(name="ExecuteOnSuccess", bind=True, trail=True)
def execute_on_success(self, previous_result):
    log.info("Current Task ID: {}".format(self.request.id))
    log.info("Previous result: {}".format(previous_result))

    return "Task Succeeded!"