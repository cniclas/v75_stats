document.addEventListener('DOMContentLoaded', function() {
    // Add event listeners to all toggle buttons 
    const toggleButtons = document.querySelectorAll('.input-pair button'); 
    toggleButtons.forEach(button => {
        button.addEventListener('click', function() {
            const propertyName = this.id.replace('_toggle_button', '');
            const checkboxes = document.querySelectorAll(`input[name^="${propertyName}_"]`);

            const allChecked = Array.from(checkboxes).every(checkbox => checkbox.checked);

            checkboxes.forEach(checkbox => {
                checkbox.checked = !allChecked; // Toggle the checkboxes
            });
        });
    });
});
