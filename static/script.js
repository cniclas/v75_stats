const addFilterButton = document.getElementById("add-filter");
const filterContainer = document.getElementById("filter-container");

addFilterButton.addEventListener("click", () => {
  fetch("/add_filter")
    .then(response => response.json())
    .then(data => {
      filterContainer.innerHTML += data.html;
    });
});
