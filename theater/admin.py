from django.contrib import admin

from theater.models import Actor, Genre, Play, TheatreHall, Performance, Reservation, Ticket
from theater.serializers import TicketSerializer


class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 0
    fields = ('row', 'seat', 'performance')

    def get_formset(self, request, obj=None, **kwargs):
      formset = super().get_formset(request, obj, **kwargs)
      formset.form.validate = TicketSerializer().validate
      return formset


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    inlines = [TicketInline]
    readonly_fields = ('user',)
    list_display = ('user_email', 'created_at', 'ticket_count')

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = 'User Email'

    def ticket_count(self, obj):
        return obj.tickets.count()

    ticket_count.short_description = 'Number of Tickets'

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Actor)
admin.site.register(Genre)
admin.site.register(Play)
admin.site.register(TheatreHall)
