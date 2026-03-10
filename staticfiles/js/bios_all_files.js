function toggleDetails(card) {
  let details = card.querySelector('.bios-details');
  if (details.style.display === 'none') {
    details.style.display = 'block';
  } else {
    details.style.display = 'none';
  }
}

