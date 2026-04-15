from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DeleteView, ListView, DetailView
from django.views import View
from django.urls import reverse_lazy as _
from django.http import FileResponse, Http404, JsonResponse
from CheckPoint.saves.models import Save, SaveVote
from CheckPoint.saves.forms import SaveUploadForm
from CheckPoint.common.permissions import OwnerOrModeratorMixin, CanDeleteContextMixin


def saves_main(request):
    recent_saves = Save.objects.select_related('uploaded_by').order_by('-created_at')[:3]
    user_recent_saves = []
    if request.user.is_authenticated:
        user_recent_saves = Save.objects.filter(uploaded_by=request.user).order_by('-created_at')[:3]

    return render(request, 'saves/saves.html', {
        'recent_saves': recent_saves,
        'user_recent_saves': user_recent_saves,
    })


class SavesAllView(ListView):
    model = Save
    template_name = 'saves/all.html'
    context_object_name = 'saves'
    paginate_by = 20

    def get_queryset(self):
        queryset = Save.objects.select_related('uploaded_by').all()

        # search by game title
        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = queryset.filter(game_title__icontains=search_query)

        # filter by platform
        platform = self.request.GET.get('platform', '')
        if platform:
            queryset = queryset.filter(platform=platform)

        # filter by save type
        save_type = self.request.GET.get('type', '')
        if save_type and save_type != 'all':
            queryset = queryset.filter(save_type=save_type)

        # sort by
        sort_by = self.request.GET.get('sort', 'latest')
        if sort_by == 'downloads':
            queryset = queryset.order_by('-downloads', '-created_at')
        elif sort_by == 'liked':
            queryset = queryset.order_by('-upvotes', '-created_at')
        else:  # latest
            queryset = queryset.order_by('-created_at')

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Attach user vote to each save object
        if self.request.user.is_authenticated:
            save_ids = [save.pk for save in context['saves']]
            user_votes = SaveVote.objects.filter(
                save_file_id__in=save_ids,
                user=self.request.user
            )
            votes_dict = {vote.save_file_id: vote.vote_type for vote in user_votes}

            # Add user_vote_type attribute to each save
            for save in context['saves']:
                save.user_vote_type = votes_dict.get(save.pk, None)
        else:
            for save in context['saves']:
                save.user_vote_type = None
        
        return context


class SavesVaultView(LoginRequiredMixin, ListView):
    model = Save
    template_name = 'saves/vault.html'
    context_object_name = 'saves'
    paginate_by = 20
    login_url = '/accounts/login/'

    def get_queryset(self):
        # only show saves uploaded by the current user
        queryset = Save.objects.filter(uploaded_by=self.request.user)

        # search by game title
        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = queryset.filter(game_title__icontains=search_query)

        # filter by platform
        platform = self.request.GET.get('platform', '')
        if platform:
            queryset = queryset.filter(platform=platform)

        # filter by game
        game = self.request.GET.get('game', '')
        if game:
            queryset = queryset.filter(game_title=game)

        # filter by save type
        save_type = self.request.GET.get('type', '')
        if save_type and save_type != 'all':
            queryset = queryset.filter(save_type=save_type)

        # sort by
        sort_by = self.request.GET.get('sort', 'latest')
        if sort_by == 'name':
            queryset = queryset.order_by('game_title')
        elif sort_by == 'platform':
            queryset = queryset.order_by('platform', '-created_at')
        else:  # latest
            queryset = queryset.order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_saves = Save.objects.filter(uploaded_by=self.request.user)
        context['total_saves'] = user_saves.count()
        context['total_platforms'] = user_saves.values('platform').distinct().count()
        total_bytes = sum(save.save_file.size for save in user_saves if save.save_file)
        context['total_storage'] = self._sizeof_fmt(total_bytes)
        context['user_games'] = user_saves.values_list('game_title', flat=True).distinct().order_by('game_title')

        return context

    # Source - https://stackoverflow.com/a/1094933
    # Posted by Sridhar Ratnakumar, modified by community. See post 'Timeline' for change history
    # Retrieved 2026-04-15, License - CC BY-SA 4.0

    def _sizeof_fmt(self, num, suffix="B"):
        for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
            if abs(num) < 1024.0:
                return f"{num:3.1f}{unit}{suffix}"
            num /= 1024.0
        return f"{num:.1f}Yi{suffix}"


class SaveUploadView(LoginRequiredMixin, CreateView):
    model = Save
    form_class = SaveUploadForm
    template_name = 'saves/upload.html'
    login_url = '/accounts/login/'
    success_url = _('saves vault page')

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        messages.success(self.request, f'Save file for "{form.instance.game_title}" uploaded successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error uploading save file. Please fill all required fields!')
        return super().form_invalid(form)


class SaveDetailView(CanDeleteContextMixin, DetailView):
    model = Save
    template_name = 'saves/details.html'
    context_object_name = 'save'
    pk_url_kwarg = 'pk'
    owner_field = 'uploaded_by'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        save_obj = self.get_object()

        if self.request.user.is_authenticated:
            user_vote = SaveVote.objects.filter(save_file=save_obj, user=self.request.user).first()
            context['user_vote'] = user_vote.vote_type if user_vote else None
        else:
            context['user_vote'] = None

        return context


class SaveDeleteView(LoginRequiredMixin, OwnerOrModeratorMixin, DeleteView):
    model = Save
    success_url = _('saves all page')
    login_url = '/accounts/login/'
    pk_url_kwarg = 'pk'
    owner_field = 'uploaded_by'

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        save_obj = self.get_object()
        messages.success(request, f'Save file for "{save_obj.game_title}" deleted successfully!')
        return super().delete(request, *args, **kwargs)


class SaveDownloadView(View):
    def get(self, request, pk):
        try:
            save = Save.objects.get(pk=pk)
            save.increment_downloads()
            response = FileResponse(save.save_file.open('rb'))
            response['Content-Disposition'] = f'attachment; filename="{save.game_title}.{save.save_file.name.split(".")[-1]}"'

            return response

        except Save.DoesNotExist:
            raise Http404("Save file not found")


@login_required
def save_vote(request, pk):
    if request.method == 'POST':
        save_obj = Save.objects.get(pk=pk)
        vote_type = request.POST.get('vote_type')
        existing_vote = SaveVote.objects.filter(save_file=save_obj, user=request.user).first()

        if existing_vote:
            if existing_vote.vote_type == vote_type:
                if vote_type == 'upvote':
                    save_obj.upvotes -= 1
                else:
                    save_obj.downvotes -= 1
                existing_vote.delete()
                save_obj.save(update_fields=['upvotes', 'downvotes'])
                return JsonResponse({
                    'status': 'success',
                    'action': 'removed',
                    'upvotes': save_obj.upvotes,
                    'downvotes': save_obj.downvotes,
                    'rating': save_obj.rating
                })
            else:
                if existing_vote.vote_type == 'upvote':
                    save_obj.upvotes -= 1
                    save_obj.downvotes += 1
                else:
                    save_obj.downvotes -= 1
                    save_obj.upvotes += 1
                existing_vote.vote_type = vote_type
                existing_vote.save()
                save_obj.save(update_fields=['upvotes', 'downvotes'])
                return JsonResponse({
                    'status': 'success',
                    'action': 'changed',
                    'vote_type': vote_type,
                    'upvotes': save_obj.upvotes,
                    'downvotes': save_obj.downvotes,
                    'rating': save_obj.rating
                })
        else:
            SaveVote.objects.create(save_file=save_obj, user=request.user, vote_type=vote_type)
            if vote_type == 'upvote':
                save_obj.upvotes += 1
            else:
                save_obj.downvotes += 1
            save_obj.save(update_fields=['upvotes', 'downvotes'])
            return JsonResponse({
                'status': 'success',
                'action': 'added',
                'vote_type': vote_type,
                'upvotes': save_obj.upvotes,
                'downvotes': save_obj.downvotes,
                'rating': save_obj.rating
            })
    return JsonResponse({'status': 'error'}, status=500)
