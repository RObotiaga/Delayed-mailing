from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Newsletter, NewsletterMessage, NewsletterLog


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('status', 'creator', 'delivery_time', 'frequency', 'recipients')
    list_filter = ('creator', 'status', 'frequency')
    search_fields = ('id', 'delivery_time',)


@admin.register(NewsletterMessage)
class NewsletterMessageAdmin(admin.ModelAdmin):
    list_display = ('theme', 'newsletter_creator')
    list_filter = ('newsletter', 'theme',)
    search_fields = ('newsletter', 'theme', 'body',)

    def newsletter_creator(self, obj):
        return obj.newsletter.creator if obj.newsletter.creator else "N/A"

    newsletter_creator.short_description = 'Автор рассылки'


@admin.register(NewsletterLog)
class NewsletterLogAdmin(admin.ModelAdmin):
    list_display = ('newsletter', 'attempt_status', 'mail_server_response', 'attempt_datetime')
    list_filter = ('newsletter', 'attempt_status',)
    search_fields = ('newsletter', 'attempt_status', 'mail_server_response',)

    def newsletter_message(self, obj):
        return obj.newsletter.newsletter.recipients

    newsletter_message.short_description = 'Получатели'
