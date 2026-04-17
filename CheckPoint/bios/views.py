from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, DeleteView, ListView
from django.views import View
from django.urls import reverse_lazy as _
from django.http import FileResponse, Http404
from CheckPoint.bios.models import Bios
from CheckPoint.bios.forms import BiosUploadForm
from CheckPoint.common.permissions import OwnerOrModeratorMixin, ModeratorOrVerifiedMixin
from CheckPoint.bios.tasks import increment_bios_downloads


def bios(request):
    recent_bios = Bios.objects.select_related('uploaded_by').order_by('-created_at')[:3]
    return render(request, 'bios/bios.html', {'recent_bios': recent_bios})


def bios_faq(request):
    return render(request, 'bios/bios-faq.html')


def bios_legal(request):
    return render(request, 'bios/bios-legal.html')


def bios_comp(request):
    return render(request, 'bios/bios-comp.html')


class BiosUploadView(LoginRequiredMixin, ModeratorOrVerifiedMixin, CreateView):
    model = Bios
    form_class = BiosUploadForm
    template_name = 'bios/bios-upload.html'
    login_url = '/accounts/login/'
    success_url = _('bios all files')

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        messages.success(self.request, f'BIOS file for {form.instance.platform} uploaded successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error uploading BIOS file. Please fill all required fields!')
        return super().form_invalid(form)


class BiosAllFilesView(ListView):
    model = Bios
    template_name = 'bios/bios-all-files.html'
    context_object_name = 'bios_files'

    def get_queryset(self):
        # searching
        queryset = Bios.objects.select_related('uploaded_by').all()

        # by filename
        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = queryset.filter(bios_file__icontains=search_query)

        # by platform
        platform = self.request.GET.get('platform', '')
        if platform:
            queryset = queryset.filter(platform=platform)

        # sort by
        sort_by = self.request.GET.get('sort', 'date')
        if sort_by == 'name':
            queryset = queryset.order_by('bios_file')
        elif sort_by == 'platform':
            queryset = queryset.order_by('platform', '-created_at')
        else:  # date
            queryset = queryset.order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # sort BIOS files by platform
        bios_by_platform = {}
        for b in self.get_queryset():
            if b.platform not in bios_by_platform:
                bios_by_platform[b.platform] = []
            bios_by_platform[b.platform].append(b)

        context['bios_by_platform'] = bios_by_platform
        return context


class BiosDeleteView(LoginRequiredMixin, OwnerOrModeratorMixin, DeleteView):
    model = Bios
    success_url = _('bios all files')
    login_url = '/accounts/login/'
    pk_url_kwarg = 'pk'
    owner_field = 'uploaded_by'

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        bios_object = self.get_object()
        messages.success(request, f'BIOS file for {bios_object.platform} deleted successfully!')
        return super().delete(request, *args, **kwargs)


class BiosDownloadView(View):
    def get(self, request, pk):
        try:
            bios_object = Bios.objects.get(pk=pk)
            increment_bios_downloads.delay(bios_object.pk)
            response = FileResponse(bios_object.bios_file.open('rb'))
            response['Content-Disposition'] = f'attachment; filename="{bios_object.bios_file.name.split("/")[-1]}"'
            return response
        except Bios.DoesNotExist:
            raise Http404("BIOS file not found")
