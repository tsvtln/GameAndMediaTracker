document.addEventListener('DOMContentLoaded', function() {
    const biosInput = document.getElementById('bios-file');
    const biosLabel = document.querySelector('label.upload-file-label[for="bios-file"]');
    if (biosInput && biosLabel) {
        biosInput.addEventListener('change', function() {
            if (biosInput.files.length > 0) {
                biosLabel.textContent = biosInput.files[0].name;
            } else {
                biosLabel.textContent = 'Select BIOS File';
            }
        });
    }
});

