document.addEventListener('DOMContentLoaded', function() {
    const deleteBtns = document.querySelectorAll('.vault-card-delete-btn');
    const modal = document.getElementById('vault-delete-modal');
    const yesBtn = modal.querySelector('.vault-delete-yes');
    const noBtn = modal.querySelector('.vault-delete-no');
    let currentDeleteBtn = null;

    deleteBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            currentDeleteBtn = btn;
            modal.classList.add('show');
        });
    });

    yesBtn.addEventListener('click', function() {
        modal.classList.remove('show');
        // note: add actual delete logic here later, to remove the records from db and all that
        if (currentDeleteBtn) {
            const card = currentDeleteBtn.closest('.vault-card');
            if (card) card.remove();
        }
        currentDeleteBtn = null;
    });

    noBtn.addEventListener('click', function() {
        modal.classList.remove('show');
        currentDeleteBtn = null;
    });
});
