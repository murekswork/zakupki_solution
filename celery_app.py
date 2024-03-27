from celery import Celery

from celery_tasks.tasks import ExtractXmlTask, ParseLinksTask

app = Celery('Worker')
app.conf.broker_url = 'redis://redis:6379'
app.conf.result_backend = 'redis://redis:6379'
app.conf.update(
    CELERY_WORKER_CONCURRENCY=10
)

app.register_task(ParseLinksTask())
app.register_task(ExtractXmlTask())
