document.addEventListener('DOMContentLoaded', () => {
    setupBackButton();
});

function setupBackButton() {
    const backButton = document.getElementById("back-button");
    if (!backButton) return;

    fetch(backArrowUrl)
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.text();
        })
        .then(svgContent => backButton.innerHTML = svgContent)
        .catch(error => console.error('Error fetching the SVG:', error));

    backButton.addEventListener("click", () => window.history.back());
}