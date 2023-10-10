from django import forms
from .models import Newsletter, NewsletterMessage


class CreateNewsletterForm(forms.ModelForm):
    delivery_time = forms.DateTimeField(widget=forms.widgets.DateInput(attrs={'type': 'datetime-local'}))
    end_delivery_time = forms.DateTimeField(widget=forms.widgets.DateInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Newsletter
        fields = ['delivery_time', 'end_delivery_time', 'frequency', 'recipients']


class CreateNewsletterMessageForm(forms.ModelForm):
    class Meta:
        model = NewsletterMessage
        fields = ['theme', 'body', ]
