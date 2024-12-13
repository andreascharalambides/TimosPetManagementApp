// Initialize Firebase
const firebaseConfig = {
    // Your Firebase config here
    apiKey: "YOUR_API_KEY",
    authDomain: "YOUR_AUTH_DOMAIN",
    projectId: "YOUR_PROJECT_ID",
    storageBucket: "YOUR_STORAGE_BUCKET",
    messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
    appId: "YOUR_APP_ID",
    measurementId: "YOUR_MEASUREMENT_ID"
};
firebase.initializeApp(firebaseConfig);

// Add event listener when the DOM content is fully loaded
document.addEventListener('DOMContentLoaded', () => {
    setupNotificationButton();
});

function setupNotificationButton() {
    fetchSvg(notificationUrl, document.getElementById("notification-button"))?.addEventListener("click",
        () => grantNotificationPermissions());
}

function grantNotificationPermissions() {
    if ('serviceWorker' in navigator && 'PushManager' in window) {
        navigator.serviceWorker.register(firebaseMessagingUrl)
            .then(function (registration) {
                console.log('Service Worker registered:', registration);
            })
            .catch(function (err) {
                console.error('Service Worker registration failed:', err);
            });

        // Request permission for notifications
        Notification.requestPermission().then(permission => {
            if (permission === "granted") {
                const messaging = firebase.messaging();
                messaging.getToken({vapidKey: "YOUR_VAPID_KEY"}).then((currentToken) => {
                    if (currentToken) {
                        // Send the token to your server
                        console.log('Device Token:', currentToken);
                        fetch('/save-token/', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({token: currentToken})
                        });
                    } else {
                        console.log('No registration token available.');
                    }
                }).catch((err) => {
                    console.error('Error retrieving token:', err);
                });
            }
        });
    }
}