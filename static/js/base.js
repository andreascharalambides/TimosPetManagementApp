document.addEventListener('DOMContentLoaded', () => {
    setupBackButton();
});

function setupBackButton() {
    fetchSvg(backArrowUrl, document.getElementById("back-button"))?.addEventListener("click",
        () => window.history.back());
}

async function enableNotifications() {
    // Now this is triggered by a user gesture
    const permission = await Notification.requestPermission();
    if (permission !== 'granted') {
        console.log('Notification permission not granted.');
        return;
    }

    // Proceed with service worker registration and subscription
    const registration = await navigator.serviceWorker.register('static/js/service-worker.js');
    const vapidPublicKey = "BHZew5RS_iHtJQhNfa9ALccaWy76vbAzkDSo6gQ8PtP5bJjYOr8RuWXjE0mk-Qj-O5EuE7Kur9-dj_HkKGjxMas";
    const convertedKey = urlBase64ToUint8Array(vapidPublicKey);
    const swRegistration = await navigator.serviceWorker.ready;
    const subscription = await swRegistration.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: convertedKey
    });

    console.log("Subscription:", subscription);

    await fetch('/users/save_subscription/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({subscription: subscription})
    });
}

function getCSRFToken() {
    return document.cookie.match(/csrftoken=([^;]+)/)[1];
}

function urlBase64ToUint8Array(base64String) {
    const padding = '='.repeat((4 - base64String.length % 4) % 4);
    const base64 = (base64String + padding)
        .replace(/-/g, '+')
        .replace(/_/g, '/');
    const rawData = window.atob(base64);
    return Uint8Array.from([...rawData].map((char) => char.charCodeAt(0)));
}

function logUserAction(action, extraData = {}) {
    fetch('/logs/log_action/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({action: action})
    });
}