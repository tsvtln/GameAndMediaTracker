document.addEventListener('DOMContentLoaded', function() {
    const deleteBtns = document.querySelectorAll('.vault-card-delete-btn');
    const modal = document.getElementById('vault-delete-modal');
    const yesBtn = modal.querySelector('.vault-delete-yes');
    const noBtn = modal.querySelector('.vault-delete-no');
    let currentDeleteUrl = null;

    deleteBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            currentDeleteUrl = btn.getAttribute('href');
            modal.classList.add('show');
        });
    });

    yesBtn.addEventListener('click', function() {
        modal.classList.remove('show');
        if (currentDeleteUrl) {
            window.location.href = currentDeleteUrl;
        }
        currentDeleteUrl = null;
    });

    noBtn.addEventListener('click', function() {
        modal.classList.remove('show');
        currentDeleteUrl = null;
    });
});
