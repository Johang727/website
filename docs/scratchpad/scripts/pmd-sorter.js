function sortList(value) {
    const list = document.getElementById('hack-list');
    const rows = Array.from(list.getElementsByClassName('hack-row'));

    rows.sort((a, b) => {
        if (value.startsWith('score')) {
            const scoreA = parseInt(a.getAttribute('data-score')) || 0;
            const scoreB = parseInt(b.getAttribute('data-score')) || 0;
            return value.endsWith('desc') ? scoreB - scoreA : scoreA - scoreB;
        } 
        else if (value.startsWith('date')) {
            const dateA = new Date(a.getAttribute('data-date'));
            const dateB = new Date(b.getAttribute('data-date'));
            return value.endsWith('desc') ? dateB - dateA : dateA - dateB;
        } 
        else if (value.startsWith('name')) {
            const nameA = a.getAttribute('data-name').toLowerCase();
            const nameB = b.getAttribute('data-name').toLowerCase();
            return nameA.localeCompare(nameB);
        }
    });

    // Re-append rows in the new sorted order
    rows.forEach(row => list.appendChild(row));
}

// Listen for user changes on the selector
document.getElementById('sort-select').addEventListener('change', function() {
sortList(this.value);
});

// Trigger default sort automatically on page load
document.addEventListener('DOMContentLoaded', function() {
sortList('score-desc');
});