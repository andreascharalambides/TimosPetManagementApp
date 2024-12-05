document.addEventListener("DOMContentLoaded", () => {
    setupAddPet();
})

function setupAddPet() {
    fetchSvg(addIconUrl, document.getElementById("add-pet-button"));
}