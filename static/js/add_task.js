document.addEventListener('DOMContentLoaded', function () {
    const categoryField = document.getElementById('id_category');
    const newCategoryField = document.getElementById('id_new_category');

    function toggleFields() {
        if (newCategoryField.value.trim() !== '') {
            categoryField.disabled = true;
        } else {
            categoryField.disabled = false;
        }
    }

    newCategoryField.addEventListener('input', toggleFields);
});
