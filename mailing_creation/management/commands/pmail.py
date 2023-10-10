from django.core.management import BaseCommand

from mailing_creation.models import Newsletter
from mailing_creation.tasks import scheduler

class Command(BaseCommand):
    help = u'Приостановка рассылки'

    def add_arguments(self, parser):
        parser.add_argument('pk', type=int, help=u'pk рассылки')

    def handle(self, *args, **kwargs):
        pk = kwargs['pk']
        my_model = Newsletter.objects.get(pk=pk)
        task_id = my_model.task_id
        if task_id:
            if my_model.status == 'paused' or my_model.status == 'completed':
                print('Рассылка уже приостановлена или окончена')
            else:
                scheduler.pause_job(task_id)
                my_model.status = 'paused'
                my_model.save()
                print('приостановлено')
