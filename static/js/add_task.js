document.addEventListener("DOMContentLoaded", () => {
    setupCategory();
    setupImportant();
});

function setupCategory() {
    const categoryField = document.getElementById("id_category");
    const newCategoryDiv = document.getElementById("new_category_div");

    if (categoryField.value !== "--new-type--") newCategoryDiv.style.display = "none";

    categoryField.addEventListener("change", () => {
        newCategoryDiv.style.display = categoryField.value === "--new-type--" ? "flex" : "none";
    });
}

function setupImportant() {
    const importantCheckbox = document.getElementById("id_important");

    importantCheckbox.parentElement.addEventListener("click", () => {
        importantCheckbox.checked = !importantCheckbox.checked;
    });
}