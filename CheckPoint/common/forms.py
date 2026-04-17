from django import forms
from django.utils.translation import gettext_lazy as gtl
from CheckPoint.common.models import Event, Thread, Post


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'event_date', 'platform', 'description', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Event title',
                'class': 'event-form-input'
            }),
            'event_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'event-form-input'
            }),
            'platform': forms.Select(attrs={
                'class': 'event-form-select'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Event description',
                'rows': 5,
                'class': 'event-form-textarea'
            }),
            'status': forms.Select(attrs={
                'class': 'event-form-select'
            }),
        }
        labels = {
            'title': gtl('Event Title'),
            'event_date': gtl('Event Date'),
            'platform': gtl('Platform (Optional)'),
            'description': gtl('Description'),
            'status': gtl('Event Status'),
        }
        help_texts = {
            'event_date': gtl('Select the date and time for the event'),
            'description': gtl('Provide details about the event'),
        }


class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['board', 'title']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter topic title...',
                'class': 'forum-form-input'
            }),
            'board': forms.Select(attrs={
                'class': 'forum-form-select'
            }),
        }
        labels = {
            'title': gtl('Title'),
            'board': gtl('Board'),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Write your post...',
                'rows': 6,
                'class': 'forum-form-textarea'
            }),
        }
        labels = {
            'content': gtl('Content'),
        }
