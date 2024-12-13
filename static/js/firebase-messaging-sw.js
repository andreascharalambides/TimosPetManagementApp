importScripts('https://www.gstatic.com/firebasejs/11.1.0/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/11.1.0/firebase-messaging.js');

const firebaseConfig = {
    apiKey: "AIzaSyBnkG1JZ3BlMIY4FI5AqAmglZC0txVnMNk",
    authDomain: "timospetapp.firebaseapp.com",
    projectId: "timospetapp",
    storageBucket: "timospetapp.appspot.com",
    messagingSenderId: "650161807951",
    appId: "1:650161807951:web:00e9c2e23745329b13c03a",
    measurementId: "G-KSQT0L9VZH"
};

firebase.initializeApp(firebaseConfig);

const messaging = firebase.messaging();

messaging.onBackgroundMessage(function (payload) {
    console.log('Received background message:', payload);
    const notificationTitle = payload.notification.title;
    const notificationOptions = {
        body: payload.notification.body,
    };
    self.registration.showNotification(notificationTitle, notificationOptions);
});
