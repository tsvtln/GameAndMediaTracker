from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from CheckPoint.bios.models import Bios


class BiosUploadViewTests(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.upload_url = reverse('bios upload')
        self.login_url = reverse('login')

        self.valid_payload = {
            'platform': 'SNES',
            'description': 'Test BIOS description',
            'source': 'Unknown source',
        }

        self.verified_group = Group.objects.create(name='Verified Users')
        self.moderator_group = Group.objects.create(name='Moderators')

    def _make_bios_file(self, name='test_bios.bin', content=b'bios-data'):
        return SimpleUploadedFile(name=name, content=content, content_type='application/octet-stream')

    def test_bios_upload_post__when_verified_user_submits_valid_payload__creates_bios_and_sets_uploader(self):
        user = self.user_model.objects.create_user(
            username='verified_user',
            email='verified_user@example.com',
            password='StrongPass1!',
        )
        user.groups.add(self.verified_group)
        self.client.force_login(user)

        payload = self.valid_payload.copy()
        payload['bios_file'] = self._make_bios_file()

        response = self.client.post(self.upload_url, data=payload)

        self.assertRedirects(response, reverse('bios all files'))
        self.assertEqual(Bios.objects.count(), 1)
        bios = Bios.objects.first()
        self.assertEqual(bios.uploaded_by, user)
        self.assertEqual(bios.platform, 'SNES')

    def test_bios_upload_post__when_moderator_submits_valid_payload__creates_bios(self):
        user = self.user_model.objects.create_user(
            username='moderator_user',
            email='moderator_user@example.com',
            password='StrongPass1!',
        )
        user.groups.add(self.moderator_group)
        self.client.force_login(user)

        payload = self.valid_payload.copy()
        payload['bios_file'] = self._make_bios_file(name='mod_bios.bin')

        response = self.client.post(self.upload_url, data=payload)

        self.assertRedirects(response, reverse('bios all files'))
        self.assertEqual(Bios.objects.count(), 1)

    def test_bios_upload_get__when_anonymous_user_requests_upload_page__redirects_to_login(self):
        response = self.client.get(self.upload_url)

        self.assertRedirects(response, f'{self.login_url}?next={self.upload_url}')

    def test_bios_upload_post__when_regular_user_submits_payload__returns_403_and_does_not_create_bios(self):
        user = self.user_model.objects.create_user(
            username='regular_user',
            email='regular_user@example.com',
            password='StrongPass1!',
        )
        self.client.force_login(user)

        payload = self.valid_payload.copy()
        payload['bios_file'] = self._make_bios_file(name='regular_bios.bin')

        response = self.client.post(self.upload_url, data=payload)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Bios.objects.count(), 0)

    def test_bios_upload_post__when_file_extension_is_invalid__returns_form_error(self):
        user = self.user_model.objects.create_user(
            username='verified_user_two',
            email='verified_user_two@example.com',
            password='StrongPass1!',
        )
        user.groups.add(self.verified_group)
        self.client.force_login(user)

        payload = self.valid_payload.copy()
        payload['bios_file'] = self._make_bios_file(name='invalid.txt')

        response = self.client.post(self.upload_url, data=payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Bios.objects.count(), 0)
        self.assertIn('form', response.context)
        self.assertIn('bios_file', response.context['form'].errors)

