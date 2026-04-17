import requests
import markdown2
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, CreateView, DeleteView
from django.urls import reverse_lazy as _
from django.http import JsonResponse
from django.utils import timezone
from CheckPoint.common.models import Event, Thread, Board, Post
from CheckPoint.common.forms import EventForm, PostForm, ThreadForm


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
    upcoming_events = Event.objects.filter(status='upcoming', event_date__gte=timezone.now()).order_by('event_date')
    past_events = Event.objects.filter(status='past').order_by('-event_date')

    for event in upcoming_events:
        delta = event.event_date - timezone.now()
        event.days_until = delta.days if delta.days >= 0 else 0

    context = {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'has_events': upcoming_events.exists() or past_events.exists()
    }
    return render(request, 'common/events.html', context)


class AddEventView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'common/add-event.html'
    success_url = _('community events page')
    login_url = '/accounts/login/'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.groups.filter(name='Moderators').exists()

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Event created successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error creating event. Please check the form.')
        return super().form_invalid(form)


@login_required
def mark_event_as_passed(request, pk):
    if request.method == 'POST':
        event = get_object_or_404(Event, pk=pk)

        # only staff and moderators can mark events as passed
        if request.user.is_staff or request.user.groups.filter(name='Moderators').exists():
            event.status = 'past'
            event.save(update_fields=['status'])
            return JsonResponse({'status': 'success', 'message': 'Event marked as passed'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    success_url = _('community events page')
    pk_url_kwarg = 'pk'

    def test_func(self):
        # only staff and moderators can delete events
        return self.request.user.is_staff or self.request.user.groups.filter(name='Moderators').exists()

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Event deleted successfully!')
        return super().delete(request, *args, **kwargs)


def community(request):
    return render(request, 'common/community.html')


def forum_index(request):
    boards = Board.objects.all()
    return render(request, 'forums/forum-index.html', {'boards': boards})


def forum_board(request, board_slug):
    board = get_object_or_404(Board, slug=board_slug)
    threads = Thread.objects.filter(board=board).select_related('author').prefetch_related('posts')

    threads_data = []
    for thread in threads:
        reply_count = thread.posts.count() - 1
        last_post = thread.posts.last() if thread.posts.exists() else None
        threads_data.append({
            'thread': thread,
            'reply_count': reply_count,
            'last_post': last_post,
        })

    context = {
        'board': board,
        'board_slug': board_slug,
        'threads_data': threads_data,
    }
    return render(request, 'forums/forum-board.html', context)


def forum_thread(request, board_slug, thread_slug):
    from django.core.paginator import Paginator
    
    board = get_object_or_404(Board, slug=board_slug)
    thread = get_object_or_404(Thread, board=board, slug=thread_slug)
    all_posts = thread.posts.select_related('author').all()
    
    op_post = all_posts.first() if all_posts.exists() else None
    replies = all_posts[1:] if all_posts.count() > 1 else []
    
    paginator = Paginator(replies, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to reply.')
            return redirect('login')
        
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.thread = thread
            post.author = request.user
            post.save()
            messages.success(request, 'Reply posted successfully!')
            return redirect('forum thread', board_slug=board_slug, thread_slug=thread_slug)
    else:
        form = PostForm()
    
    context = {
        'board': board,
        'board_slug': board_slug,
        'thread': thread,
        'thread_slug': thread_slug,
        'op_post': op_post,
        'replies': page_obj,
        'form': form,
    }
    return render(request, 'forums/forum-thread.html', context)


@login_required
def forum_new_topic(request):
    if request.method == 'POST':
        thread_form = ThreadForm(request.POST)
        post_form = PostForm(request.POST)
        
        if thread_form.is_valid() and post_form.is_valid():
            thread = thread_form.save(commit=False)
            thread.author = request.user
            thread.save()
            
            post = post_form.save(commit=False)
            post.thread = thread
            post.author = request.user
            post.save()
            
            messages.success(request, 'Topic created successfully!')
            return redirect('forum thread', board_slug=thread.board.slug, thread_slug=thread.slug)
    else:
        thread_form = ThreadForm()
        post_form = PostForm()
    
    context = {
        'thread_form': thread_form,
        'post_form': post_form,
    }
    return render(request, 'forums/forum-new-topic.html', context)


class ThreadDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Thread
    pk_url_kwarg = 'pk'
    
    def test_func(self):
        return self.request.user.is_staff or self.request.user.groups.filter(name='Moderators').exists()
    
    def get_success_url(self):
        board_slug = self.object.board.slug
        return f'/forums/{board_slug}/'

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Thread deleted successfully!')
        return super().delete(request, *args, **kwargs)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    pk_url_kwarg = 'pk'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.groups.filter(name='Moderators').exists()

    def get_success_url(self):
        thread = self.object.thread
        return f'/forums/{thread.board.slug}/{thread.slug}/'

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Post deleted successfully!')
        return super().delete(request, *args, **kwargs)


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


