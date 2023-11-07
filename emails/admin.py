from django.contrib import admin

from emails.models import Email


class EmailAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender_provider')
    list_filter = ('sender_provider', )


admin.site.register(Email, EmailAdmin)
