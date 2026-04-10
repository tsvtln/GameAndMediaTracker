document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('password-modal');
    const openBtn = document.getElementById('change-password-btn');
    const closeBtn = document.querySelector('.password-modal-close');

    // oopen modal
    openBtn.addEventListener('click', function(e) {
        e.preventDefault();
        modal.style.display = 'flex';
    });

    // close modal
    closeBtn.addEventListener('click', function() {
        modal.style.display = 'none';
    });
    window.addEventListener('click', function(e) {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });
});

