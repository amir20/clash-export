import os
from datetime import timedelta

from celery import Celery
from model import Player
from mongoengine import connect

celery = Celery('CLASH_TASKS', broker=os.getenv('BROKER_URL'))

connect(db='clashstats', host='db', connect=False)


@celery.task
def test():
    print(Player.objects.distinct('clan.name'))


celery.conf.beat_schedule = {
    'test-every-3-seconds': {
        'task': 'worker.test',
        'schedule': timedelta(seconds=3)
    }
}
