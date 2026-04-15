document.addEventListener('DOMContentLoaded', function() {
    let deleteModal = document.getElementById('delete-screenshot-modal');
    let deleteModalClose = document.querySelector('.delete-screenshot-modal-close');
    let cancelDeleteBtn = document.querySelector('.cancel-delete-btn');
    let deleteForm = document.getElementById('delete-screenshot-form');

    document.querySelectorAll('.favorite-screenshots-delete-btn').forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            let screenshotId = btn.getAttribute('data-screenshot-id');
            if (screenshotId) {
                let deleteUrl = `/accounts/screenshots/delete/${screenshotId}/`;
                deleteForm.setAttribute('action', deleteUrl);
                deleteModal.style.display = 'flex';
            }
        });
    });

    if (deleteModalClose) {
        deleteModalClose.addEventListener('click', function() {
            deleteModal.style.display = 'none';
        });
    }

    if (cancelDeleteBtn) {
        cancelDeleteBtn.addEventListener('click', function() {
            deleteModal.style.display = 'none';
        });
    }

    window.addEventListener('click', function(e) {
        if (e.target === deleteModal) {
            deleteModal.style.display = 'none';
        }
    });

    let modalDownload = document.querySelector('.favorite-screenshot-modal-download');
    if (modalDownload) {
        modalDownload.addEventListener('click', function() {
            let modalImg = document.getElementById('favorite-screenshot-modal-img');
            if (modalImg && modalImg.src) {
                let link = document.createElement('a');
                link.href = modalImg.src;
                link.download = 'screenshot.png';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            }
        });
    }
});

