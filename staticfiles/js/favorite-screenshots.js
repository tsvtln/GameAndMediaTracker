document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('favorite-screenshot-modal');
    const modalImg = document.getElementById('favorite-screenshot-modal-img');
    const modalGame = document.querySelector('.favorite-screenshot-modal-game');
    const modalPlatform = document.querySelector('.favorite-screenshot-modal-platform');
    const modalUploader = document.querySelector('.favorite-screenshot-modal-uploader');
    const modalClose = document.querySelector('.favorite-screenshot-modal-close');
    const modalRemove = document.querySelector('.favorite-screenshot-modal-remove');
    const modalDownload = document.querySelector('.favorite-screenshot-modal-download');

    // dummy uploader for now
    const dummyUploader = 'Uploaded by: user123';

    // open modal box on View button click
    document.querySelectorAll('.favorite-screenshots-view-btn').forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const card = btn.closest('.favorite-screenshots-card');
            const img = card.querySelector('img');
            const game = card.querySelector('.favorite-screenshots-game').innerText.replace('Game:\n', '').replace('Game:', '').trim();
            const platform = card.querySelector('.favorite-screenshots-platform').innerText.replace('Platform:\n', '').replace('Platform:', '').trim();
            modalImg.src = img.src;
            modalImg.alt = img.alt;
            modalGame.textContent = 'Game: ' + game;
            modalPlatform.textContent = 'Platform: ' + platform;
            // make uploader clickable
            modalUploader.innerHTML = 'Uploaded by: <a href="#" class="favorite-screenshot-modal-uploader-link">user123</a>';
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

    // remove from favorites (dummy)
    modalRemove.addEventListener('click', function() {
        alert('Removed from favorites!');
        modal.style.display = 'none';
    });

    // download (dummy)
    modalDownload.addEventListener('click', function() {
        alert('Download started!');
    });
});
