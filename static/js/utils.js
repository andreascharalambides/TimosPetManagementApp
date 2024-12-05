function fetchSvg(path, parent) {
    if (!parent) return;

    fetch(path)
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.text();
        })
        .then(svgContent => parent.innerHTML = svgContent)
        .catch(error => console.error('Error fetching the SVG:', error));

    return parent;
}

function parseFrequently(str) {
    const parser = new DOMParser();
    const decodedString = parser.parseFromString(str, 'text/html').documentElement.textContent;

    return decodedString
        .replace(/[\[\]']/g, "")
        .split(", ")
        .map(item => item.trim())
        .filter(item => item.length > 0);
}