function toggleSelection(card) {
    // Toggle the selection state
    const checkbox = card.querySelector('.book-checkbox');
    checkbox.value = checkbox.value === 'true' ? 'false' : 'true';
    
    // Add or remove styles based on the selection state
    if (checkbox.value === 'true') {
        card.classList.add('border-indigo-500'); // Add border when selected
    } else {
        card.classList.remove('border-indigo-500'); // Remove border when deselected
    }
}
