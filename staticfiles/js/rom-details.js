document.addEventListener('DOMContentLoaded', function() {
    const writeCommentBtn = document.getElementById('write-comment-btn');
    const writeReviewBtn = document.getElementById('write-review-btn');
    const commentForm = document.getElementById('comment-form');
    const reviewForm = document.getElementById('review-form');
    const buttons = document.querySelector('.rom-details-interactive-buttons');
    const stars = document.querySelectorAll('.rom-details-rating-stars .star');
    let selectedRating = 0;

    if (writeCommentBtn) {
        writeCommentBtn.addEventListener('click', function() {
            buttons.style.display = 'none';
            commentForm.style.display = 'flex';
        });
    }
    if (writeReviewBtn) {
        writeReviewBtn.addEventListener('click', function() {
            buttons.style.display = 'none';
            reviewForm.style.display = 'flex';
        });
    }
    if (stars.length) {
        stars.forEach(function(star) {
            star.addEventListener('mouseenter', function() {
                stars.forEach(s => s.classList.remove('selected'));
                for (let i = 0; i < parseInt(star.dataset.value); i++) {
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
            star.addEventListener('click', function() {
                selectedRating = parseInt(star.dataset.value);
                stars.forEach(s => s.classList.remove('selected'));
                for (let i = 0; i < selectedRating; i++) {
                    stars[i].classList.add('selected');
                }
            });
        });
    }


    // comments buttons
    const deleteBtns = document.querySelectorAll('.rom-details-comment-delete-btn');
    const deleteModal = document.getElementById('comment-delete-modal');
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
    if (deleteYes) {
        deleteYes.addEventListener('click', function() {
            // for now just hide it... later remove comment with django
            deleteModal.style.display = 'none';
            commentToDelete = null;
        });
    }

    // reviews buttons
    const reviewDeleteBtns = document.querySelectorAll('.rom-details-review-delete-btn');
    const reviewDeleteModal = document.getElementById('review-delete-modal');
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
    if (reviewDeleteYes) {
        reviewDeleteYes.addEventListener('click', function() {
            // for now just hide it... later remove review with django
            reviewDeleteModal.style.display = 'none';
            reviewToDelete = null;
        });
    }

    // ROM delete button
    const romDeleteBtn = document.getElementById('rom-delete-btn');
    const romDeleteModal = document.getElementById('rom-delete-modal');
    const romDeleteYes = romDeleteModal.querySelector('.rom-details-review-delete-yes');
    const romDeleteNo = romDeleteModal.querySelector('.rom-details-review-delete-no');

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
    if (romDeleteYes) {
        romDeleteYes.addEventListener('click', function() {
            romDeleteModal.style.display = 'none';
            // note: add real delete logic here later
        });
    }
});
