document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('password-modal');
    const openBtn = document.getElementById('change-password-btn');
    const closeBtn = document.querySelector('.password-modal-close');
    const saveBtn = document.querySelector('.password-modal-save-btn');

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

    // dummy save handler
    saveBtn.addEventListener('click', function() {
        alert('Password changed! (not implemented)');
        modal.style.display = 'none';
    });
});

