import os
import tempfile
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from PIL import Image

from theater.models import Play, Genre, Actor
from theater.serializers import PlayListSerializer, PlayDetailsSerializer


def create_test_image():
    """Create a test image file for testing image uploads"""
    img = Image.new('RGB', (100, 100), color='red')
    tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
    img.save(tmp_file)
    tmp_file.seek(0)
    return tmp_file


def create_user(email='user@example.com', password='testpass123', is_staff=False):
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


PLAYS_URL = reverse("theater:play-list")


def detail_url(play_id):
    """Return play detail URL"""
    return reverse("theater:play-detail", args=[play_id])


def image_upload_url(play_id):
    """Return URL for play image upload"""
    return reverse("theater:play-upload-image", args=[play_id])


class PublicPlayApiTests(TestCase):
    """Test unauthenticated play API access"""

    def setUp(self):
        self.client = APIClient()
        self.genre = create_genre()
        self.actor = create_actor()

    def test_list_plays(self):
        """Test retrieving a list of plays"""
        create_play()
        create_play(title='Another Play')

        res = self.client.get(PLAYS_URL)

        plays = Play.objects.all().order_by('id')
        serializer = PlayListSerializer(plays, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

    def test_retrieve_play_detail(self):
        """Test retrieving a play detail"""
        play = create_play()
        play.genres.add(self.genre)
        play.actors.add(self.actor)

        url = detail_url(play.id)
        res = self.client.get(url)

        serializer = PlayDetailsSerializer(play)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_play_unauthorized(self):
        """Test creating a play requires admin privileges"""
        payload = {
            'title': 'New Play',
            'description': 'New description',
        }
        res = self.client.post(PLAYS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(Play.objects.filter(title=payload['title']).exists())

    def test_filtering_plays_by_genre(self):
        """Test filtering plays by genre"""
        comedy = create_genre(name='Comedy')
        tragedy = create_genre(name='Tragedy')

        play1 = create_play(title='Funny Play')
        play2 = create_play(title='Sad Play')
        play1.genres.add(comedy)
        play2.genres.add(tragedy)

        res = self.client.get(PLAYS_URL, {'search': 'Comedy'})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 1)
        self.assertEqual(res.data['results'][0]['title'], 'Funny Play')

    def test_filtering_plays_by_title(self):
        """Test filtering plays by title"""
        create_play(title='Hamlet')
        create_play(title='Romeo and Juliet')

        res = self.client.get(PLAYS_URL, {'search': 'Hamlet'})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 1)
        self.assertEqual(res.data['results'][0]['title'], 'Hamlet')


class PrivatePlayApiTests(TestCase):
    """Test authenticated API requests"""

    def setUp(self):
        self.admin_user = create_user(
            email='admin@example.com',
            password='password123',
            is_staff=True
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin_user)
        self.genre = create_genre()
        self.actor = create_actor()

    def test_create_play(self):
        """Test creating a play if admin"""
        genre = create_genre()
        actor = create_actor()

        payload = {
            'title': 'New Play',
            'description': 'This is a test play',
            'genres': [genre.id],
            'actors': [actor.id]
        }
        res = self.client.post(PLAYS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        play = Play.objects.get(id=res.data['id'])

        self.assertEqual(payload['title'], play.title)
        self.assertEqual(payload['description'], play.description)

        self.assertEqual(play.genres.count(), 1)
        self.assertEqual(play.actors.count(), 1)
        self.assertEqual(play.genres.first().id, genre.id)
        self.assertEqual(play.actors.first().id, actor.id)

    def test_partial_update_play(self):
        """Test updating a play with patch"""
        play = create_play()

        payload = {'title': 'Updated Title'}
        url = detail_url(play.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        play.refresh_from_db()
        self.assertEqual(play.title, payload['title'])

    def test_full_update_play(self):
        """Test updating a play with put"""
        play = create_play()
        play.genres.add(self.genre)
        play.actors.add(self.actor)

        new_genre = create_genre(name='Comedy')
        new_actor = create_actor(first_name='Jane', last_name='Smith')

        payload = {
            'title': 'New Title',
            'description': 'New description',
            'genres': [new_genre.id],
            'actors': [new_actor.id]
        }
        url = detail_url(play.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        play.refresh_from_db()
        self.assertEqual(play.title, payload['title'])
        self.assertEqual(play.description, payload['description'])
        self.assertEqual(play.genres.count(), 1)
        self.assertEqual(play.actors.count(), 1)
        self.assertEqual(play.genres.first().id, new_genre.id)
        self.assertEqual(play.actors.first().id, new_actor.id)

    def test_delete_play(self):
        """Test deleting a play"""
        play = create_play()

        url = detail_url(play.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Play.objects.filter(id=play.id).exists())


class PlayImageUploadTests(TestCase):
    """Tests for the Play image upload API"""
    def setUp(self):
        self.admin_user = create_user(
            email='admin@example.com',
            password='password123',
            is_staff=True
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin_user)
        self.play = create_play()
        self.play.genres.add(create_genre())
        self.play.actors.add(create_actor())

    def tearDown(self):
        self.play.image.delete()

    def test_upload_image(self):
        """Test uploading an image to a play"""
        url = image_upload_url(self.play.id)

        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            img = Image.new('RGB', (10, 10))
            img.save(image_file, format='JPEG')
            image_file.seek(0)

            res = self.client.post(
                url,
                {'image': image_file},
                format='multipart'
            )

        self.play.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)

        if res.status_code == status.HTTP_200_OK:
            self.assertTrue(os.path.exists(self.play.image.path))

    def test_upload_image_bad_request(self):
        """Test uploading invalid image"""
        url = image_upload_url(self.play.id)
        res = self.client.post(url, {'image': 'not-an-image'}, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_upload_image_unauthorized(self):
        """Test that non-admin users cannot upload images"""
        self.client.force_authenticate(user=create_user())
        url = image_upload_url(self.play.id)

        with create_test_image() as image_file:
            res = self.client.post(
                url,
                {'image': image_file},
                format='multipart'
            )

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
