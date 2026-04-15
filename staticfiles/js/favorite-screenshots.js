document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('favorite-screenshot-modal');
    const modalImg = document.getElementById('favorite-screenshot-modal-img');
    const modalGame = document.querySelector('.favorite-screenshot-modal-game');
    const modalPlatform = document.querySelector('.favorite-screenshot-modal-platform');
    const modalUploader = document.querySelector('.favorite-screenshot-modal-uploader');
    const modalClose = document.querySelector('.favorite-screenshot-modal-close');
    const modalRemove = document.querySelector('.favorite-screenshot-modal-remove');
    const modalAdd = document.querySelector('.favorite-screenshot-modal-add');
    const modalDownload = document.querySelector('.favorite-screenshot-modal-download');
    let isFavorited = false;

    // open modal box on View button click
    document.querySelectorAll('.favorite-screenshots-view-btn').forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const card = btn.closest('.favorite-screenshots-card');
            const img = card.querySelector('img');
            const game = card.querySelector('.favorite-screenshots-game').innerText.replace('Game:\n', '').replace('Game:', '').trim();
            const platform = card.querySelector('.favorite-screenshots-platform').innerText.replace('Platform:\n', '').replace('Platform:', '').trim();
            let uploader = 'user123';
            const uploaderSpan = card.querySelector('.favorite-screenshots-uploader');
            if (uploaderSpan) {
                uploader = uploaderSpan.innerText.replace('Uploaded by:', '').trim();
            }
            modalImg.src = img.src;
            modalImg.alt = img.alt;
            modalGame.textContent = 'Game: ' + game;
            modalPlatform.textContent = 'Platform: ' + platform;
            modalUploader.textContent = 'Uploaded by: ' + uploader;
            isFavorited = false;
            if (modalAdd) modalAdd.style.display = 'inline-block';
            if (modalRemove) modalRemove.style.display = 'none';
            modal.style.display = 'flex';
        });
    });

    // close modal box
    modalClose.addEventListener('click', function() {
        modal.style.display = 'none';
    });
    window.addEventListener('click', function(e) {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });

    if (modalAdd) {
        modalAdd.addEventListener('click', function() {
            isFavorited = true;
            modalAdd.style.display = 'none';
            modalRemove.style.display = 'inline-block';
        });
    }

    if (modalRemove) {
        modalRemove.addEventListener('click', function() {
            isFavorited = false;
            modalRemove.style.display = 'none';
            modalAdd.style.display = 'inline-block';
        });
    }

    // if (modalDownload) {
    //     modalDownload.addEventListener('click', function() {
    //         alert('Download started!');
    //     });
    // }
});
