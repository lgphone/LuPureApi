from celery import Celery
from app.config import CELERY_BROKER_URL
from app.model.users import Users

celery = Celery(__name__, broker=CELERY_BROKER_URL)


@celery.task
def test(name):
    print(name)
    import time
    time.sleep(3)
    res = Users.query.all()
    for r in res:
        print(r.id, r.username)
    print(res)
    print('123')
