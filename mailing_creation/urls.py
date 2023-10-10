from django.urls import path
from .views import HomeView, CreateNewsletter, UpdateNewsletter, ReadNewsletter, DeleteNewsletterView, PauseTaskView
app_name = 'mailing_creation'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('create/', CreateNewsletter.as_view(), name='create_newsletter'),
    path('newsletter/<int:pk>/', ReadNewsletter.as_view(), name='newsletter_info'),
    path('update/<int:pk>/', UpdateNewsletter.as_view(), name='update_newsletter'),
    path('delete_newsletter/<int:model_id>/', DeleteNewsletterView.as_view(), name='delete_newsletter'),
    path('pause_task/<int:model_id>/', PauseTaskView.as_view(), name='pause_task'),
]
