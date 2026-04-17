document.addEventListener('DOMContentLoaded', function() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || document.querySelector('script[data-csrf]')?.dataset.csrf;

    const passButtons = document.querySelectorAll('.event-pass-btn');
    passButtons.forEach(button => {
        button.addEventListener('click', function() {
            const eventId = this.dataset.eventId;

            fetch(`/events/mark-passed/${eventId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    location.reload();
                } else {
                    alert(data.message || 'An error occurred');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Failed to update event');
            });
        });
    });

    const deleteButtons = document.querySelectorAll('.event-delete-btn');
    const deleteModal = document.getElementById('event-delete-modal');
    const deleteYesBtn = deleteModal?.querySelector('.event-delete-yes');
    const deleteNoBtn = deleteModal?.querySelector('.event-delete-no');
    let currentDeleteEventId = null;

    deleteButtons.forEach(button => {
        button.addEventListener('click', function() {
            currentDeleteEventId = this.dataset.eventId;
            deleteModal.style.display = 'flex';
        });
    });

    if (deleteNoBtn) {
        deleteNoBtn.addEventListener('click', function() {
            deleteModal.style.display = 'none';
            currentDeleteEventId = null;
        });
    }

    if (deleteYesBtn) {
        deleteYesBtn.addEventListener('click', function() {
            if (currentDeleteEventId) {
                const form = document.createElement('form');
                form.method = 'POST';
                form.action = `/events/delete/${currentDeleteEventId}/`;

                const csrfInput = document.createElement('input');
                csrfInput.type = 'hidden';
                csrfInput.name = 'csrfmiddlewaretoken';
                csrfInput.value = csrfToken;

                form.appendChild(csrfInput);
                document.body.appendChild(form);
                form.submit();
            }
        });
    }
});

