
let allBanorState = localStorage.getItem('allBanorState') !== null ?
                    localStorage.getItem('allBanorState') === 'true' : 
                    true; 

let allMonthsState = localStorage.getItem('allMonthsState') !== null ?
                     localStorage.getItem('allMonthsState') === 'true' : 
                     true;

function alla_banor_click() {
    const locationSelectionDiv = document.querySelector('.banor-checkboxes');
    const checkboxes = locationSelectionDiv.querySelectorAll('input[type="checkbox"]');

    allBanorState = !allBanorState; 

    for (const checkbox of checkboxes) {
        checkbox.checked = allBanorState;
    }

    const toggleButton = document.getElementById('alla_banor_toggle_button');
    if (allBanorState) {
        toggleButton.textContent = "Avmarkera alla banor";
    } else {
        toggleButton.textContent = "Markera alla banor";
    }

    localStorage.setItem('allBanorState', allBanorState); 
}

function all_months_click() {
    const locationSelectionDiv = document.querySelector('.selected_months');
    const checkboxes = locationSelectionDiv.querySelectorAll('input[type="checkbox"]');

    allMonthsState = !allMonthsState;

    for (const checkbox of checkboxes) {
        checkbox.checked = allMonthsState;
    }

    const toggleButton = document.getElementById('all_months_toggle_button');
    if (allMonthsState) {
        toggleButton.textContent = "Avmarkera alla månader";
    } else {
        toggleButton.textContent = "Markera alla månader";
    }

    localStorage.setItem('allMonthsState', allMonthsState);
}

window.onload = function() {  
    // Banor Button State
    const banorButton = document.getElementById('alla_banor_toggle_button');
    if (allBanorState) {
        banorButton.textContent = "Avmarkera alla banor";
    } else {
        banorButton.textContent = "Markera alla banor";
    }

    // Month Button State
    const monthButton = document.getElementById('all_months_toggle_button');
    if (allMonthsState) {
        monthButton.textContent = "Avmarkera alla månader";
    } else {
        monthButton.textContent = "Markera alla månader";
    }
}

document.addEventListener('DOMContentLoaded', function () {
    var inputs = document.querySelectorAll('.large-number-input');

    inputs.forEach(function(input) {
        input.addEventListener('input', function(e) {
            // Save the cursor position
            let cursorPosition = this.selectionStart;

            // Get the current value, remove non-digit characters except for the decimal point
            let value = this.value.replace(/[^\d.]/g, '');

            // Split the value into whole and fractional parts
            let parts = value.split('.');
            let wholePart = parts[0];
            let fractionalPart = parts[1];

            // Format the whole part with commas
            let formattedWholePart = wholePart.replace(/\B(?=(\d{3})+(?!\d))/g, ",");

            // Reconstruct the value with the formatted whole part and original fractional part
            this.value = formattedWholePart + (fractionalPart ? '.' + fractionalPart : '');

            // Restore the cursor position, adjusted for added/removed commas
            let delta = this.value.length - value.length;
            this.setSelectionRange(cursorPosition + delta, cursorPosition + delta);
        });
    });
});

