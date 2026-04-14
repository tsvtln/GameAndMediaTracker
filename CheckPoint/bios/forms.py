from django import forms
from django.utils.translation import gettext_lazy as gtl
from CheckPoint.bios.models import Bios


class BiosUploadForm(forms.ModelForm):
    class Meta:
        model = Bios
        fields = ['platform', 'bios_file', 'description', 'source']

        widgets = {
            'platform': forms.Select(attrs={
                'class': 'styled-select',
                'id': 'platform',
            }),

            'description': forms.Textarea(attrs={
                'class': 'styled-input',
                'id': 'description',
                'rows': 5,
                'placeholder': 'PlayStation BIOS used by many PS1 emulators.',
            }),

            'source': forms.Select(attrs={
                'class': 'styled-select',
                'id': 'source',
            }),

            'bios_file': forms.FileInput(attrs={
                'class': 'upload-file-input',
                'id': 'bios-file',
                'accept': '.bin,.rom,.zip,.tar.gz,.pup',
            }),
        }

        labels = {
            'platform': 'System / Platform',
            'bios_file': 'BIOS File',
            'description': 'Description',
            'source': 'Upload Source',
        }

        help_texts = {
            'bios_file': gtl('Max size: 5GB. Accepted: .bin .rom .zip .tar.gz .pup'),
        }

    def clean_bios_file(self):
        bios_file = self.cleaned_data.get('bios_file')
        if bios_file:
            # check file size (5GB = 5 * 1024 * 1024 * 1024 bytes = 5 * 1024^3 = 5368709120 bytes)
            max_size = 5368709120
            if bios_file.size > max_size:
                raise forms.ValidationError(gtl('File size cannot exceed 5GB.'))
        return bios_file
