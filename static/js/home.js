document.addEventListener("DOMContentLoaded", () => {
    setupAddPet();

    const date = selectedDay ? new Date(selectedDay) : new Date();
    setupEvents(date);
    updateDateDisplay(date);

    const enableNotificationsBtn = document.getElementById('enable-notifications');
    enableNotificationsBtn.addEventListener('click', async () => {
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
    });
});

function setupAddPet() {
    fetchSvg(addIconUrl, document.getElementById("add-pet-button"));
}

function updateDateDisplay(date) {
    const selectedDateElement = document.getElementById("selected-date");

    const today = new Date();
    const tomorrow = new Date(today);
    const yesterday = new Date(today);

    tomorrow.setDate(today.getDate() + 1);
    yesterday.setDate(today.getDate() - 1);

    console.log(date);
    if (date.toDateString() === today.toDateString()) {
        selectedDateElement.textContent = "Today";
    } else if (date.toDateString() === tomorrow.toDateString()) {
        selectedDateElement.textContent = "Tomorrow";
    } else if (date.toDateString() === yesterday.toDateString()) {
        selectedDateElement.textContent = "Yesterday";
    } else {
        selectedDateElement.textContent = date.toLocaleDateString(undefined, {
            year: "numeric",
            month: "long",
            day: "numeric",
        });
    }

    const formattedDate = date.toISOString().split("T")[0];
    const currentDayParam = new URL(window.location.href).searchParams.get("day");
    if (currentDayParam !== formattedDate) history.pushState(null, "", `?day=${formattedDate}`);

    fetchAndUpdateTasks(date);
}

function setupEvents(date) {
    document.getElementById("prev-day-button").addEventListener("click", () => {
        date.setDate(date.getDate() - 1);
        updateDateDisplay(date);
    });

    document.getElementById("next-day-button").addEventListener("click", () => {
        date.setDate(date.getDate() + 1);
        updateDateDisplay(date);
    });
}

async function fetchAndUpdateTasks(date) {
    const formattedDate = date.toISOString().split("T")[0];
    const taskListElement = document.querySelector(".task-list");

    try {
        const response = await fetch(`/api/fetch-tasks/?day=${formattedDate}`);
        if (!response.ok) {
            throw new Error("Failed to fetch tasks");
        }

        const data = await response.json();
        const dateNavigation = document.getElementById("date-navigation");
        taskListElement.innerHTML = "";
        taskListElement.appendChild(dateNavigation);

        if (data.tasks && data.tasks.length > 0) {
            data.tasks.forEach(task => {
                const taskItem = document.createElement("li");
                const taskLink = document.createElement("a");
                taskLink.href = `/tasks/update/${task.id}`;

                const taskTitle = document.createElement("h4");
                taskTitle.textContent = `${task.category} for ${task.pet} at ${task.start_time}`;
                taskLink.appendChild(taskTitle);

                const days = parseFrequently(task.frequently);
                const daysElement = document.createElement("h4");

                if (days.length === 7) daysElement.textContent = "Everyday";
                else if (days.length > 0) daysElement.textContent = `Every ${days.join(", ")}`;
                else daysElement.textContent = formattedDate;
                taskLink.appendChild(daysElement);

                taskItem.appendChild(taskLink);
                taskListElement.appendChild(taskItem);
            });
        } else {
            const taskItem = document.createElement("li");
            taskItem.textContent = "You have no tasks for this day.";
            taskListElement.appendChild(taskItem);
        }
    } catch (error) {
        console.error(error);
        taskListElement.innerHTML = "<li>Failed to load tasks.</li>";
    }
}

function urlBase64ToUint8Array(base64String) {
    const padding = '='.repeat((4 - base64String.length % 4) % 4);
    const base64 = (base64String + padding)
        .replace(/-/g, '+')
        .replace(/_/g, '/');
    const rawData = window.atob(base64);
    return Uint8Array.from([...rawData].map((char) => char.charCodeAt(0)));
}

function getCSRFToken() {
    return document.cookie.match(/csrftoken=([^;]+)/)[1];
}