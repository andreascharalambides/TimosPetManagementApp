document.addEventListener('DOMContentLoaded', () => {
    setupBackButton();
    setupNotificationButton();

    if (localStorage.getItem('serviceWorkerReload') === 'true') {
        localStorage.removeItem('serviceWorkerReload');
        enableFullNotificationSetup();
    }
});

function setupBackButton() {
    fetchSvg(backArrowUrl, document.getElementById("back-button"))?.addEventListener("click", () => {
        window.history.back();
    });
}

function setupNotificationButton() {
    fetchSvg(notificationUrl, document.getElementById("notification-button"))?.addEventListener("click", () => {
        enableNotifications();
    });
}

async function enableNotifications() {
    try {
        const registrations = await navigator.serviceWorker.getRegistrations();
        for (let registration of registrations) {
            await registration.unregister();
            console.log('Unregistered existing service worker');
        }

        // Register the Service Worker
        await navigator.serviceWorker.register('/users/service-worker');

        // Wait for activation with more detailed tracking
        if (!navigator.serviceWorker.controller) {
            localStorage.setItem('serviceWorkerReload', 'true');
            window.location.reload();
        } else enableFullNotificationSetup();

    } catch (error) {
        console.error('Error enabling notifications:', error);
    }
}

async function enableFullNotificationSetup() {
    try {
        // Request notification permissions
        // Directly get the registration instead of using .ready
        const registrations = await navigator.serviceWorker.getRegistrations();
        const registration = registrations[0];

        if (!registration) {
            console.error('No service worker registration found');
            return;
        }

        console.log('Service worker registration:', registration);

        // VAPID public key for push notifications
        const vapidPublicKey = "BHZew5RS_iHtJQhNfa9ALccaWy76vbAzkDSo6gQ8PtP5bJjYOr8RuWXjE0mk-Qj-O5EuE7Kur9-dj_HkKGjxMas";
        const convertedKey = urlBase64ToUint8Array(vapidPublicKey);

        // Subscribe to push notifications
        const subscription = await registration.pushManager.subscribe({
            userVisibleOnly: true,
            applicationServerKey: convertedKey,
        });

        console.log('Push Subscription:', subscription);

        // Send the subscription to the backend to save it
        await fetch('/users/save_subscription/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken(),
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(subscription.toJSON()), // Send subscription as JSON
        });

        console.log('Push subscription saved successfully.');
    } catch (error) {
        console.error('Error enabling notifications:', error);
    }
}

function getCSRFToken() {
    const match = document.cookie.match(/csrftoken=([^;]+)/);
    if (!match) {
        console.error('CSRF token not found.');
        return null;
    }
    return match[1];
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
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({action, ...extraData}),
    });
}
