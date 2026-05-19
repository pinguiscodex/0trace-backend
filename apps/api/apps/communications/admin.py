from django.contrib import admin

from .models import MailMessage, MailRecipientState, Notification


admin.site.register(MailMessage)
admin.site.register(MailRecipientState)
admin.site.register(Notification)

