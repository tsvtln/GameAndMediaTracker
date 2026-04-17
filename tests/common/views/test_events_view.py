from datetime import datetime
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from CheckPoint.common.models import Event


class EventViewTests(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.add_event_url = reverse('community add event page')
        self.events_url = reverse('community events page')

        self.staff_user = self.user_model.objects.create_user(
            username='staff_user',
            email='staff_user@example.com',
            password='StrongPass1!',
            is_staff=True,
        )
        self.regular_user = self.user_model.objects.create_user(
            username='regular_user',
            email='regular_user@example.com',
            password='StrongPass1!',
        )

        self.valid_payload = {
            'title': 'Community Tournament',
            'event_date': '2026-05-01T20:00',
            'platform': 'SNES',
            'description': 'Monthly SNES tournament event.',
            'status': 'upcoming',
        }

    def test_event_create_post__when_staff_user_submits_valid_payload__creates_event_and_sets_creator(self):
        self.client.force_login(self.staff_user)

        response = self.client.post(self.add_event_url, data=self.valid_payload)

        self.assertRedirects(response, self.events_url)
        self.assertEqual(Event.objects.count(), 1)
        event = Event.objects.first()
        self.assertEqual(event.created_by, self.staff_user)
        self.assertEqual(event.title, 'Community Tournament')

    def test_event_create_post__when_regular_user_submits_payload__returns_403_and_does_not_create_event(self):
        self.client.force_login(self.regular_user)

        response = self.client.post(self.add_event_url, data=self.valid_payload)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Event.objects.count(), 0)

    def test_event_delete_post__when_staff_user_deletes_existing_event__removes_event(self):
        event = Event.objects.create(
            title='Delete Me',
            event_date=timezone.make_aware(datetime(2026, 5, 1, 20, 0)),
            platform='SNES',
            description='Event to delete.',
            status='upcoming',
            created_by=self.staff_user,
        )
        delete_url = reverse('event delete', kwargs={'pk': event.pk})
        self.client.force_login(self.staff_user)

        response = self.client.post(delete_url)

        self.assertRedirects(response, self.events_url)
        self.assertFalse(Event.objects.filter(pk=event.pk).exists())

    def test_event_delete_post__when_regular_user_deletes_existing_event__returns_403_and_keeps_event(self):
        event = Event.objects.create(
            title='Keep Me',
            event_date=timezone.make_aware(datetime(2026, 5, 1, 20, 0)),
            platform='SNES',
            description='Event to keep.',
            status='upcoming',
            created_by=self.staff_user,
        )
        delete_url = reverse('event delete', kwargs={'pk': event.pk})
        self.client.force_login(self.regular_user)

        response = self.client.post(delete_url)

        self.assertEqual(response.status_code, 403)
        self.assertTrue(Event.objects.filter(pk=event.pk).exists())

