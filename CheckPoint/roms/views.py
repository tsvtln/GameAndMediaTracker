from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, DetailView, DeleteView, ListView
from django.views import View
from django.urls import reverse_lazy
from django.db.models import Count, Avg
from django.http import FileResponse, Http404
from CheckPoint.roms.models import Rom, Comment, Review
from CheckPoint.roms.forms import RomUploadForm, CommentForm, ReviewForm


def roms(request):
    return render(request, 'roms/roms.html')


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


def newly_added(request):
    return render(request, 'roms/newly-added.html')


def trending(request):
    return render(request, 'roms/trending.html')


def most_downloaded(request):
    return render(request, 'roms/most-downloaded.html')


def genres(request):
    return render(request, 'roms/genres.html')


def genre_action(request):
    return render(request, 'roms/genres/action.html')


def genre_adventure(request):
    return render(request, 'roms/genres/adventure.html')


def genre_platformer(request):
    return render(request, 'roms/genres/platformer.html')


def genre_rpg(request):
    return render(request, 'roms/genres/rpg.html')


def genre_fighting(request):
    return render(request, 'roms/genres/fighting.html')


def genre_shooter(request):
    return render(request, 'roms/genres/shooter.html')


def genre_puzzle(request):
    return render(request, 'roms/genres/puzzle.html')


def genre_sports(request):
    return render(request, 'roms/genres/sports.html')


def genre_racing(request):
    return render(request, 'roms/genres/racing.html')


def genre_strategy(request):
    return render(request, 'roms/genres/strategy.html')


def genre_simulation(request):
    return render(request, 'roms/genres/simulation.html')


def genre_horror(request):
    return render(request, 'roms/genres/horror.html')


def platforms(request):
    return render(request, 'roms/platforms.html')


def platform_nes(request):
    return render(request, 'roms/platforms/nes.html')


def platform_famicom(request):
    return render(request, 'roms/platforms/famicom.html')


def platform_snes(request):
    return render(request, 'roms/platforms/snes.html')


def platform_super_famicom(request):
    return render(request, 'roms/platforms/super-famicom.html')


def platform_n64(request):
    return render(request, 'roms/platforms/n64.html')


def platform_gamecube(request):
    return render(request, 'roms/platforms/gamecube.html')


def platform_wii(request):
    return render(request, 'roms/platforms/wii.html')


def platform_wii_u(request):
    return render(request, 'roms/platforms/wii-u.html')


def platform_nintendo_switch(request):
    return render(request, 'roms/platforms/nintendo-switch.html')


def platform_gameboy(request):
    return render(request, 'roms/platforms/gameboy.html')


def platform_gbc(request):
    return render(request, 'roms/platforms/gbc.html')


def platform_gba(request):
    return render(request, 'roms/platforms/gba.html')


def platform_nintendo_ds(request):
    return render(request, 'roms/platforms/nintendo-ds.html')


def platform_nintendo_3ds(request):
    return render(request, 'roms/platforms/nintendo-3ds.html')


def platform_sega_master_system(request):
    return render(request, 'roms/platforms/sega-master-system.html')


def platform_genesis(request):
    return render(request, 'roms/platforms/genesis.html')


def platform_sega_cd(request):
    return render(request, 'roms/platforms/sega-cd.html')


def platform_32x(request):
    return render(request, 'roms/platforms/32x.html')


def platform_sega_saturn(request):
    return render(request, 'roms/platforms/sega-saturn.html')


def platform_sega_dreamcast(request):
    return render(request, 'roms/platforms/sega-dreamcast.html')


def platform_game_gear(request):
    return render(request, 'roms/platforms/game-gear.html')


def platform_ps1(request):
    return render(request, 'roms/platforms/ps1.html')


def platform_ps2(request):
    return render(request, 'roms/platforms/ps2.html')


def platform_ps3(request):
    return render(request, 'roms/platforms/ps3.html')


def platform_psp(request):
    return render(request, 'roms/platforms/psp.html')


def platform_vita(request):
    return render(request, 'roms/platforms/vita.html')


def platform_xbox(request):
    return render(request, 'roms/platforms/xbox.html')


def platform_xbox_360(request):
    return render(request, 'roms/platforms/xbox-360.html')


def platform_xbox_one(request):
    return render(request, 'roms/platforms/xbox-one.html')


def platform_atari(request):
    return render(request, 'roms/platforms/atari.html')


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
        return reverse_lazy(
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


class RomDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Rom
    success_url = reverse_lazy('roms page')
    login_url = '/accounts/login/'
    pk_url_kwarg = 'pk'

    def test_func(self):
        rom = self.get_object()
        user = self.request.user

        # allow if user is_staff or is in Moderators group
        if user.is_staff:
            return True

        if user.groups.filter(name='Moderators').exists():
            return True

        # allow if user is the uploader
        if rom.uploaded_by == user:
            return True
        return False

    def delete(self, request, *args, **kwargs):
        rom = self.get_object()
        messages.success(request, f'ROM "{rom.title}" deleted successfully!')
        return super().delete(request, *args, **kwargs)


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    pk_url_kwarg = 'pk'

    def test_func(self):
        comment = self.get_object()
        user = self.request.user

        # allow if user is_staff or is in Moderators group
        if user.is_staff:
            return True
        if user.groups.filter(name='Moderators').exists():
            return True

        # allow if user is the comment author
        if comment.user == user:
            return True
        return False

    def get_success_url(self):
        return reverse_lazy(
            'roms details',
            kwargs={'pk': self.object.rom.pk}
        )

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Comment deleted successfully!')
        return super().delete(request, *args, **kwargs)


class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    pk_url_kwarg = 'pk'

    def test_func(self):
        review = self.get_object()
        user = self.request.user

        # allow if user is_staff or is in Moderators group
        if user.is_staff:
            return True
        if user.groups.filter(name='Moderators').exists():
            return True

        # allow if user is the review author
        if review.user == user:
            return True
        return False

    def get_success_url(self):
        return reverse_lazy(
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
