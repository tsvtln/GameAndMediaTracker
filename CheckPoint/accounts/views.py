from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView as DjangoPasswordChangeView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy as _
from django.views.generic import CreateView, DetailView, UpdateView, TemplateView, ListView, DeleteView
from django.http import JsonResponse
from CheckPoint.accounts.models import AppUser, Profile, Screenshot, FavoriteScreenshot
from CheckPoint.common.permissions import OwnerOrModeratorMixin
from CheckPoint.accounts.forms import (
    AppUserRegistrationForm,
    AppUserLoginForm,
    ProfileUpdateForm,
    UserUpdateForm,
    CustomPasswordChangeForm,
    ScreenshotUploadForm
)
from CheckPoint.accounts.tasks import sync_screenshot_favorite_counters


class RegisterView(CreateView):
    # user registration view
    model = AppUser
    form_class = AppUserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = _('login')

    def dispatch(self, request, *args, **kwargs):
        # will redirect to home if already loged in
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # save the user nad log them in
        response = super().form_valid(form)
        messages.success(
            self.request,
            'Registration successful! You can now log in with your credentials.'
        )
        return response

    def form_invalid(self, form):
        messages.error(
            self.request,
            'Registration failed. Please correct the errors below.'
        )
        return super().form_invalid(form)


class AppUserLoginView(LoginView):

    form_class = AppUserLoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return _('home')

    def form_valid(self, form):
        messages.success(self.request, f'Welcome back, {form.get_user().username}!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid email or password.')
        return super().form_invalid(form)


class AppUserLogoutView(LogoutView):
    next_page = _('home')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, 'You have been logged out successfully.')
        return super().dispatch(request, *args, **kwargs)


class ProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile.html'
    context_object_name = 'profile'
    success_url = _('profile')

    def get_object(self, queryset=None):
        return self.request.user.profile

    def form_valid(self, form):
        messages.success(self.request, 'Avatar updated successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error updating avatar. Please try again.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_own_profile'] = True
        return context


class PublicProfileView(DetailView):
    model = AppUser
    template_name = 'accounts/profile.html'
    context_object_name = 'profile_user'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = self.get_object()
        context['user'] = profile_user
        context['is_own_profile'] = self.request.user.is_authenticated and self.request.user == profile_user
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile.html'
    success_url = _('profile')

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'user_form' not in context:
            context['user_form'] = UserUpdateForm(instance=self.request.user)
        context['profile_form'] = context.pop('form')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=self.object
        )
        user_form = UserUpdateForm(
            request.POST,
            instance=request.user
        )

        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect(self.success_url)
        else:
            messages.error(request, 'Please correct the errors below.')
            return self.render_to_response(
                self.get_context_data(
                    profile_form=profile_form,
                    user_form=user_form
                )
            )


class FavoritesView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/favorites.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from CheckPoint.roms.models import FavoriteRom
        
        # get top 2 favorite ROMs
        favorite_roms = FavoriteRom.objects.filter(
            user=self.request.user
        ).select_related('rom')[:2]
        
        # get top 8 favorite screenshots
        favorite_screenshots = FavoriteScreenshot.objects.filter(
            user=self.request.user
        ).select_related('screenshot')[:8]
        
        context['favorite_roms'] = favorite_roms
        context['favorite_screenshots'] = favorite_screenshots
        context['has_favorite_roms'] = favorite_roms.exists()
        context['has_favorite_screenshots'] = favorite_screenshots.exists()
        
        return context


class FavoriteRomsView(LoginRequiredMixin, ListView):
    template_name = 'accounts/favorite-roms.html'
    context_object_name = 'favorite_roms'
    paginate_by = 10

    def get_queryset(self):
        from CheckPoint.roms.models import FavoriteRom
        queryset = FavoriteRom.objects.filter(user=self.request.user).select_related('rom', 'rom__uploaded_by')
        
        platform = self.request.GET.get('platform', '')
        search = self.request.GET.get('search', '')
        sort_by = self.request.GET.get('sort', 'recent')
        
        if platform:
            queryset = queryset.filter(rom__platform=platform)
        
        if search:
            queryset = queryset.filter(rom__title__icontains=search)
        
        if sort_by == 'name':
            queryset = queryset.order_by('rom__title')
        elif sort_by == 'platform':
            queryset = queryset.order_by('rom__platform', '-created_at')
        else:  # recent
            queryset = queryset.order_by('-created_at')
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        platform = self.request.GET.get('platform', '')
        sort_by = self.request.GET.get('sort', 'recent')

        context['selected_platform'] = platform
        context['selected_sort'] = sort_by

        return context


class FavoriteScreenshotsView(LoginRequiredMixin, ListView):
    template_name = 'accounts/favorite-screenshots.html'
    context_object_name = 'favorite_screenshots'
    paginate_by = 12

    def get_queryset(self):
        queryset = FavoriteScreenshot.objects.filter(
            user=self.request.user
        ).select_related('screenshot', 'screenshot__uploaded_by')

        # Apply filters
        platform = self.request.GET.get('platform', '')
        game = self.request.GET.get('game', '')
        search = self.request.GET.get('search', '')
        sort_by = self.request.GET.get('sort', 'recent')

        if platform:
            queryset = queryset.filter(screenshot__platform=platform)

        if game:
            queryset = queryset.filter(screenshot__game_name=game)

        if search:
            queryset = queryset.filter(screenshot__game_name__icontains=search)

        if sort_by == 'game':
            queryset = queryset.order_by('screenshot__game_name')
        elif sort_by == 'platform':
            queryset = queryset.order_by('screenshot__platform', '-created_at')
        else:  # recent
            queryset = queryset.order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # get unique games from user favorited screenshots for filter
        favorited_games = FavoriteScreenshot.objects.filter(
            user=self.request.user
        ).values_list('screenshot__game_name', flat=True).distinct().order_by('screenshot__game_name')

        context['favorited_games'] = favorited_games
        context['selected_platform'] = self.request.GET.get('platform', '')
        context['selected_game'] = self.request.GET.get('game', '')
        context['selected_sort'] = self.request.GET.get('sort', 'recent')

        return context


class PasswordChangeView(LoginRequiredMixin, DjangoPasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'accounts/profile.html'
    success_url = _('profile')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Password changed successfully!')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Error changing password. Please check your input.')
        return super().form_invalid(form)


def accounts(request):
    return render(request, 'accounts/accounts.html')


class ScreenshotUploadView(LoginRequiredMixin, CreateView):
    model = Screenshot
    form_class = ScreenshotUploadForm
    template_name = 'screenshots/upload-screenshot.html'
    login_url = '/accounts/login/'
    success_url = _('my screenshots')

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        response = super().form_valid(form)

        # increment screenshot count on user profile
        self.request.user.profile.increment_screenshots()

        messages.success(self.request, f'Screenshot for "{form.instance.game_name}" uploaded successfully!')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Error uploading screenshot. Please check the form.')
        return super().form_invalid(form)


class ScreenshotListView(TemplateView):
    template_name = 'screenshots/screenshots.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_screenshots'] = Screenshot.objects.select_related('uploaded_by').order_by('-created_at')[:6]
        context['top_rated_screenshots'] = Screenshot.objects.select_related('uploaded_by').order_by('-likes', '-created_at')[:6]
        return context


class LatestScreenshotsView(ListView):
    model = Screenshot
    template_name = 'screenshots/latest.html'
    context_object_name = 'screenshots'
    paginate_by = 12

    def get_queryset(self):
        return Screenshot.objects.select_related('uploaded_by').order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # add favorite status for each screenshot if user is authenticated
        if self.request.user.is_authenticated:
            screenshot_ids = [s.pk for s in context['screenshots']]
            favorited_ids = FavoriteScreenshot.objects.filter(
                user=self.request.user,
                screenshot_id__in=screenshot_ids
            ).values_list('screenshot_id', flat=True)

            for screenshot in context['screenshots']:
                screenshot.is_favorited = screenshot.pk in favorited_ids
        else:
            for screenshot in context['screenshots']:
                screenshot.is_favorited = False

        return context


class TopRatedScreenshotsView(ListView):
    model = Screenshot
    template_name = 'screenshots/top-rated.html'
    context_object_name = 'screenshots'
    paginate_by = 12

    def get_queryset(self):
        queryset = Screenshot.objects.select_related('uploaded_by')
        game_filter = self.request.GET.get('game')

        if game_filter:
            queryset = queryset.filter(game_name__iexact=game_filter)
        else:
            queryset = queryset.filter(likes__gt=0)

        return queryset.order_by('-likes', '-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['game_filter'] = self.request.GET.get('game', '')

        # add favorite status for each screenshot if user is authenticated
        if self.request.user.is_authenticated:
            screenshot_ids = [s.pk for s in context['screenshots']]
            favorited_ids = FavoriteScreenshot.objects.filter(
                user=self.request.user,
                screenshot_id__in=screenshot_ids
            ).values_list('screenshot_id', flat=True)

            for screenshot in context['screenshots']:
                screenshot.is_favorited = screenshot.pk in favorited_ids
        else:
            for screenshot in context['screenshots']:
                screenshot.is_favorited = False

        return context


class MyScreenshotsView(LoginRequiredMixin, ListView):
    model = Screenshot
    template_name = 'screenshots/my-screenshots.html'
    context_object_name = 'screenshots'
    paginate_by = 9
    login_url = '/accounts/login/'

    def get_queryset(self):
        return Screenshot.objects.filter(uploaded_by=self.request.user).order_by('-created_at')


class ScreenshotDeleteView(LoginRequiredMixin, OwnerOrModeratorMixin, DeleteView):
    model = Screenshot
    success_url = _('my screenshots')
    login_url = '/accounts/login/'
    pk_url_kwarg = 'pk'
    owner_field = 'uploaded_by'

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


@login_required
def check_favorite_screenshot(request, pk):
    try:
        screenshot = Screenshot.objects.get(pk=pk)
        is_favorited = FavoriteScreenshot.objects.filter(user=request.user, screenshot=screenshot).exists()
        return JsonResponse({
            'status': 'success',
            'is_favorited': is_favorited
        })
    except Screenshot.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Screenshot not found'}, status=404)


@login_required
def toggle_favorite_screenshot(request, pk):
    if request.method == 'POST':
        try:
            screenshot = Screenshot.objects.get(pk=pk)

            # prevent users from favoriting their own screenshots
            if screenshot.uploaded_by == request.user:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Cannot favorite own screenshot!'
                }, status=400)

            favorite, created = FavoriteScreenshot.objects.get_or_create(user=request.user, screenshot=screenshot)

            if not created:
                favorite.delete()
                action = 'removed'
                message = 'Screenshot removed from favorites'
            else:
                action = 'added'
                message = 'Screenshot added to favorites'

            sync_screenshot_favorite_counters.delay(screenshot.pk, request.user.pk)

            return JsonResponse({
                'status': 'success',
                'action': action,
                'message': message
            })
        except Screenshot.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Screenshot not found'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
