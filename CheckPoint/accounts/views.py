from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView as DjangoPasswordChangeView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy as _
from django.views.generic import CreateView, DetailView, UpdateView, TemplateView, ListView, DeleteView
from CheckPoint.accounts.models import AppUser, Profile, Screenshot
from CheckPoint.common.permissions import OwnerOrModeratorMixin
from CheckPoint.accounts.forms import (
    AppUserRegistrationForm,
    AppUserLoginForm,
    ProfileUpdateForm,
    UserUpdateForm,
    CustomPasswordChangeForm,
    ScreenshotUploadForm
)


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
        # redirect to home page when logged in
        # NOTE: if have time to make it to redirect to the last page visited that redirected to login
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


class FavoriteRomsView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/favorite-roms.html'


class FavoriteScreenshotsView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/favorite-screenshots.html'


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


# keep these function-based views for now (will convert later if needed)
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
    paginate_by = 9

    def get_queryset(self):
        return Screenshot.objects.select_related('uploaded_by').order_by('-created_at')


class TopRatedScreenshotsView(ListView):
    model = Screenshot
    template_name = 'screenshots/top-rated.html'
    context_object_name = 'screenshots'
    paginate_by = 9

    def get_queryset(self):
        return Screenshot.objects.select_related('uploaded_by').order_by('-likes', '-created_at')


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

    def delete(self, request, *args, **kwargs):
        screenshot = self.get_object()

        # decrement screenshot count on user profile
        screenshot.uploaded_by.profile.decrement_screenshots()

        messages.success(request, f'Screenshot for "{screenshot.game_name}" deleted successfully!')
        return super().delete(request, *args, **kwargs)
