document.addEventListener('DOMContentLoaded', function() {
    const biosInput = document.getElementById('bios-file');
    const biosLabel = document.querySelector('label.bios-upload-file-label[for="bios-file"]');
    biosInput.addEventListener('change', function() {
        if (biosInput.files.length > 0) {
            biosLabel.textContent = biosInput.files[0].name;
        } else {
            biosLabel.textContent = 'Select BIOS File';
        }
    });
});

