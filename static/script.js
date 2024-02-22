
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
