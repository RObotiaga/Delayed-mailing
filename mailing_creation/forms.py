from django import forms
from .models import Newsletter, NewsletterMessage
from django.contrib.postgres.fields import ArrayField

class CreateNewsletterForm(forms.ModelForm):
    delivery_time = forms.DateTimeField(widget=forms.widgets.DateInput(attrs={'type': 'datetime-local'}))
    end_delivery_time = forms.DateTimeField(widget=forms.widgets.DateInput(attrs={'type': 'datetime-local'}))
    recipients = ArrayField(forms.CharField(max_length=100), default=list, verbose_name='Получатели')
    class Meta:
        model = Newsletter
        fields = ['delivery_time', 'end_delivery_time', 'frequency', 'recipients']


class CreateNewsletterMessageForm(forms.ModelForm):
    class Meta:
        model = NewsletterMessage
        fields = ['theme', 'body', ]
