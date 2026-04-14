from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, DetailView, DeleteView, ListView
from django.views import View
from django.urls import reverse_lazy as _
from django.db.models import Count, Avg
from django.http import FileResponse, Http404
from django.utils import timezone
from datetime import timedelta
from CheckPoint.roms.models import Rom, Comment, Review
from CheckPoint.roms.forms import RomUploadForm, CommentForm, ReviewForm
from CheckPoint.common.permissions import OwnerOrModeratorMixin


def roms(request):
    # Get top 3 ROMs for each category
    top_games_list = Rom.objects.order_by('-rating', '-downloads')[:3]
    newly_added_list = Rom.objects.order_by('-created_at')[:3]
    trending_list = Rom.objects.order_by('-downloads', '-created_at')[:3]
    most_downloaded_list = Rom.objects.order_by('-downloads')[:3]

    context = {
        'top_games': top_games_list,
        'newly_added': newly_added_list,
        'trending': trending_list,
        'most_downloaded': most_downloaded_list,
    }
    return render(request, 'roms/roms.html', context)


class TopGamesView(ListView):
    model = Rom
    template_name = 'roms/top-games.html'
    context_object_name = 'roms'

    def get_queryset(self):
        # Get ROMs with their average rating from reviews
        return Rom.objects.annotate(
            review_count=Count('reviews'),
            avg_rating=Avg('reviews__rating')
        ).order_by('-rating', '-avg_rating', '-downloads')[:11]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        roms = list(self.get_queryset())

        # Top 3 for banner
        context['top_3'] = roms[:3] if len(roms) >= 3 else roms

        # remaining for list
        context['remaining_roms'] = roms[3:] if len(roms) > 3 else []

        return context


class NewlyAddedView(ListView):
    model = Rom
    template_name = 'roms/newly-added.html'
    context_object_name = 'roms'
    paginate_by = 20

    def get_queryset(self):
        queryset = Rom.objects.all()
        sort_by = self.request.GET.get('sort', 'date')
        filter_by = self.request.GET.get('filter', '')

        if filter_by == 'week':
            week_ago = timezone.now() - timedelta(days=7)
            queryset = queryset.filter(created_at__gte=week_ago)
        elif filter_by == 'month':
            month_ago = timezone.now() - timedelta(days=30)
            queryset = queryset.filter(created_at__gte=month_ago)

        if sort_by == 'platform':
            queryset = queryset.order_by('platform', '-created_at')
        elif sort_by == 'downloads':
            queryset = queryset.order_by('-downloads', '-created_at')
        else:
            queryset = queryset.order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # for this week and month calculation
        week_ago = timezone.now() - timedelta(days=7)
        month_ago = timezone.now() - timedelta(days=30)

        context['week_count'] = Rom.objects.filter(created_at__gte=week_ago).count()
        context['month_count'] = Rom.objects.filter(created_at__gte=month_ago).count()
        context['current_filter'] = self.request.GET.get('filter', '')

        return context


class TrendingView(ListView):
    model = Rom
    template_name = 'roms/trending.html'
    context_object_name = 'roms'

    def get_queryset(self):
        month_ago = timezone.now() - timedelta(days=30)
        return Rom.objects.filter(created_at__gte=month_ago).order_by('-downloads', '-rating')[:6]


class MostDownloadedView(ListView):
    model = Rom
    template_name = 'roms/most-downloaded.html'
    context_object_name = 'roms'
    paginate_by = 20

    def get_queryset(self):
        queryset = Rom.objects.all()
        platform = self.request.GET.get('platform', '')

        if platform:
            queryset = queryset.filter(platform=platform)

        sort_by = self.request.GET.get('sort', 'all-time')
        if sort_by == 'year':
            year_ago = timezone.now() - timedelta(days=365)
            queryset = queryset.filter(created_at__gte=year_ago)
        elif sort_by == 'month':
            month_ago = timezone.now() - timedelta(days=30)
            queryset = queryset.filter(created_at__gte=month_ago)

        return queryset.order_by('-downloads', '-rating')


def genres(request):
    return render(request, 'roms/genres.html')


class GenreDetailView(ListView):
    model = Rom
    context_object_name = 'roms'
    paginate_by = 20

    def get_template_names(self):
        genre = self.kwargs.get('genre')
        return [f'roms/genres/{genre}.html']

    def get_queryset(self):
        genre = self.kwargs.get('genre')
        all_geners = {
            'action': 'Action',
            'adventure': 'Adventure',
            'platformer': 'Platformer',
            'rpg': 'RPG',
            'fighting': 'Fighting',
            'shooter': 'Shooter',
            'puzzle': 'Puzzle',
            'sports': 'Sports',
            'racing': 'Racing',
            'strategy': 'Strategy',
            'simulation': 'Simulation',
            'horror': 'Horror',
        }

        genre_name = all_geners.get(genre, '')
        if not genre_name:
            return Rom.objects.none()

        queryset = Rom.objects.filter(genre=genre_name)

        platform = self.request.GET.get('platform', '')
        if platform:
            queryset = queryset.filter(platform=platform)

        rating = self.request.GET.get('rating', '')
        if rating:
            queryset = queryset.filter(rating__gte=float(rating))

        return queryset.order_by('-rating', '-downloads')


def platforms(request):
    return render(request, 'roms/platforms.html')


class PlatformDetailView(ListView):
    model = Rom
    context_object_name = 'roms'
    paginate_by = 20
    
    all_platforms = {
        '32x': '32X',
        'nes': 'NES',
        'famicom': 'Famicom',
        'snes': 'SNES',
        'super-famicom': 'Super Famicom',
        'n64': 'Nintendo 64',
        'gamecube': 'GameCube',
        'wii': 'Wii',
        'wii-u': 'Wii U',
        'nintendo-switch': 'Nintendo Switch',
        'gameboy': 'Game Boy',
        'gbc': 'Game Boy Color',
        'gba': 'Game Boy Advance',
        'nintendo-ds': 'Nintendo DS',
        'nintendo-3ds': 'Nintendo 3DS',
        'sega-master-system': 'Sega Master System',
        'genesis': 'Sega Genesis / Mega Drive',
        'sega-cd': 'Sega CD',
        'sega-saturn': 'Sega Saturn',
        'sega-dreamcast': 'Sega Dreamcast',
        'game-gear': 'Game Gear',
        'ps1': 'PlayStation',
        'ps2': 'PlayStation 2',
        'ps3': 'PlayStation 3',
        'psp': 'PlayStation Portable (PSP)',
        'vita': 'PlayStation Vita',
        'xbox': 'Xbox',
        'xbox-360': 'Xbox 360',
        'xbox-one': 'Xbox One',
        'atari': 'Atari',
    }

    def get_template_names(self):
        platform = self.kwargs.get('platform')
        return [f'roms/platforms/{platform}.html']

    def get_queryset(self):
        platform = self.kwargs.get('platform')
        platform_name = self.all_platforms.get(platform, '')
        if not platform_name:
            return Rom.objects.none()

        queryset = Rom.objects.filter(platform=platform_name)

        # search bar functionality
        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        return queryset.order_by('-rating', '-downloads')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        platform = self.kwargs.get('platform')
        platform_name = self.all_platforms.get(platform, '')
        
        if platform_name:
            context['total_games'] = Rom.objects.filter(platform=platform_name).count()
        else:
            context['total_games'] = 0

        return context


class RomDetailView(DetailView):
    model = Rom
    template_name = 'roms/rom-details.html'
    context_object_name = 'rom'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rom = self.get_object()
        user = self.request.user

        # check if user can delete this ROM
        can_delete = False
        if user.is_authenticated:
            if user.is_staff or rom.uploaded_by == user:
                can_delete = True
            elif user.groups.filter(name='Moderators').exists():
                can_delete = True

        context['can_delete'] = can_delete
        context['comments'] = rom.comments.select_related('user').all()
        context['reviews'] = rom.reviews.select_related('user').all()
        context['comment_form'] = CommentForm()
        context['review_form'] = ReviewForm()

        # check if user has already reviewed this ROM so we can hide it in the front end if true
        if user.is_authenticated:
            context['user_has_reviewed'] = rom.reviews.filter(user=user).exists()
            context['is_moderator'] = user.groups.filter(name='Moderators').exists()
        else:
            context['user_has_reviewed'] = False
            context['is_moderator'] = False

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if 'rating' in request.POST:
            # Handle review
            review_id = request.POST.get('review_id')

            if review_id:
                # Editing existing review
                try:
                    review = Review.objects.get(pk=review_id, rom=self.object)
                    if request.user == review.user:
                        form = ReviewForm(request.POST, instance=review)
                        if form.is_valid():
                            form.save()
                            self.object.update_rating()
                            messages.success(request, 'Review updated successfully!')
                        else:
                            messages.error(request, 'Error updating review.')
                    else:
                        messages.error(request, 'You can only edit your own reviews.')
                except Review.DoesNotExist:
                    messages.error(request, 'Review not found.')
            else:
                # Creating new review
                form = ReviewForm(request.POST)
                if form.is_valid() and request.user.is_authenticated:
                    # Check if user already reviewed this ROM
                    if Review.objects.filter(rom=self.object, user=request.user).exists():
                        messages.error(request, 'You have already reviewed this ROM.')
                    else:
                        review = form.save(commit=False)
                        review.rom = self.object
                        review.user = request.user
                        review.save()
                        self.object.update_rating()
                        messages.success(request, 'Review posted successfully!')
                else:
                    if not request.user.is_authenticated:
                        messages.error(request, 'You must be logged in to write a review.')
                    else:
                        messages.error(request, 'Error posting review. Please try again.')
        else:
            # Handle comment
            comment_id = request.POST.get('comment_id')

            if comment_id:
                # editing existing comment
                try:
                    comment = Comment.objects.get(pk=comment_id, rom=self.object)
                    if request.user == comment.user:
                        form = CommentForm(request.POST, instance=comment)
                        if form.is_valid():
                            form.save()
                            messages.success(request, 'Comment updated successfully!')
                        else:
                            messages.error(request, 'Error updating comment.')
                    else:
                        messages.error(request, 'You can only edit your own comments.')
                except Comment.DoesNotExist:
                    messages.error(request, 'Comment not found.')
            else:
                # creating new comment
                form = CommentForm(request.POST)
                if form.is_valid() and request.user.is_authenticated:
                    comment = form.save(commit=False)
                    comment.rom = self.object
                    comment.user = request.user
                    comment.save()
                    messages.success(request, 'Comment posted successfully!')
                else:
                    if not request.user.is_authenticated:
                        messages.error(request, 'You must be logged in to comment.')
                    else:
                        messages.error(request, 'Error posting comment. Please try again.')

        return self.get(request, *args, **kwargs)


class RomUploadView(LoginRequiredMixin, CreateView):
    model = Rom
    form_class = RomUploadForm
    template_name = 'roms/upload_rom.html'
    login_url = '/accounts/login/'

    def get_success_url(self):
        return _(
            'roms details',
            kwargs={'pk': self.object.pk}
        )

    def form_valid(self, form):
        # set uploaded by to the current user
        form.instance.uploaded_by = self.request.user
        messages.success(self.request, f'ROM "{form.instance.title}" uploaded successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error uploading ROM. Please check the form.')
        return super().form_invalid(form)


class RomDeleteView(LoginRequiredMixin, OwnerOrModeratorMixin, DeleteView):
    model = Rom
    success_url = _('roms page')
    login_url = '/accounts/login/'
    pk_url_kwarg = 'pk'
    owner_field = 'uploaded_by'

    def delete(self, request, *args, **kwargs):
        rom = self.get_object()
        messages.success(request, f'ROM "{rom.title}" deleted successfully!')
        return super().delete(request, *args, **kwargs)


class CommentDeleteView(LoginRequiredMixin, OwnerOrModeratorMixin, DeleteView):
    model = Comment
    pk_url_kwarg = 'pk'
    owner_field = 'user'

    def get_success_url(self):
        return _(
            'roms details',
            kwargs={'pk': self.object.rom.pk}
        )

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Comment deleted successfully!')
        return super().delete(request, *args, **kwargs)


class ReviewDeleteView(LoginRequiredMixin, OwnerOrModeratorMixin, DeleteView):
    model = Review
    pk_url_kwarg = 'pk'
    owner_field = 'user'

    def get_success_url(self):
        return _(
            'roms details',
            kwargs={'pk': self.object.rom.pk}
        )

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Review deleted successfully!')
        return super().delete(request, *args, **kwargs)


class RomDownloadView(View):
    def get(self, request, pk):
        try:
            rom = Rom.objects.get(pk=pk)
            rom.increment_downloads()

            # return file for download
            response = FileResponse(rom.rom_file.open('rb'))
            response['Content-Disposition'] = f'attachment; filename="{rom.title}.{rom.rom_file.name.split(".")[-1]}"'
            return response
        except Rom.DoesNotExist:
            raise Http404("ROM not found")
