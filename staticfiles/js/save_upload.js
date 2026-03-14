document.addEventListener('DOMContentLoaded', function() {
    const saveInput = document.getElementById('save-file');
    const saveLabel = document.querySelector('label.upload-file-label[for="save-file"]');
    if (saveInput && saveLabel) {
        saveInput.addEventListener('change', function() {
            if (saveInput.files.length > 0) {
                saveLabel.textContent = saveInput.files[0].name;
            } else {
                saveLabel.textContent = 'Select Save File';
            }
        });
    }

    // mission field toggle
    const progressSelect = document.getElementById('progress');
    const missionField = document.getElementById('mission-field');
    if (progressSelect && missionField) {
        progressSelect.addEventListener('change', function() {
            if (progressSelect.value === 'mission') {
                missionField.style.display = 'block';
            } else {
                missionField.style.display = 'none';
            }
        });
    }

    const imageInput = document.getElementById('save-image');
    const imageLabel = document.querySelector('label.upload-file-label[for="save-image"]');
    const imagePreview = document.getElementById('save-image-preview');
    if (imageInput && imageLabel && imagePreview) {
        imageInput.addEventListener('change', function() {
            if (imageInput.files.length > 0) {
                imageLabel.textContent = imageInput.files[0].name;
                const file = imageInput.files[0];
                const reader = new FileReader();
                reader.onload = function(e) {
                    imagePreview.style.display = 'block';
                    imagePreview.innerHTML = '<img src="' + e.target.result + '" alt="Preview" style="max-width:180px; max-height:180px; border-radius:8px; box-shadow:0 0 8px #49ff18;">';
                };
                reader.readAsDataURL(file);
            } else {
                imageLabel.textContent = 'Select Image';
                imagePreview.style.display = 'none';
                imagePreview.innerHTML = '';
            }
        });
    }
});
