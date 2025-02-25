import tempfile

from PIL import Image
from django.contrib.auth import get_user_model
from django.urls import reverse

from theater.models import Genre, Actor, Play


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

def detail_url(play_id):
    """Return play detail URL"""
    return reverse("theater:play-detail", args=[play_id])


def image_upload_url(play_id):
    """Return URL for play image upload"""
    return reverse("theater:play-upload-image", args=[play_id])