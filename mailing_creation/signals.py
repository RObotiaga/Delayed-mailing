from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Newsletter
from .tasks import my_task, scheduler

@receiver(post_save, sender=Newsletter)
def create_task_on_model_create(sender, instance, created, **kwargs):
    freq = {'daily': 1, 'weekly': 7, 'monthly': 30}
    my_model_id = instance.id
    model = Newsletter.objects.get(id=my_model_id)
    frequency = model.frequency
    delivery_time = model.delivery_time
    if created:
        if model.task_id:
            scheduler.remove_job(model.task_id)
        task = scheduler.add_job(
            my_task,
            "interval",
            start_date=delivery_time,
            args=[my_model_id],  # Передаем аргументы в функцию my_task
            seconds=freq[frequency],  # Пример: задача будет выполняться каждый день
        )
        model.task_id = task.id
        model.save()
