import requests
import markdown2
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView


def home(request):
    return render(request, 'common/home.html')


def about(request):
    return render(request, 'common/about.html')


def contacts(request):
    return render(request, 'common/contacts.html')


def website_news(request):
    changelog_url = "https://raw.githubusercontent.com/tsvtln/GameAndMediaTracker/refs/heads/main/CHANGELOG.md"
    changelog_md = ""
    changelog_html = "<p>No News here at the moment 🤷‍♂️</p>"
    try:
        response = requests.get(changelog_url, timeout=5)
        if response.status_code == 200:
            changelog_md = response.text
            changelog_html = markdown2.markdown(changelog_md)
    except Exception:
        pass
    return render(request, 'common/website-news.html', {'changelog_html': changelog_html})


class AdminPanelView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    # if someone manually type admin-panel to forward him to login
    template_name = 'common/admin-panel.html'
    login_url = '/accounts/login/'

    def test_func(self):
        # check if user is staff
        return self.request.user.is_staff


def events(request):
    return render(request, 'common/events.html')


def add_event(request):
    return render(request, 'common/add-event.html')


def community(request):
    return render(request, 'common/community.html')


def forum_index(request):
    return render(request, 'forums/forum-index.html')


def forum_board(request, board_slug):
    return render(request, 'forums/forum-board.html', {'board_slug': board_slug})


def forum_thread(request, board_slug, thread_slug):
    return render(request, 'forums/forum-thread.html', {'board_slug': board_slug, 'thread_slug': thread_slug})


def forum_new_topic(request):
    return render(request, 'forums/forum-new-topic.html')


def screenshots_main(request):
    return render(request, 'screenshots/screenshots.html')


def latest_screenshots(request):
    return render(request, 'screenshots/latest.html')


def top_rated_screenshots(request):
    return render(request, 'screenshots/top-rated.html')


def upload_screenshot(request):
    return render(request, 'screenshots/upload-screenshot.html')


def custom_404(request, exception=None):
    return render(request, 'common/404.html', status=404)


def custom_403(request, exception=None):
    return render(request, 'common/403.html', status=403)


def custom_500(request, exception=None):
    return render(request, 'common/500.html', status=500)


class CustomAdminLoginView(LoginView):
    template_name = 'accounts/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return redirect('/admin/')
            else:
                return redirect('profile')
        return super().dispatch(request, *args, **kwargs)


