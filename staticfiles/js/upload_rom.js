document.addEventListener('DOMContentLoaded', function() {
    const romInput = document.getElementById('rom-file');
    const romLabel = document.querySelector('label.upload-rom-file-label[for="rom-file"]');
    romInput.addEventListener('change', function() {
        if (romInput.files.length > 0) {
            romLabel.textContent = romInput.files[0].name;
        } else {
            romLabel.textContent = 'Select ROM File';
        }
    });

    const boxArtInput = document.getElementById('box-art');
    const boxArtLabel = document.querySelector('label.upload-rom-file-label[for="box-art"]');
    const boxArtPreview = document.getElementById('boxart-preview');
    boxArtInput.addEventListener('change', function() {
        if (boxArtInput.files.length > 0) {
            boxArtLabel.textContent = boxArtInput.files[0].name;
            // Show preview
            const file = boxArtInput.files[0];
            const reader = new FileReader();
            reader.onload = function(e) {
                boxArtPreview.innerHTML = '<img src="' + e.target.result + '" alt="Box Art Preview">';
            };
            reader.readAsDataURL(file);
        } else {
            boxArtLabel.textContent = 'Select Box Art';
            boxArtPreview.innerHTML = 'BOX ART PREVIEW';
        }
    });
});
