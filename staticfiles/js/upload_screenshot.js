document.addEventListener('DOMContentLoaded', function() {
    const screenshotInput = document.getElementById('screenshot-file');
    const screenshotLabel = document.querySelector('label.upload-file-label[for="screenshot-file"]');
    const screenshotPreview = document.getElementById('screenshot-preview');
    const screenshotDrop = document.getElementById('screenshot-drop');

    if (screenshotInput && screenshotLabel) {
        screenshotInput.addEventListener('change', function() {
            if (screenshotInput.files.length > 0) {
                screenshotLabel.textContent = screenshotInput.files[0].name;
                if (screenshotLabel.textContent.length > 30) {
                    screenshotLabel.textContent = screenshotLabel.textContent.slice(0, 25) + '...' + screenshotLabel.textContent.slice(-4);
                }
                const file = screenshotInput.files[0];
                if (file && file.type.match('image.*')) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        screenshotPreview.innerHTML = '<img src="' + e.target.result + '" alt="Screenshot Preview" style="max-width:100%;max-height:220px;border-radius:8px;box-shadow:0 0 12px #49ff18;">';
                    };
                    reader.readAsDataURL(file);
                } else {
                    screenshotPreview.innerHTML = 'SCREENSHOT PREVIEW';
                }
            } else {
                screenshotLabel.textContent = 'Select Screenshot';
                screenshotPreview.innerHTML = 'SCREENSHOT PREVIEW';
            }
        });
    }

    if (screenshotDrop) {
        screenshotDrop.addEventListener('dragover', function(e) {
            e.preventDefault();
            screenshotDrop.classList.add('drag-active');
        });
        screenshotDrop.addEventListener('dragleave', function(e) {
            e.preventDefault();
            screenshotDrop.classList.remove('drag-active');
        });
        screenshotDrop.addEventListener('drop', function(e) {
            e.preventDefault();
            screenshotDrop.classList.remove('drag-active');
            if (e.dataTransfer.files && e.dataTransfer.files[0]) {
                screenshotInput.files = e.dataTransfer.files;
                screenshotInput.dispatchEvent(new Event('change'));
            }
        });
    }
});
