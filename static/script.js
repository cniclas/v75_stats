let allCheckBoxesState = true;
function alla_banor_click() {
    const locationSelectionDiv = document.querySelector('.banor-checkboxes');
    const checkboxes = locationSelectionDiv.querySelectorAll('input[type="checkbox"]');

    allCheckBoxesState = !allCheckBoxesState;

    // Loop through and uncheck each checkbox
    for (const checkbox of checkboxes) {
        checkbox.checked = allCheckBoxesState;
    }

    const toggleButton = document.getElementById('alla_banor_toggle_button');
    if (allCheckBoxesState){
        toggleButton.textContent = "Avmarkera alla banor";
    }
    else{
        toggleButton.textContent = "Markera alla banor";
    }
    
}

let allMonthsState = true;
function all_months_click() {
    const locationSelectionDiv = document.querySelector('.selected_months');
    const checkboxes = locationSelectionDiv.querySelectorAll('input[type="checkbox"]');

    allMonthsState = !allMonthsState;

    // Loop through and uncheck each checkbox
    for (const checkbox of checkboxes) {
        checkbox.checked = allMonthsState;
    }

    const toggleButton = document.getElementById('all_months_toggle_button');
    if (allMonthsState){
        toggleButton.textContent = "Avmarkera alla månader";
    }
    else{
        toggleButton.textContent = "Markera alla månader";
    }
    
}