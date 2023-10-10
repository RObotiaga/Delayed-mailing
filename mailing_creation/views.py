from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Newsletter, NewsletterMessage, NewsletterLog
from django.views.generic import ListView, DetailView, View, CreateView, UpdateView, FormView
from .forms import CreateNewsletterForm, CreateNewsletterMessageForm
from .tasks import scheduler


class HomeView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Newsletter
    permission_required = 'mailing_creation.view_newsletter'
    template_name = 'mailing_creation/newsletter_list.html'
    context_object_name = 'newsletters'

    def get_queryset(self):
        return Newsletter.objects.prefetch_related('newslettermessage_set')


class CreateNewsletter(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    permission_required = 'mailing_creation.add_newsletter'
    template_name = 'mailing_creation/newsletter_form.html'
    form_class = CreateNewsletterForm
    second_form_class = CreateNewsletterMessageForm
    success_url = reverse_lazy('mailing_creation:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['newsletter_form'] = context['form']
        context['newsletter_message_form'] = self.second_form_class()
        return context

    def form_valid(self, form):
        # Обработка первой формы
        newsletter = form.save(commit=False)
        newsletter.creator = self.request.user
        newsletter.save()

        # Обработка второй формы
        second_form = self.second_form_class(self.request.POST)
        if second_form.is_valid():
            newsletter_message = second_form.save(commit=False)
            newsletter_message.newsletter = newsletter
            newsletter_message.save()

        return super().form_valid(form)


class UpdateNewsletter(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Newsletter
    permission_required = 'mailing_creation.change_newsletter'
    form_class = CreateNewsletterForm
    template_name = 'mailing_creation/newsletter_form.html'
    success_url = reverse_lazy('mailing_creation:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        newsletter_message = NewsletterMessage.objects.get(newsletter=self.object)
        context['newsletter_message_form'] = CreateNewsletterMessageForm(instance=newsletter_message)
        return context

    def form_valid(self, form):
        # Обработка первой формы
        newsletter = form.save(commit=False)
        newsletter.save()

        # Обработка второй формы
        newsletter_message = NewsletterMessage.objects.get(newsletter=newsletter)
        second_form = CreateNewsletterMessageForm(self.request.POST, instance=newsletter_message)
        if second_form.is_valid():
            second_form.save()

        return super().form_valid(form)


class ReadNewsletter(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Newsletter
    permission_required = 'mailing_creation.view_newsletter'
    template_name = 'mailing_creation/newsletter_info.html'
    context_object_name = 'newsletter'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['newsletter_message'] = NewsletterMessage.objects.get(newsletter=self.object)
        context['newsletter_log'] = context['newsletter_message']
        return context


class DeleteNewsletterView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'mailing_creation.delete_newsletter'

    def get(self, request, model_id):
        my_model = get_object_or_404(Newsletter, id=model_id)
        task_id = my_model.task_id
        if task_id:
            scheduler.remove_job(task_id)
            my_model.task_id = None
            my_model.save()
        my_model.delete()
        return redirect("mailing_creation:home")

class PauseTaskView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'mailing_creation.start_and_stop_newsletter'

    def get(self, request, model_id):
        my_model = get_object_or_404(Newsletter, id=model_id)
        task_id = my_model.task_id
        print(my_model.status)
        if task_id:
            if my_model.status == 'paused' or my_model.status == 'completed':
                scheduler.resume_job(task_id)
                my_model.status = 'created'
                my_model.save()
            else:
                scheduler.pause_job(task_id)
                my_model.status = 'paused'
                my_model.save()
        return redirect("mailing_creation:home")