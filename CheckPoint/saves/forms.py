from django import forms
from django.utils.translation import gettext_lazy as gtl
from CheckPoint.saves.models import Save


class SaveUploadForm(forms.ModelForm):
    class Meta:
        model = Save
        fields = [
            'game_title',
            'platform',
            'save_type',
            'progress',
            'mission_detail',
            'description',
            'completion',
            'save_file',
            'save_image'
        ]
        widgets = {
            'game_title': forms.TextInput(attrs={
                'id': 'game-title',
                'placeholder': 'GTA San Andreas',
            }),

            'platform': forms.Select(attrs={
                'id': 'platform',
            }),

            'save_type': forms.Select(attrs={
                'id': 'save-type',
            }),

            'progress': forms.Select(attrs={
                'id': 'progress',
                'onchange': 'toggleMissionField()',
            }),

            'mission_detail': forms.TextInput(attrs={
                'id': 'mission-detail',
                'placeholder': 'After mission "Black Project"',
            }),

            'description': forms.Textarea(attrs={
                'id': 'description',
                'rows': 4,
                'placeholder': 'Describe your save file, progress, or any special instructions...',
                'class': 'save-upload-description',
            }),

            'completion': forms.NumberInput(attrs={
                'id': 'completion',
                'type': 'range',
                'min': '0',
                'max': '100',
                'value': '0',
                'step': '1',
                'oninput': "document.getElementById('completion-value').textContent = this.value + '%'",
            }),

            'save_file': forms.FileInput(attrs={
                'id': 'save-file',
                'class': 'upload-file-input',
                'accept': '.zip,.rar,.7z,.sav,.srm,.state,.dat',
                'style': 'display:none;',
            }),

            'save_image': forms.FileInput(attrs={
                'id': 'save-image',
                'class': 'upload-file-input',
                'accept': '.png,.jpg,.jpeg,.webp',
                'style': 'display:none;',
            }),
        }

        labels = {
            'game_title': 'Game Title',
            'platform': 'Platform',
            'save_type': 'Save Type',
            'progress': 'Game Progress',
            'mission_detail': 'Specific Mission:',
            'description': 'Description',
            'completion': 'Completion Percentage',
            'save_file': 'Save File',
            'save_image': 'Upload Picture',
        }

    def clean_save_file(self):
        save_file = self.cleaned_data.get('save_file')
        if save_file:
            # MAX 50MB = 50 * 1024 * 1024 = 52,428,800 bytes
            max_size = 52428800
            if save_file.size > max_size:
                raise forms.ValidationError(gtl('File size cannot exceed 50MB.'))
        return save_file

    def clean_save_image(self):
        save_image = self.cleaned_data.get('save_image')
        if save_image:
            # MAX 10MB = 10 * 1024 * 1024 = 10,485,760 bytes
            max_size = 10485760
            if save_image.size > max_size:
                raise forms.ValidationError(gtl('Image size cannot exceed 10MB.'))
        return save_image
