document.addEventListener('DOMContentLoaded', function() {
    let upvoteBtns = document.querySelectorAll('.save-card-upvote-btn');
    let downvoteBtns = document.querySelectorAll('.save-card-downvote-btn');

    function getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
    }

    function handleVote(saveId, voteType, button) {
        console.log('handleVote called:', saveId, voteType);
        let formData = new FormData();
        formData.append('vote_type', voteType);
        formData.append('csrfmiddlewaretoken', getCsrfToken());

        fetch(`/saves/vote/${saveId}/`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCsrfToken(),
            }
        })
        .then(response => response.json())
        .then(data => {
            // console.log('Vote response:', data);
            if (data.status === 'success') {
                let saveCard = button.closest('.save-card, .save-details-actions');
                let upvoteBtn = saveCard.querySelector('.save-card-upvote-btn');
                let downvoteBtn = saveCard.querySelector('.save-card-downvote-btn');
                let upvoteImg = upvoteBtn.querySelector('.save-card-vote-icon');
                let downvoteImg = downvoteBtn.querySelector('.save-card-vote-icon');
                if (data.action === 'added' || data.action === 'changed') {
                    if (data.vote_type === 'upvote') {
                        upvoteImg.src = upvoteImg.src.replace('upvote.webp', 'upvoted.webp');
                        downvoteImg.src = downvoteImg.src.replace('downvoted.webp', 'downvote.webp');
                    } else {
                        downvoteImg.src = downvoteImg.src.replace('downvote.webp', 'downvoted.webp');
                        upvoteImg.src = upvoteImg.src.replace('upvoted.webp', 'upvote.webp');
                    }
                } else if (data.action === 'removed') {
                    upvoteImg.src = upvoteImg.src.replace('upvoted.webp', 'upvote.webp');
                    downvoteImg.src = downvoteImg.src.replace('downvoted.webp', 'downvote.webp');
                }
                let ratingElement = saveCard.querySelector('.save-card-meta:has(.rom-details-rating-star)');
                if (ratingElement) {
                    ratingElement.innerHTML = `Rating:<br> <span class="rom-details-rating-star">⭐</span>${data.rating}`;
                }
                let detailRating = document.querySelector('.save-details-rating');
                if (detailRating) {
                    detailRating.textContent = `Rating: ⭐${data.rating} (${data.upvotes} 👍 / ${data.downvotes} 👎)`;
                }
            }
        })
        .catch(error => console.error('Vote error:', error));
    }
    upvoteBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            let saveId = this.dataset.saveId;
            handleVote(saveId, 'upvote', this);
        });
    });
    downvoteBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            let saveId = this.dataset.saveId;
            handleVote(saveId, 'downvote', this);
        });
    });
});

