from django.contrib import admin

from theater.models import Actor, Genre, Play, TheatreHall, Performance, Reservation, Ticket
from theater.serializers import TicketSerializer


class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 0
    fields = ("row", "seat", "performance")

    def get_formset(self, request, obj=None, **kwargs):
      formset = super().get_formset(request, obj, **kwargs)
      formset.form.validate = TicketSerializer().validate
      return formset


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    inlines = [TicketInline]
    readonly_fields = ("user",)
    list_display = ("user_email", "created_at", "ticket_count")

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = "User Email"

    def ticket_count(self, obj):
        return obj.tickets.count()

    ticket_count.short_description = "Number of Tickets"

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name"]
    search_fields = ["first_name", "last_name"]
    # ordering = ["first_name", "-first_name", "last_name", "-last_name"]
    # order_fields = ["first_name", "last_name"]


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(Play)
class PlayAdmin(admin.ModelAdmin):
    list_display = ["title", "description"]
    search_fields = ["title", "genres__name"]


@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = ["play__title", "theatre_hall__name", "show_time"]
    search_fields = ["show_time", "play__title", "theatre_hall__name"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("play", "theatre_hall")


@admin.register(TheatreHall)
class TheatreHallAdmin(admin.ModelAdmin):
    list_display = ["name", "capacity"]
    search_fields = ["name"]
