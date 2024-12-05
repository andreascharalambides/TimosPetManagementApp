document.addEventListener('DOMContentLoaded', () => {
    setupBackButton();
});

function setupBackButton() {
    fetchSvg(backArrowUrl, document.getElementById("back-button"))?.addEventListener("click",
        () => window.history.back());
}