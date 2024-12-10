self.addEventListener('push', function (event) {
    if (!event.data) {
        return;
    }

    const data = event.data.json();
    const title = data.title || 'Task Reminder';
    const options = {
        body: data.body || 'You have a task starting soon!',
        icon: data.icon || '/static/images/notification_icon.png',
        badge: '/static/images/notification_badge.png'
    };

    event.waitUntil(
        self.registration.showNotification(title, options)
    );
});
