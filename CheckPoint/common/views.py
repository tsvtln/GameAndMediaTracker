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
    changelog_html = ""
    try:
        response = requests.get(changelog_url, timeout=5)
        if response.status_code == 200:
            changelog_md = response.text
            changelog_html = markdown2.markdown(changelog_md)
        else:
            changelog_html = "<p>No News here at the moment ¯\_(ツ)_/¯</p>"
    except Exception:
        changelog_html = "<p>No News here at the moment ¯\_(ツ)_/¯</p>"
    return render(request, 'common/website-news.html', {'changelog_html': changelog_html})
