from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField

class Newsletter(models.Model):
    delivery_time = models.DateTimeField(verbose_name='Дата начала рассылки')
    end_delivery_time = models.DateTimeField(verbose_name='Дата окончания рассылки')
    creation_date = models.DateTimeField(auto_now_add=True,
                                         verbose_name='Дата создания')
    frequency = models.CharField(max_length=40,
                                 verbose_name='Периодичность отправки',
                                 choices=[('daily', 'Раз в день'),
                                          ('weekly', 'Раз в неделю'),
                                          ('monthly', 'Раз в месяц')],
                                 default='monthly')

    status = models.CharField(max_length=40,
                              choices=[('completed', 'Завершена'),
                                       ('created', 'Создана'),
                                       ('running', 'Запущена'),
                                       ('paused', 'Приостановлена')],
                              default='created')

    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.SET_NULL,
                                verbose_name='Создатель',
                                null=True, blank=True)

    task_id = models.CharField(max_length=100, blank=True, null=True)

    recipients = ArrayField(models.CharField(max_length=100), default=list, verbose_name='Получатели')

    def __str__(self):
        return f'Рассылка {self.pk}'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
        permissions = [
            (
                'start_and_stop_newsletter',
                'Can start and stop newsletter'
            )
        ]


class NewsletterMessage(models.Model):
    newsletter = models.ForeignKey(Newsletter, on_delete=models.CASCADE)
    theme = models.CharField(max_length=255)
    body = models.TextField()

    def __str__(self):
        return self.theme

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'


class NewsletterLog(models.Model):
    newsletter = models.ForeignKey(NewsletterMessage, on_delete=models.CASCADE)
    attempt_datetime = models.DateTimeField(auto_now_add=True)
    attempt_status = models.CharField(max_length=20)
    mail_server_response = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'Лог рассылки {self.newsletter.pk}'

    class Meta:
        verbose_name = 'лог'
        verbose_name_plural = 'логи'
