from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from .models import Newsletter, NewsletterMessage, NewsletterLog
from django.core.mail import send_mail, BadHeaderError
from config import settings
from smtplib import SMTPException
from django.utils import timezone

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")
scheduler.start()


def my_task(my_model_id):
    my_model = Newsletter.objects.get(id=my_model_id)
    model_message = NewsletterMessage.objects.get(newsletter=my_model)
    my_model.status = 'running'
    my_model.save()
    if timezone.now() < my_model.end_delivery_time:
        try:
            send_mail(
                subject=model_message.theme,
                message=model_message.body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=my_model.recipients,
                fail_silently=False
            )
        except SMTPException as e:
            log_entry = NewsletterLog(
                newsletter=model_message,
                attempt_status='Ошибка',
                mail_server_response=str(e)
            )
        else:
            log_entry = NewsletterLog(
                newsletter=model_message,
                attempt_status='Отправлено',
                mail_server_response='200'
            )
        log_entry.save()
    else:
        scheduler.pause_job(my_model.task_id)
        my_model.status = 'completed'
        my_model.save()
