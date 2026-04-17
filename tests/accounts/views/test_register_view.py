from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from CheckPoint.accounts.models import Profile


class RegisterViewTests(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.home_url = reverse('home')
        self.valid_payload = {
            'username': 'new_user',
            'email': 'new_user@example.com',
            'password1': 'StrongPass1!',
            'password2': 'StrongPass1!',
        }

    def test_register_post_valid_data__when_valid_payload_submitted__creates_user_and_profile(self):
        response = self.client.post(self.register_url, data=self.valid_payload)

        self.assertRedirects(response, self.login_url)
        self.assertTrue(self.user_model.objects.filter(username='new_user').exists())

        user = self.user_model.objects.get(username='new_user')
        self.assertEqual(user.email, 'new_user@example.com')
        self.assertTrue(Profile.objects.filter(user=user).exists())

    def test_register_post_existing_username__when_username_already_exists__returns_form_error(self):
        self.user_model.objects.create_user(
            username='new_user',
            email='different@example.com',
            password='StrongPass1!',
        )

        response = self.client.post(self.register_url, data=self.valid_payload)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This username is already taken.')

    def test_register_post_existing_email__when_email_already_exists__returns_form_error(self):
        self.user_model.objects.create_user(
            username='existing_user',
            email='new_user@example.com',
            password='StrongPass1!',
        )

        response = self.client.post(self.register_url, data=self.valid_payload)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'A user with this email already exists.')

    def test_register_post_weak_password__when_password_fails_strength_validation__returns_form_error(self):
        payload = self.valid_payload.copy()
        payload['password1'] = 'weak'
        payload['password2'] = 'weak'

        response = self.client.post(self.register_url, data=payload)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Password must be at least 8 characters long.')
        self.assertFalse(self.user_model.objects.filter(username='new_user').exists())

    def test_register_post_password_mismatch__when_password_confirmation_differs__returns_form_error(self):
        payload = self.valid_payload.copy()
        payload['password2'] = 'StrongPass2!'

        response = self.client.post(self.register_url, data=payload)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'The two password fields didn')
        self.assertFalse(self.user_model.objects.filter(username='new_user').exists())

    def test_register_get_authenticated_user__when_user_is_logged_in__redirects_home(self):
        user = self.user_model.objects.create_user(
            username='already_logged',
            email='already_logged@example.com',
            password='StrongPass1!',
        )
        self.client.force_login(user)

        response = self.client.get(self.register_url)

        self.assertRedirects(response, self.home_url)

    def test_register_post_authenticated_user__when_user_is_logged_in__redirects_home_without_creating_user(self):
        user = self.user_model.objects.create_user(
            username='already_logged',
            email='already_logged@example.com',
            password='StrongPass1!',
        )
        self.client.force_login(user)

        response = self.client.post(self.register_url, data=self.valid_payload)

        self.assertRedirects(response, self.home_url)
        self.assertFalse(self.user_model.objects.filter(username='new_user').exists())
