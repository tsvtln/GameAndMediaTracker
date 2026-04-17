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
    let currentScreenshotId = null;
    let currentCardButton = null;

    // get CSRF token
    function getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value ||
               document.cookie.split('; ').find(row => row.startsWith('csrftoken='))?.split('=')[1];
    }

    // toggle favorite via AJAX
    function toggleFavorite(screenshotId, button) {
        fetch(`/accounts/screenshots/favorite/${screenshotId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCsrfToken(),
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                if (data.action === 'added') {
                    if (button) {
                        button.classList.remove('favorite-screenshots-add-btn');
                        button.classList.add('favorite-screenshots-remove-btn');
                        button.textContent = '❤ Remove';
                        button.setAttribute('data-favorited', 'true');
                    }
                    if (modalAdd && modalRemove) {
                        modalAdd.style.display = 'none';
                        modalRemove.style.display = 'inline-block';
                    }
                } else {
                    if (button) {
                        button.classList.remove('favorite-screenshots-remove-btn');
                        button.classList.add('favorite-screenshots-add-btn');
                        button.textContent = '❤ Favorite';
                        button.setAttribute('data-favorited', 'false');
                    }
                    if (modalAdd && modalRemove) {
                        modalRemove.style.display = 'none';
                        modalAdd.style.display = 'inline-block';
                    }
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    // handle favorite button clicks on cards
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('favorite-toggle-btn')) {
            e.preventDefault();
            const screenshotId = e.target.getAttribute('data-screenshot-id');
            toggleFavorite(screenshotId, e.target);
        }
    });

    // open modal box on View button click
    document.querySelectorAll('.favorite-screenshots-view-btn').forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const card = btn.closest('.favorite-screenshots-card');
            const img = card.querySelector('img');
            const game = card.querySelector('.favorite-screenshots-game').innerText.replace('Game:\n', '').replace('Game:', '').trim();
            const platform = card.querySelector('.favorite-screenshots-platform').innerText.replace('Platform:\n', '').replace('Platform:', '').trim();
            let uploader = 'Unknown';
            const uploaderSpan = card.querySelector('.favorite-screenshots-uploader');
            if (uploaderSpan) {
                uploader = uploaderSpan.innerText.replace('Uploaded by:', '').replace('Uploaded by:\n', '').trim();
            }

            currentScreenshotId = card.getAttribute('data-screenshot-id');
            currentCardButton = card.querySelector('.favorite-toggle-btn');

            modalImg.src = img.src;
            modalImg.alt = img.alt;
            modalGame.textContent = 'Game: ' + game;
            modalPlatform.textContent = 'Platform: ' + platform;
            modalUploader.textContent = 'Uploaded by: ' + uploader;

            // check if this is user's own screenshot (button will be disabled)
            const isOwnScreenshot = card.querySelector('.favorite-screenshots-add-btn[disabled]') !== null;

            // set modal button state based on card button state
            if (currentCardButton && modalAdd && modalRemove) {
                const isFavorited = currentCardButton.getAttribute('data-favorited') === 'true';
                if (isFavorited) {
                    modalAdd.style.display = 'none';
                    modalRemove.style.display = 'inline-block';
                } else {
                    modalAdd.style.display = 'inline-block';
                    modalRemove.style.display = 'none';
                }
            } else if (isOwnScreenshot) {
                // hide both favorite buttons if it's user's own screenshot
                if (modalAdd) modalAdd.style.display = 'none';
                if (modalRemove) modalRemove.style.display = 'none';
            } else {
                // no toggle button means user is not authenticated or other reason
                if (modalAdd) modalAdd.style.display = 'none';
                if (modalRemove) modalRemove.style.display = 'none';
            }

            modal.style.display = 'flex';
        });
    });

    // close modal box
    if (modalClose) {
        modalClose.addEventListener('click', function() {
            modal.style.display = 'none';
        });
    }

    window.addEventListener('click', function(e) {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });

    // modal add to favorites
    if (modalAdd) {
        modalAdd.addEventListener('click', function() {
            if (currentScreenshotId) {
                toggleFavorite(currentScreenshotId, currentCardButton);
            }
        });
    }

    // modal remove from favorites
    if (modalRemove) {
        modalRemove.addEventListener('click', function() {
            if (currentScreenshotId) {
                toggleFavorite(currentScreenshotId, currentCardButton);
            }
        });
    }

    // download screenshot
    if (modalDownload) {
        modalDownload.addEventListener('click', function() {
            if (modalImg && modalImg.src) {
                const link = document.createElement('a');
                link.href = modalImg.src;
                link.download = 'screenshot.png';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            }
        });
    }
});
