document.addEventListener('DOMContentLoaded', function() {
    // --- ROM file label ---
    const romInput = document.getElementById('id_rom_file');
    const romLabel = document.querySelector('label.upload-file-label[for="id_rom_file"]');
    if (romInput && romLabel) {
        romInput.addEventListener('change', function() {
            if (romInput.files.length > 0) {
                romLabel.textContent = romInput.files[0].name;
            } else {
                romLabel.textContent = 'Select ROM File';
            }
        });
    }

    // --- Box art preview logic ---
    const boxArtInput = document.getElementById('id_box_art');
    const boxArtLabel = document.querySelector('label.upload-file-label[for="id_box_art"]');
    const boxArtPreview = document.getElementById('boxart-preview');
    if (boxArtInput && boxArtLabel && boxArtPreview) {
        boxArtInput.addEventListener('change', function() {
            if (boxArtInput.files.length > 0) {
                boxArtLabel.textContent = boxArtInput.files[0].name;
                const file = boxArtInput.files[0];
                if (file && file.type.match('image.*')) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        boxArtPreview.innerHTML = '<img src="' + e.target.result + '" alt="Box Art Preview">';
                    };
                    reader.readAsDataURL(file);
                } else {
                    boxArtPreview.innerHTML = 'BOX ART PREVIEW';
                }
            } else {
                boxArtLabel.textContent = 'Select Box Art';
                boxArtPreview.innerHTML = 'BOX ART PREVIEW';
            }
        });
    }
});
