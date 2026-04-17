document.addEventListener('DOMContentLoaded', function() {
    const writeCommentBtn = document.getElementById('write-comment-btn');
    const writeReviewBtn = document.getElementById('write-review-btn');
    const commentForm = document.getElementById('comment-form');
    const reviewForm = document.getElementById('review-form');
    const buttons = document.querySelector('.rom-details-interactive-buttons');
    const cancelCommentBtn = document.getElementById('cancel-comment-btn');
    const cancelReviewBtn = document.getElementById('cancel-review-btn');
    const stars = document.querySelectorAll('.rom-details-rating-stars .star');
    let selectedRating = 0;

    if (writeCommentBtn) {
        writeCommentBtn.addEventListener('click', function() {
            buttons.style.display = 'none';
            commentForm.style.display = 'flex';

            const commentIdField = document.getElementById('comment-id');
            if (commentIdField) {
                commentIdField.value = '';
            }

            document.getElementById('comment-text').value = '';

            const submitBtn = commentForm.querySelector('.rom-details-submit-btn');
            if (submitBtn) {
                submitBtn.textContent = 'Submit';
            }
        });
    }
    if (writeReviewBtn) {
        writeReviewBtn.addEventListener('click', function() {
            buttons.style.display = 'none';
            reviewForm.style.display = 'flex';
        });
    }
    
    // validate review form submission
    if (reviewForm) {
        reviewForm.addEventListener('submit', function(e) {
            const ratingValue = document.getElementById('review-rating-value');
            if (!ratingValue || !ratingValue.value || ratingValue.value === '') {
                e.preventDefault();
                alert('Please select a rating (1-5 stars) before submitting your review.');
                return false;
            }
        });
    }
    if (cancelCommentBtn) {
        cancelCommentBtn.addEventListener('click', function() {
            commentForm.style.display = 'none';
            buttons.style.display = 'flex';
            document.getElementById('comment-text').value = '';
        });
    }
    if (cancelReviewBtn) {
        cancelReviewBtn.addEventListener('click', function() {
            reviewForm.style.display = 'none';
            buttons.style.display = 'flex';
            document.getElementById('review-text').value = '';
            selectedRating = 0;
            const ratingField = document.getElementById('review-rating-value');
            if (ratingField) {
                ratingField.value = '';
            }
            stars.forEach(s => s.classList.remove('selected'));
        });
    }
    if (stars.length) {
        stars.forEach(function(star) {
            star.addEventListener('mouseenter', function() {
                const hoverValue = parseInt(star.dataset.value);
                stars.forEach(s => s.classList.remove('selected'));
                for (let i = 0; i < hoverValue; i++) {
                    stars[i].classList.add('selected');
                }
            });
            star.addEventListener('mouseleave', function() {
                stars.forEach(s => s.classList.remove('selected'));
                if (selectedRating > 0) {
                    for (let i = 0; i < selectedRating; i++) {
                        stars[i].classList.add('selected');
                    }
                }
            });
            star.addEventListener('click', function(e) {
                e.preventDefault();
                selectedRating = parseInt(star.dataset.value);
                stars.forEach(s => s.classList.remove('selected'));
                for (let i = 0; i < selectedRating; i++) {
                    stars[i].classList.add('selected');
                }
                // update hidden rating field
                const ratingField = document.getElementById('review-rating-value');
                if (ratingField) {
                    ratingField.value = selectedRating;
                }
            });
        });
    }


    // comments delete buttons
    const deleteBtns = document.querySelectorAll('.rom-details-comment-delete-btn');
    const deleteModal = document.getElementById('comment-delete-modal');
    const commentDeleteForm = document.getElementById('comment-delete-form');
    const deleteYes = document.querySelector('.rom-details-comment-delete-yes');
    const deleteNo = document.querySelector('.rom-details-comment-delete-no');
    let commentToDelete = null;

    deleteBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            commentToDelete = btn.dataset.comment;
            deleteModal.style.display = 'flex';
        });
    });
    if (deleteNo) {
        deleteNo.addEventListener('click', function() {
            deleteModal.style.display = 'none';
            commentToDelete = null;
        });
    }
    if (deleteYes && commentDeleteForm) {
        deleteYes.addEventListener('click', function() {
            if (commentToDelete) {
                commentDeleteForm.action = '/roms/comment/delete/' + commentToDelete + '/';
                commentDeleteForm.submit();
            }
            deleteModal.style.display = 'none';
            commentToDelete = null;
        });
    }

    // comments edit buttons-inline editing
    const editBtns = document.querySelectorAll('.rom-details-comment-edit-btn');
    editBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const commentId = btn.dataset.comment;
            const commentDiv = document.querySelector(`.rom-details-comment[data-comment-id="${commentId}"]`);

            if (commentDiv) {
                const commentText = commentDiv.querySelector('.rom-details-comment-text');
                const editForm = commentDiv.querySelector('.rom-details-comment-edit-form');
                const actions = commentDiv.querySelector('.rom-details-comment-actions');

                // Hide text and actions, show form
                commentText.style.display = 'none';
                if (actions) actions.style.display = 'none';
                editForm.style.display = 'block';
            }
        });
    });

    // cancel edit buttons handler
    const cancelEditBtns = document.querySelectorAll('.rom-details-cancel-edit-btn');
    cancelEditBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const commentDiv = btn.closest('.rom-details-comment');

            if (commentDiv) {
                const commentText = commentDiv.querySelector('.rom-details-comment-text');
                const editForm = commentDiv.querySelector('.rom-details-comment-edit-form');
                const actions = commentDiv.querySelector('.rom-details-comment-actions');

                // show text and actions, hide form
                commentText.style.display = 'inline';
                if (actions) actions.style.display = 'flex';
                editForm.style.display = 'none';

                // reset textarea to original text
                const textarea = editForm.querySelector('.rom-details-comment-edit-textarea');
                const originalText = commentText.textContent;
                if (textarea) textarea.value = originalText;
            }
        });
    });

    // reviews delete buttons
    const reviewDeleteBtns = document.querySelectorAll('.rom-details-review-delete-btn');
    const reviewDeleteModal = document.getElementById('review-delete-modal');
    const reviewDeleteForm = document.getElementById('review-delete-form');
    const reviewDeleteYes = document.querySelector('.rom-details-review-delete-yes');
    const reviewDeleteNo = document.querySelector('.rom-details-review-delete-no');
    let reviewToDelete = null;

    reviewDeleteBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            reviewToDelete = btn.dataset.review;
            reviewDeleteModal.style.display = 'flex';
        });
    });
    if (reviewDeleteNo) {
        reviewDeleteNo.addEventListener('click', function() {
            reviewDeleteModal.style.display = 'none';
            reviewToDelete = null;
        });
    }
    if (reviewDeleteYes && reviewDeleteForm) {
        reviewDeleteYes.addEventListener('click', function() {
            if (reviewToDelete) {
                reviewDeleteForm.action = '/roms/review/delete/' + reviewToDelete + '/';
                reviewDeleteForm.submit();
            }
            reviewDeleteModal.style.display = 'none';
            reviewToDelete = null;
        });
    }

    // reviews edit buttons - inline editing
    const reviewEditBtns = document.querySelectorAll('.rom-details-review-edit-btn');
    reviewEditBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const reviewId = btn.dataset.review;
            const reviewDiv = document.querySelector(`.rom-details-review[data-review-id="${reviewId}"]`);

            if (reviewDiv) {
                const reviewText = reviewDiv.querySelector('.rom-details-review-text');
                const reviewAuthor = reviewDiv.querySelector('.rom-details-review-author');
                const reviewRatingDisplay = reviewDiv.querySelector('.rom-details-rating');
                const reviewStarDisplay = reviewDiv.querySelector('.rom-details-rating-star');
                const editForm = reviewDiv.querySelector('.rom-details-review-edit-form');
                const actions = reviewDiv.querySelector('.rom-details-review-actions');

                // stars for current rating
                const currentRating = parseInt(reviewDiv.querySelector('.review-rating-input').value);
                const editStars = editForm.querySelectorAll('.star');
                for (let i = 0; i < currentRating; i++) {
                    editStars[i].classList.add('selected');
                }

                // gide text and actions, show form
                reviewText.style.display = 'none';
                reviewAuthor.style.display = 'none';
                if (reviewRatingDisplay) reviewRatingDisplay.style.display = 'none';
                if (reviewStarDisplay) reviewStarDisplay.style.display = 'none';
                if (actions) actions.style.display = 'none';
                editForm.style.display = 'block';
            }
        });
    });

    // handle edit stars click for inline edit
    document.querySelectorAll('.rom-details-rating-stars-edit').forEach(starsContainer => {
        const editStars = starsContainer.querySelectorAll('.star');
        let editSelectedRating = 0;

        editStars.forEach(star => {
            star.addEventListener('click', function() {
                editSelectedRating = parseInt(star.dataset.value);
                editStars.forEach(s => s.classList.remove('selected'));
                for (let i = 0; i < editSelectedRating; i++) {
                    editStars[i].classList.add('selected');
                }
                // Update hidden rating field in the form
                const form = star.closest('.rom-details-review-edit-form');
                const ratingInput = form.querySelector('.review-rating-input');
                if (ratingInput) {
                    ratingInput.value = editSelectedRating;
                }
            });
        });
    });

    // cancel review edit buttons handler
    const cancelReviewEditBtns = document.querySelectorAll('.rom-details-cancel-review-edit-btn');
    cancelReviewEditBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const reviewDiv = btn.closest('.rom-details-review');

            if (reviewDiv) {
                const reviewText = reviewDiv.querySelector('.rom-details-review-text');
                const reviewAuthor = reviewDiv.querySelector('.rom-details-review-author');
                const reviewRatingDisplay = reviewDiv.querySelector('.rom-details-rating');
                const reviewStarDisplay = reviewDiv.querySelector('.rom-details-rating-star');
                const editForm = reviewDiv.querySelector('.rom-details-review-edit-form');
                const actions = reviewDiv.querySelector('.rom-details-review-actions');

                // show text and actions, hide form
                reviewText.style.display = 'block';
                reviewAuthor.style.display = 'inline';
                if (reviewRatingDisplay) reviewRatingDisplay.style.display = 'inline';
                if (reviewStarDisplay) reviewStarDisplay.style.display = 'inline';
                if (actions) actions.style.display = 'flex';
                editForm.style.display = 'none';

                // reset textarea and stars to original
                const textarea = editForm.querySelector('.rom-details-review-edit-textarea');
                const originalText = reviewText.textContent;
                if (textarea) textarea.value = originalText;

                const editStars = editForm.querySelectorAll('.star');
                editStars.forEach(s => s.classList.remove('selected'));
            }
        });
    });

    // ROM delete button
    const romDeleteBtn = document.getElementById('rom-delete-btn');
    const romDeleteModal = document.getElementById('rom-delete-modal');
    const romDeleteForm = document.getElementById('rom-delete-form');
    const romDeleteYes = romDeleteModal ? romDeleteModal.querySelector('.rom-details-review-delete-yes') : null;
    const romDeleteNo = romDeleteModal ? romDeleteModal.querySelector('.rom-details-review-delete-no') : null;

    if (romDeleteBtn && romDeleteModal) {
        romDeleteBtn.addEventListener('click', function(e) {
            e.preventDefault();
            romDeleteModal.style.display = 'flex';
        });
    }
    if (romDeleteNo) {
        romDeleteNo.addEventListener('click', function() {
            romDeleteModal.style.display = 'none';
        });
    }
    if (romDeleteYes && romDeleteForm) {
        romDeleteYes.addEventListener('click', function() {
            romDeleteModal.style.display = 'none';
            romDeleteForm.submit();
        });
    }

    // screenshot modal logic
    const modal = document.getElementById('rom-details-screenshot-modal');
    const modalImg = document.getElementById('rom-details-screenshot-modal-img');
    const modalGame = document.querySelector('.rom-details-screenshot-modal-game');
    const modalPlatform = document.querySelector('.rom-details-screenshot-modal-platform');
    const modalUploader = document.querySelector('.rom-details-screenshot-modal-uploader');
    const modalClose = document.querySelector('.rom-details-screenshot-modal-close');
    const modalAdd = document.querySelector('.rom-details-screenshot-modal-add');
    const modalRemove = document.querySelector('.rom-details-screenshot-modal-remove');
    const modalDownload = document.querySelector('.rom-details-screenshot-modal-download');
    let currentScreenshotId = null;

    document.querySelectorAll('.rom-details-screenshot').forEach(function(link) {
        if (link.classList.contains('rom-details-screenshot-more')) return;
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const img = link.querySelector('img');
            currentScreenshotId = link.dataset.screenshotId;
            const uploaderId = link.dataset.uploaderId;

            modalImg.src = img.src;
            modalImg.alt = img.alt;
            modalGame.textContent = 'Game: ' + (link.dataset.game || 'Unknown');
            modalPlatform.textContent = 'Platform: ' + (link.dataset.platform || 'Unknown');
            modalUploader.textContent = 'Uploaded by: ' + (link.dataset.uploader || 'Unknown');

            if (!window.currentUserId) {
                modalAdd.style.display = 'none';
                modalRemove.style.display = 'none';
            } else if (uploaderId && parseInt(uploaderId) === parseInt(window.currentUserId)) {
                modalAdd.style.display = 'none';
                modalRemove.style.display = 'none';
            } else if (currentScreenshotId) {
                fetch(`/accounts/screenshots/check-favorite/${currentScreenshotId}/`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.is_favorited) {
                            modalAdd.style.display = 'none';
                            modalRemove.style.display = 'inline-block';
                        } else {
                            modalAdd.style.display = 'inline-block';
                            modalRemove.style.display = 'none';
                        }
                    })
                    .catch(error => {
                        console.error('Error checking favorite status:', error);
                        modalAdd.style.display = 'none';
                        modalRemove.style.display = 'none';
                    });
            }

            modal.style.display = 'flex';
        });
    });

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

    if (modalAdd) {
        modalAdd.addEventListener('click', function() {
            if (!currentScreenshotId) return;

            fetch(`/accounts/screenshots/favorite/${currentScreenshotId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    modalAdd.style.display = 'none';
                    modalRemove.style.display = 'inline-block';
                }
            });
        });
    }

    if (modalRemove) {
        modalRemove.addEventListener('click', function() {
            if (!currentScreenshotId) return;

            fetch(`/accounts/screenshots/favorite/${currentScreenshotId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    modalRemove.style.display = 'none';
                    modalAdd.style.display = 'inline-block';
                }
            });
        });
    }

    if (modalDownload) {
        modalDownload.addEventListener('click', function() {
            if (currentScreenshotId && modalImg.src) {
                window.open(modalImg.src, '_blank');
            }
        });
    }

    const reviewLikeBtns = document.querySelectorAll('.rom-details-review-favorite-btn');
    reviewLikeBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const reviewId = this.dataset.reviewId;
            const heartIcon = this.querySelector('.rom-details-review-heart-icon');
            const countSpan = this.querySelector('.rom-details-review-favorite-count');

            fetch(`/roms/review/like/${reviewId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    countSpan.textContent = data.likes_count;
                    if (data.is_liked) {
                        heartIcon.src = heartIcon.src.replace('heart_empty.png', 'heart_full.png');
                        heartIcon.alt = 'Unlike';
                    } else {
                        heartIcon.src = heartIcon.src.replace('heart_full.png', 'heart_empty.png');
                        heartIcon.alt = 'Like';
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
