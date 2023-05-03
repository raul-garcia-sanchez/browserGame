from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from django.db.models import Q
from django.urls import reverse
from django.utils.html import format_html

class LogInline(admin.TabularInline):
    model = Log
    # fields = ["user","log_level","title","description","route","date"]
    ordering = ("-date",)
    extra = 0

class EventHistoryInline(admin.TabularInline):
    model = EventHistory
    extra = 0
    fields = ('action', 'user_transmitter', 'user_receiver', 'succeed')
    readonly_fields = ('action', 'user_transmitter', 'user_receiver', 'succeed')
    fk_name = 'user_transmitter'
    verbose_name_plural = 'Events transmesos'


class EventHistoryInlineReceptor(admin.TabularInline):
    model = EventHistory
    extra = 0
    fields = ('action', 'user_transmitter', 'user_receiver', 'succeed')
    readonly_fields = ('action', 'user_transmitter', 'user_receiver', 'succeed')
    fk_name = 'user_receiver'
    verbose_name_plural = 'Events rebuts'


class UserAdmin(admin.ModelAdmin):

    list_display = ['id','username', 'email', 'is_staff', 'level', 'exp', 'life', 'mana', 'last_update',"get_event_history"]
    inlines = [LogInline,  EventHistoryInline, EventHistoryInlineReceptor]
    ordering = ('-date_joined',)
    def get_event_history(self, obj):
        event_history = EventHistory.objects.filter(
            models.Q(user_transmitter=obj) | models.Q(user_receiver=obj)
        ).order_by('-date')[:5]  # Mostrar los últimos 5 eventos

        event_history_links = []
        for event in event_history:
            url = reverse('admin:%s_%s_change' % (
                event._meta.app_label, event._meta.model_name), args=[event.id])
            event_history_links.append('<a href="%s">%s</a>' % (url, str(event)))

        return format_html(', '.join(event_history_links))

    get_event_history.short_description = 'Historial de eventos'


    list_per_page = 25
    list_per_page_options = [10, 25, 50, 100]
    list_max_show_all = 100

admin.site.register(User, UserAdmin)
admin.site.register(GameOption)
admin.site.register(EventHistory)
admin.site.register(Action)
