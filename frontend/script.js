const isLocal = ["localhost", "127.0.0.1"].includes(window.location.hostname);
const API = window.PATHPILOT_API || (isLocal ? "http://127.0.0.1:8001" : "");

const weekdays = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
];

let currentPlanId = null;


// =====================================
// PAGE LOAD
// =====================================

document.addEventListener("DOMContentLoaded", () => {

    console.log("🚀 PathPilot script loaded!");

    createDayButtons();

    if (localStorage.getItem("pathpilotReminders") === "enabled") {
        document.getElementById("reminderBtn")?.classList.add("enabled");
    }

    const savedPlanId = localStorage.getItem("pathpilotPlanId");

    if (savedPlanId) {
        currentPlanId = Number(savedPlanId);
        restoreSavedPlan();
    }

    const reminderButton = document.getElementById("reminderBtn");
    if (reminderButton) {
        reminderButton.addEventListener("click", enableReminders);
    }

    const form = document.getElementById("planForm");
    const newPlanBtn = document.getElementById("newPlan");

    // =====================================
    // GENERATE ROADMAP
    // =====================================

    if (form) {

        form.addEventListener("submit", async (event) => {

            event.preventDefault();
            event.stopPropagation();

            console.log("🔥 SUBMIT EVENT FIRED");

            const goal =
                document.getElementById("goal").value.trim();

            const level =
                document.getElementById("level").value;

            const days =
                Number(document.getElementById("days").value);

            const dailyMinutes =
                Number(document.getElementById("minutes").value);

            const startTime =
                document.getElementById("startTime").value;


            // =====================================
            // STUDY DAYS
            // =====================================

            const studyDays =
                Array.from(
                    document.querySelectorAll(
                        'input[name="studyDays"]:checked'
                    )
                ).map(
                    checkbox => checkbox.value
                );


            // =====================================
            // KNOWN SKILLS
            // =====================================

            const knownSkills =
                document.getElementById("knownSkills")
                    .value
                    .split(",")
                    .map(skill => skill.trim())
                    .filter(Boolean);


            // =====================================
            // VALIDATION
            // =====================================

            if (!goal) {

                showToast("⚠️ Please enter your goal");

                return;
            }

            if (!studyDays.length) {

                showToast(
                    "⚠️ Select at least one study day"
                );

                return;
            }


            // =====================================
            // BUTTON LOADING
            // =====================================

            const button =
                document.getElementById("generateBtn");

            button.disabled = true;
            button.innerText = "⏳ Generating...";


            try {

                console.log("📡 Sending request to backend...");


                // =====================================
                // API REQUEST
                // =====================================

                const response =
                    await fetch(
                        `${API}/api/plans`,
                        {
                            method: "POST",

                            headers: {
                                "Content-Type": "application/json"
                            },

                            body: JSON.stringify({

                                goal: goal,

                                level: level,

                                days: days,

                                daily_minutes:
                                    dailyMinutes,

                                start_time:
                                    startTime,

                                study_days:
                                    studyDays,

                                known_skills:
                                    knownSkills
                            })
                        }
                    );


                if (!response.ok) {

                    throw new Error(
                        `HTTP ${response.status}`
                    );
                }


                const result =
                    await response.json();


                console.log(
                    "✅ Roadmap generated:",
                    result
                );


                // =====================================
                // SAVE PLAN ID
                // =====================================

                currentPlanId =
                    result.plan_id;

                localStorage.setItem(
                    "pathpilotPlanId",
                    currentPlanId
                );


                // =====================================
                // SHOW DASHBOARD
                // =====================================

                showDashboard(
                    result.tasks,
                    goal
                );


                showToast(
                    "🎉 Roadmap generated successfully!"
                );


            } catch (error) {

                console.error(
                    "❌ Generate error:",
                    error
                );

                showToast(
                    "❌ Could not generate roadmap"
                );


            } finally {

                button.disabled = false;

                button.innerText =
                    "✨ Generate My Roadmap";
            }

        });
    }


    // =====================================
    // NEW PLAN
    // =====================================

    if (newPlanBtn) {

        newPlanBtn.addEventListener(
            "click",
            (event) => {

                event.preventDefault();
                event.stopPropagation();

                const dashboard =
                    document.getElementById(
                        "dashboard"
                    );

                const setupCard =
                    document.getElementById(
                        "setupCard"
                    );


                dashboard.classList.add("hidden");

                setupCard.classList.remove("hidden");

                dashboard.style.display = "";

                currentPlanId = null;

                localStorage.removeItem(
                    "pathpilotPlanId"
                );


                showToast(
                    "✨ Ready for a new plan!"
                );
            }
        );
    }

});


// =====================================
// CREATE STUDY DAY BUTTONS
// =====================================

function createDayButtons() {

    const container =
        document.getElementById(
            "dayButtons"
        );

    if (!container) return;

    container.innerHTML = "";


    weekdays.forEach(day => {

        const label =
            document.createElement("label");

        label.className =
            "day";


        const checkbox =
            document.createElement("input");

        checkbox.type = "checkbox";

        checkbox.name = "studyDays";

        checkbox.value = day;


        // Monday - Saturday selected
        if (day !== "Sunday") {
            checkbox.checked = true;
        }


        const text =
            document.createElement("span");

        text.textContent =
            day.slice(0, 3);


        label.appendChild(checkbox);

        label.appendChild(text);

        container.appendChild(label);
    });
}


// =====================================
// SHOW DASHBOARD
// =====================================

function showDashboard(tasks, goal) {

    console.log("📊 SHOW DASHBOARD");

    const setupCard =
        document.getElementById(
            "setupCard"
        );

    const dashboard =
        document.getElementById(
            "dashboard"
        );


    if (!setupCard || !dashboard) {

        console.error(
            "❌ Dashboard elements not found"
        );

        return;
    }


    // Hide setup
    setupCard.classList.add("hidden");


    // Show dashboard
    dashboard.classList.remove("hidden");


    // Clear any inline display issue
    dashboard.style.display = "";


    // Goal title
    const goalTitle =
        document.getElementById(
            "goalTitle"
        );

    if (goalTitle) {
        goalTitle.textContent = goal;
    }


    // Render missions
    renderTasks(tasks);

    renderCalendar(tasks);
    loadAnalytics();


    // Update statistics
    updateStats(tasks);


    // Update streak
    updateStreak();


    console.log(
        "✅ Dashboard is now visible"
    );
}


// =====================================
// RENDER TASKS
// =====================================

function renderTasks(tasks) {

    const container =
        document.getElementById(
            "taskList"
        );

    if (!container) return;

    container.innerHTML = "";


    if (!tasks || tasks.length === 0) {

        container.innerHTML = `
            <div class="empty-state">
                🎯 No missions found.
            </div>
        `;

        return;
    }


    tasks.forEach(task => {

        const card =
            document.createElement("div");

        card.className =
            "task";


        if (task.completed) {

            card.classList.add(
                "done"
            );
        }


        card.innerHTML = `

            <div class="taskInfo">

                <div class="task-day">
                    Day ${task.day_number}
                </div>

                <h3 class="title">
                    ${task.title}
                </h3>

                <p class="time">
                    📅 ${task.date}
                </p>

                <p class="time">
                    ⏰ ${task.start_time}
                    -
                    ${task.end_time}
                </p>

            </div>


            <div class="task-action">

                ${
                    task.completed

                    ? `
                        <button
                            class="check undo-btn"
                            data-id="${task.id}"
                            type="button"
                        >
                            ↩ Undo
                        </button>
                    `

                    : `
                        <button
                            class="check complete-btn"
                            data-id="${task.id}"
                            type="button"
                        >
                            ✓ Complete
                        </button>
                    `
                }

            </div>
        `;


        container.appendChild(card);
    });


    // =====================================
    // COMPLETE BUTTONS
    // =====================================

    document
        .querySelectorAll(".complete-btn")
        .forEach(button => {

            button.addEventListener(
                "click",
                () => {

                    completeTask(
                        button.dataset.id
                    );

                }
            );

        });


    // =====================================
    // UNDO BUTTONS
    // =====================================

    document
        .querySelectorAll(".undo-btn")
        .forEach(button => {

            button.addEventListener(
                "click",
                () => {

                    undoTask(
                        button.dataset.id
                    );

                }
            );

        });
}


// =====================================
// COMPLETE TASK
// =====================================

async function completeTask(taskId) {

    if (!taskId) {

        showToast(
            "❌ Task ID missing"
        );

        return;
    }


    try {

        const response =
            await fetch(
                `${API}/api/tasks/${taskId}/complete`,
                {
                    method: "PATCH"
                }
            );


        if (!response.ok) {

            throw new Error(
                `HTTP ${response.status}`
            );
        }


        const result =
            await response.json();


        console.log(
            "Complete:",
            result
        );


        if (!result.success) {

            throw new Error(
                "Task not found"
            );
        }


        showToast(
            "✅ Mission completed!"
        );


        await reloadPlan();


    } catch (error) {

        console.error(
            "❌ Complete error:",
            error
        );

        showToast(
            "❌ Could not update task"
        );
    }
}


// =====================================
// UNDO TASK
// =====================================

async function undoTask(taskId) {

    if (!taskId) {

        showToast(
            "❌ Task ID missing"
        );

        return;
    }


    try {

        const response =
            await fetch(
                `${API}/api/tasks/${taskId}/undo`,
                {
                    method: "PATCH"
                }
            );


        if (!response.ok) {

            throw new Error(
                `HTTP ${response.status}`
            );
        }


        const result =
            await response.json();


        console.log(
            "Undo:",
            result
        );


        if (!result.success) {

            throw new Error(
                "Task not found"
            );
        }


        showToast(
            "↩ Mission undone"
        );


        await reloadPlan();


    } catch (error) {

        console.error(
            "❌ Undo error:",
            error
        );

        showToast(
            "❌ Could not update task"
        );
    }
}


// =====================================
// RELOAD PLAN
// =====================================

async function reloadPlan() {

    if (!currentPlanId) return;


    try {

        const response =
            await fetch(
                `${API}/api/plans/${currentPlanId}`
            );


        if (!response.ok) {

            throw new Error(
                `HTTP ${response.status}`
            );
        }


        const result =
            await response.json();


        renderTasks(
            result.tasks
        );


        updateStats(
            result.tasks
        );


        updateStreak();
        renderCalendar(result.tasks);
        loadAnalytics();


    } catch (error) {

        console.error(
            "❌ Reload error:",
            error
        );
    }
}


// =====================================
// UPDATE STATS
// =====================================

function updateStats(tasks) {

    if (!tasks) return;


    const total =
        tasks.length;


    const completed =
        tasks.filter(
            task => task.completed
        ).length;


    const percentage =
        total
            ? Math.round(
                completed / total * 100
            )
            : 0;


    const totalElement =
        document.getElementById(
            "totalTasks"
        );

    const doneElement =
        document.getElementById(
            "doneTasks"
        );

    const progressElement =
        document.getElementById(
            "progress"
        );

    const progressText =
        document.getElementById(
            "progressText"
        );

    const barFill =
        document.getElementById(
            "barFill"
        );


    if (totalElement)
        totalElement.textContent =
            total;

    if (doneElement)
        doneElement.textContent =
            completed;

    if (progressElement)
        progressElement.textContent =
            `${percentage}%`;

    if (progressText)
        progressText.textContent =
            `${percentage}%`;

    if (barFill)
        barFill.style.width =
            `${percentage}%`;

    updateAchievements();
}


// =====================================
// STREAK
// =====================================

async function updateStreak() {

    if (!currentPlanId) return;


    try {

        const response =
            await fetch(
                `${API}/api/plans/${currentPlanId}/stats`
            );


        if (!response.ok) {

            throw new Error(
                `HTTP ${response.status}`
            );
        }


        const stats =
            await response.json();


        console.log(
            "🔥 Stats:",
            stats
        );


        const streakElement =
            document.getElementById(
                "streak"
            );


        if (streakElement) {

            streakElement.textContent =
                `🔥 ${stats.streak}`;
        }


        const totalElement =
            document.getElementById(
                "totalTasks"
            );

        const doneElement =
            document.getElementById(
                "doneTasks"
            );

        const progressElement =
            document.getElementById(
                "progress"
            );

        const progressText =
            document.getElementById(
                "progressText"
            );

        const barFill =
            document.getElementById(
                "barFill"
            );


        if (totalElement)
            totalElement.textContent =
                stats.total;

        if (doneElement)
            doneElement.textContent =
                stats.completed;

        if (progressElement)
            progressElement.textContent =
                `${stats.progress}%`;

        if (progressText)
            progressText.textContent =
                `${stats.progress}%`;

        if (barFill)
            barFill.style.width =
                `${stats.progress}%`;


    } catch (error) {

        console.error(
            "❌ Stats error:",
            error
        );
    }
}


// =====================================
// TOAST
// =====================================

function showToast(message) {

    const toast =
        document.getElementById(
            "toast"
        );


    if (!toast) return;


    toast.textContent =
        message;


    toast.classList.add(
        "show"
    );


    setTimeout(
        () => {

            toast.classList.remove(
                "show"
            );

        },
        2500
    );
}


// =====================================
// RESTORE SAVED PLAN
// =====================================

async function restoreSavedPlan() {

    try {

        const response = await fetch(
            `${API}/api/plans/${currentPlanId}`
        );

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const result = await response.json();

        if (result.error || !result.plan) {
            throw new Error("Saved plan not found");
        }

        showDashboard(result.tasks, result.plan.goal);

    } catch (error) {

        console.error("Restore error:", error);
        currentPlanId = null;
        localStorage.removeItem("pathpilotPlanId");
    }
}


function renderCalendar(tasks) {

    const calendar = document.getElementById("calendar");
    if (!calendar) return;

    const grouped = tasks.reduce((days, task) => {
        (days[task.date] ||= []).push(task);
        return days;
    }, {});

    calendar.innerHTML = Object.entries(grouped).slice(0, 7).map(([date, dayTasks]) => `
        <div class="calendarDay">
            <div class="calendarDate"><b>${new Date(`${date}T00:00:00`).toLocaleDateString(undefined, { weekday: "short" })}</b><span>${date.slice(5)}</span></div>
            <div class="calendarTasks">${dayTasks.map(task => `<span class="scheduleItem ${task.completed ? "isDone" : ""}"><i></i>${task.start_time} ${task.title}</span>`).join("")}</div>
        </div>
    `).join("");
}


async function loadAnalytics() {

    if (!currentPlanId) return;

    try {
        const response = await fetch(`${API}/api/plans/${currentPlanId}/analytics`);
        const result = await response.json();
        const analytics = document.getElementById("analytics");
        if (analytics && result.days) {
            analytics.innerHTML = result.days.map(day => {
                const height = day.total ? Math.max(10, day.completed / day.total * 100) : 6;
                return `<div class="chartDay"><div class="chartTrack"><span style="height:${height}%"></span></div><b>${day.completed}/${day.total}</b><small>${day.label}</small></div>`;
            }).join("");
        }
        updateAchievements();
    } catch (error) {
        console.error("Analytics error:", error);
    }
}


function updateAchievements() {

    const total = Number(document.getElementById("doneTasks")?.textContent || 0);
    const streak = Number(document.getElementById("streak")?.textContent.replace(/\D/g, "") || 0);
    const xp = total * 25 + streak * 10;
    const xpElement = document.getElementById("xpTotal");
    const achievements = document.getElementById("achievements");
    if (xpElement) xpElement.textContent = `${xp} XP`;
    if (achievements) {
        const badges = [
            ["🌱", "First step", total >= 1],
            ["⚡", "Five in flow", total >= 5],
            ["🔥", "On a roll", streak >= 3]
        ];
        achievements.innerHTML = badges.map(([icon, name, earned]) => `<span class="badge ${earned ? "earned" : ""}"><b>${icon}</b>${name}</span>`).join("");
    }
}


async function enableReminders() {

    if (!("Notification" in window)) {
        showToast("Notifications are not supported here");
        return;
    }

    const permission = await Notification.requestPermission();
    if (permission !== "granted") {
        showToast("Reminder permission was not granted");
        return;
    }

    localStorage.setItem("pathpilotReminders", "enabled");
    document.getElementById("reminderBtn").classList.add("enabled");
    showToast("Daily study reminders enabled");
}