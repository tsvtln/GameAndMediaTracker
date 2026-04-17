from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from pathlib import Path
from django.conf import settings
from CheckPoint.roms.models import Rom


class RomUploadDeleteViewTests(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.upload_url = reverse('roms upload')
        self.roms_page_url = reverse('roms page')
        self.login_url = reverse('login')

        self.owner_user = self.user_model.objects.create_user(
            username='owner_user',
            email='owner_user@example.com',
            password='StrongPass1!',
        )
        self.other_user = self.user_model.objects.create_user(
            username='other_user',
            email='other_user@example.com',
            password='StrongPass1!',
        )
        self.staff_user = self.user_model.objects.create_user(
            username='staff_user',
            email='staff_user@example.com',
            password='StrongPass1!',
            is_staff=True,
        )

        self.valid_payload = {
            'title': 'Super Mario Test',
            'platform': 'SNES',
            'genre': 'Platformer',
            'description': 'Test ROM description',
        }

    def _make_rom_file(self, name='test_rom.zip', content=b'PK\x03\x04test-rom'):
        return SimpleUploadedFile(name=name, content=content, content_type='application/zip')

    def _make_box_art(self, name='box_art.png'):
        image_path = Path(settings.BASE_DIR) / 'staticfiles' / 'images' / 'placeholders' / 'no_image_placeholder.png'
        with open(image_path, 'rb') as image_file:
            return SimpleUploadedFile(name=name, content=image_file.read(), content_type='image/png')

    def _create_rom(self, uploaded_by, title='ROM To Delete'):
        return Rom.objects.create(
            title=title,
            platform='SNES',
            genre='Platformer',
            description='Delete test ROM',
            rom_file=self._make_rom_file(name='delete_me.zip'),
            box_art=self._make_box_art(name='delete_me.png'),
            uploaded_by=uploaded_by,
        )

    def test_rom_upload_post__when_authenticated_user_submits_valid_payload__creates_rom_and_redirects_to_details(self):
        self.client.force_login(self.owner_user)
        payload = self.valid_payload.copy()
        payload['rom_file'] = self._make_rom_file()
        payload['box_art'] = self._make_box_art()

        response = self.client.post(self.upload_url, data=payload)

        self.assertEqual(Rom.objects.count(), 1)
        rom = Rom.objects.first()
        self.assertEqual(rom.uploaded_by, self.owner_user)
        self.assertRedirects(response, reverse('roms details', kwargs={'pk': rom.pk}))

    def test_rom_upload_get__when_anonymous_user_requests_upload_page__redirects_to_login(self):
        response = self.client.get(self.upload_url)

        self.assertRedirects(response, f'{self.login_url}?next={self.upload_url}')

    def test_rom_upload_post__when_invalid_rom_extension_submitted__returns_form_error_and_does_not_create_rom(self):
        self.client.force_login(self.owner_user)
        payload = self.valid_payload.copy()
        payload['rom_file'] = self._make_rom_file(name='invalid.txt')
        payload['box_art'] = self._make_box_art()

        response = self.client.post(self.upload_url, data=payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Rom.objects.count(), 0)
        self.assertIn('form', response.context)
        self.assertIn('rom_file', response.context['form'].errors)

    def test_rom_delete_post__when_owner_deletes_existing_rom__removes_rom_and_redirects(self):
        rom = self._create_rom(uploaded_by=self.owner_user)
        delete_url = reverse('roms delete', kwargs={'pk': rom.pk})
        self.client.force_login(self.owner_user)

        response = self.client.post(delete_url)

        self.assertRedirects(response, self.roms_page_url)
        self.assertFalse(Rom.objects.filter(pk=rom.pk).exists())

    def test_rom_delete_post__when_staff_user_deletes_existing_rom__removes_rom(self):
        rom = self._create_rom(uploaded_by=self.owner_user, title='Staff Delete ROM')
        delete_url = reverse('roms delete', kwargs={'pk': rom.pk})
        self.client.force_login(self.staff_user)

        response = self.client.post(delete_url)

        self.assertRedirects(response, self.roms_page_url)
        self.assertFalse(Rom.objects.filter(pk=rom.pk).exists())

    def test_rom_delete_post__when_non_owner_regular_user_deletes_existing_rom__returns_403_and_keeps_rom(self):
        rom = self._create_rom(uploaded_by=self.owner_user, title='Protected ROM')
        delete_url = reverse('roms delete', kwargs={'pk': rom.pk})
        self.client.force_login(self.other_user)

        response = self.client.post(delete_url)

        self.assertEqual(response.status_code, 403)
        self.assertTrue(Rom.objects.filter(pk=rom.pk).exists())
