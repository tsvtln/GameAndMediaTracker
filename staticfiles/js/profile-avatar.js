document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('avatar-modal');
    const openBtn = document.getElementById('change-avatar-btn');
    const closeBtn = document.querySelector('.avatar-modal-close');
    const uploadInput = document.getElementById('avatar-upload-input');
    const previewImg = document.getElementById('avatar-preview-img');
    const avatarForm = document.getElementById('avatar-upload-form');

    // Open modal
    openBtn.addEventListener('click', function(e) {
        e.preventDefault();
        modal.style.display = 'flex';
    });

    // Close modal
    closeBtn.addEventListener('click', function() {
        modal.style.display = 'none';
    });
    window.addEventListener('click', function(e) {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });

    // Preview avatar
    uploadInput.addEventListener('change', function() {
        const file = uploadInput.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                previewImg.src = e.target.result;
            };
            reader.readAsDataURL(file);
        }
    });
});

