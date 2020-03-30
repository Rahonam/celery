# celery
A guide for implementing celery, using django web framework.

1. Setup your django project.
2. Setup a Message Queue Manager/ Broker.
      e.g.: rabbitmq, redis, ...
3. Setup celery
4. Setup backend to store task results
5. Setup flower for monitoring

# STACK - Django - Celery - Rabbitmq

Prerequisites: python, django project setup


CELERY & RABBITMQ
Installation & Management:

To install celery - pip install Celery

To manage celery - celery -A <PROJECT NAME> worker -l info

To install rabbitmq - 

Since rabbitmq is written in erlang programming language, we need ‘erlang’ first

apt-get install -y erlang

apt-get install rabbitmq-server

systemctl is used to examine and control the state of “systemd” system and service manager.

systemd is system and service manager for Unix like operating systems

To manage rabbitmq - 
We need systemctl

systemctl enable rabbitmq-server

systemctl start rabbitmq-server

DJANGO
Extra Setups:

STEP 1
Create a celery.py file alongside settings.py for project
celery.py:
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

app = Celery('mysite')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

Here we’re specifying celery to look in into settings.py of project mysite, with namespace ‘CELERY’ (i.e. every settings prefixed with CELERY_ is for celery usage)

STEP 2
We need to add celery in __init__.py, To load celery settings every time django starts.
__init__.py:
from .celery import app as celery_app

__all__ = ['celery_app']


STEP 3
In order to monitor task progress, we need to have a backend to store task results.
Using django backend itself is optimal for small projects.

To install django_celery_results - pip install django_celery_results

To manage django_celery_results - 

In settings.py add ‘django_celery_results’ to INSTALLED APPS

INSTALLED_APPS = [
    #other apps
    'django_celery_results'
]

Also add the following configurations at the end of the file

CELERY_BROKER_URL = 'amqp://localhost'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

BROKER_URL is the address of our message broker, which will manage task messages.
RESULT_BACKEND is the database for storing task results and status.
ACCEPT_CONTENT is the list of allowed formats for storing results.
TASK_SERIALIZER and RESULT_SERIALIZER specify the formats to which values will be parsed in order to interact with our message broker.

Note: we need to run rabbitmq before celery, celery will always look for a message broker on start.

Steps to start servers:

Once every thing setup as mentioned above
Start Rabbitmq server
systemctl start rabbitmq-server
systemctl status rabbitmq-server (to verify)
Start Celery worker
celery -A <PROJECT NAME> worker -l info
Start Flower (optional for real time monitoring)
celery -A <PROJECT NAME> flower