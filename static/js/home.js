document.addEventListener("DOMContentLoaded", () => {
    setupAddPet();

    const date = selectedDay ? new Date(selectedDay) : new Date();
    setupEvents(date);
    updateDateDisplay(date);
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
    document.getElementById("prev-day-button").addEventListener("click",  () => {
        date.setDate(date.getDate() - 1);
        updateDateDisplay(date);
    });

    document.getElementById("next-day-button").addEventListener("click",  () => {
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