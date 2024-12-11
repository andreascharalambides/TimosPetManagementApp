document.addEventListener("DOMContentLoaded", () => {
    setupCategory();
    setupImportant();
});

function setupCategory() {
    const categoryField = document.getElementById("id_category");
    const newCategoryDiv = document.getElementById("new_category_div");

}

function setupImportant() {
    const importantCheckbox = document.getElementById("id_important");

    importantCheckbox.parentElement.addEventListener("click", () => {
        importantCheckbox.checked = !importantCheckbox.checked;
    });
}