import requests
import markdown2
from django.shortcuts import render


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


def admin_page(request):
    return render(request, 'common/admin-panel.html')


def events(request):
    return render(request, 'common/events.html')


def add_event(request):
    return render(request, 'common/add-event.html')


def community(request):
    return render(request, 'common/community.html')
