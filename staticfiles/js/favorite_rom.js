document.addEventListener('DOMContentLoaded', function() {
    const favoriteBtn = document.getElementById('favorite-rom-btn');

    if (!favoriteBtn) return;

    const romId = favoriteBtn.dataset.romId;
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    favoriteBtn.addEventListener('click', function(e) {
        e.preventDefault();

        fetch(`/roms/favorite/${romId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            // data.is_favorited = undefined;
            if (data.status === 'success') {
                const heartIcon = favoriteBtn.querySelector('img');
                if (data.is_favorited) {
                    heartIcon.src = '/staticfiles/images/icons/heart_full.png';
                    heartIcon.alt = 'Remove from favorites';
                } else {
                    heartIcon.src = '/staticfiles/images/icons/heart_empty.png';
                    heartIcon.alt = 'Add to favorites';
                }
            } else {
                alert(data.message || 'Something broke. Check the code.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to update favorites');
        });
    });
});


