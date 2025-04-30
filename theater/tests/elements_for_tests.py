import tempfile

from PIL import Image
from django.contrib.auth import get_user_model
from django.urls import reverse

from theater.models import Genre, Actor, Play, TheatreHall, Performance, Reservation, Ticket

GENRES_URL = reverse("theater:genre-list")
ACTORS_URL = reverse("theater:actor-list")
PLAYS_URL = reverse("theater:play-list")
THEATRE_HALL_URL = reverse("theater:theatrehall-list")
RESERVATIONS_URL = reverse("theater:reservation-list")
PERFORMANCE_URL = reverse("theater:performance-list")


def create_test_image():
    """Create a test image file for testing image uploads"""
    img = Image.new('RGB', (100, 100), color='red')
    tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
    img.save(tmp_file)
    tmp_file.seek(0)
    return tmp_file


def create_user(
        email='user@example.com',
        password='testpass123',
        is_staff=False
):
    """Helper function to create a user"""
    return get_user_model().objects.create_user(
        email=email,
        password=password,
        is_staff=is_staff
    )


def create_genre(name='Drama'):
    """Helper function to create a genre"""
    return Genre.objects.create(name=name)


def create_actor(first_name='John', last_name='Doe'):
    """Helper function to create an actor"""
    return Actor.objects.create(first_name=first_name, last_name=last_name)


def create_play(**params):
    """Helper function to create a play with default values"""
    defaults = {
        'title': 'Test Play',
        'description': 'Test description',
    }
    defaults.update(params)
    return Play.objects.create(**defaults)


def create_theatre_hall(**params):
    """Helper function to create a theatre hall with default values"""
    defaults = {
        "name": "Test Theatre Hall",
        "rows": 9,
        "seats_in_row": 8
    }
    defaults.update(params)
    return TheatreHall.objects.create(**defaults)


def create_performance(
        play=create_play(),
        theatre_hall=create_theatre_hall(),
        show_time="2025-02-20T10:15:30Z"
):
    """Helper function to create a performance hall with default values"""
    return Performance.objects.create(
        play=play,
        theatre_hall=theatre_hall,
        show_time=show_time
    )


def create_reservation(user=None):
    """Helper function to create a reservation with default values"""
    if user is None:
        user = create_user()
    return Reservation.objects.create(user=user)


def create_ticket(reservation, performance, row=1, seat=1):
    return Ticket.objects.create(
        seat=seat,
        row=row,
        reservation=reservation,
        performance=performance
    )


def detail_url(play_id):
    """Return play detail URL"""
    return reverse("theater:play-detail", args=[play_id])


def image_upload_url(play_id):
    """Return URL for play image upload"""
    return reverse("theater:play-upload-image", args=[play_id])
