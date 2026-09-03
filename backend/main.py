from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
from datetime import datetime, timedelta
import sqlite3
import json
import os

app = FastAPI(title="PathPilot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "pathpilot.db")
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            goal TEXT,
            level TEXT,
            days INTEGER,
            daily_minutes INTEGER,
            start_time TEXT,
            study_days TEXT,
            known_skills TEXT,
            created_at TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plan_id INTEGER,
            day_number INTEGER,
            date TEXT,
            title TEXT,
            start_time TEXT,
            end_time TEXT,
            completed INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()


init_db()

app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")


class PlanRequest(BaseModel):
    goal: str
    level: str
    days: int
    daily_minutes: int
    start_time: str
    study_days: List[str]
    known_skills: List[str] = []


# =========================
# ROADMAP DATA
# =========================

ROADMAPS = {

    "data analyst": [
        ("Excel Fundamentals", 120),
        ("SQL Basics", 180),
        ("SQL Practice", 180),
        ("Statistics", 150),
        ("Python for Data Analysis", 240),
        ("Pandas & NumPy", 240),
        ("Power BI", 210),
        ("Data Visualization", 150),
        ("Portfolio Project", 300),
        ("Resume & Interview Preparation", 120)
    ],

    "data scientist": [
        ("Python Fundamentals", 180),
        ("NumPy & Pandas", 240),
        ("Statistics", 240),
        ("Data Visualization", 150),
        ("Machine Learning Basics", 300),
        ("Supervised Learning", 300),
        ("Unsupervised Learning", 240),
        ("Model Evaluation", 180),
        ("Machine Learning Project", 360)
    ],

    "software developer": [
        ("Programming Fundamentals", 180),
        ("Git & GitHub", 120),
        ("Data Structures", 300),
        ("Algorithms", 300),
        ("Object Oriented Programming", 180),
        ("SQL & Databases", 180),
        ("APIs & Backend Basics", 240),
        ("Frontend Basics", 240),
        ("Full Stack Project", 360)
    ],

    "ui/ux design": [
        ("Design Thinking & UX Principles", 180),
        ("User Research & Personas", 210),
        ("Information Architecture", 180),
        ("Wireframing", 180),
        ("UI Design Fundamentals", 240),
        ("Typography & Color Systems", 180),
        ("Figma Essentials", 240),
        ("Prototyping & User Testing", 240),
        ("Design Systems", 210),
        ("UX Case Study Portfolio", 300)
    ],

    "frontend developer": [
        ("HTML & Semantic Web", 180),
        ("CSS Layouts & Responsive Design", 240),
        ("JavaScript Fundamentals", 300),
        ("DOM & Browser APIs", 210),
        ("Git & GitHub", 120),
        ("React Fundamentals", 300),
        ("Accessibility & Performance", 180),
        ("Frontend Testing", 180),
        ("Production Portfolio Project", 300)
    ],

    "backend developer": [
        ("Programming Fundamentals", 240),
        ("Git & GitHub", 120),
        ("HTTP & REST APIs", 210),
        ("SQL & Database Design", 240),
        ("Backend Frameworks", 300),
        ("Authentication & Security", 210),
        ("Testing & Documentation", 180),
        ("Deployment & Monitoring", 210),
        ("Backend Portfolio Project", 300)
    ],

    "product manager": [
        ("Product Discovery", 180),
        ("User Research", 180),
        ("Problem Framing & Prioritization", 210),
        ("Roadmaps & Product Strategy", 210),
        ("Writing Product Requirements", 180),
        ("Agile & Scrum", 180),
        ("Product Metrics & Analytics", 210),
        ("Stakeholder Communication", 150),
        ("Product Case Study Portfolio", 240)
    ],

    "digital marketing": [
        ("Marketing Fundamentals", 180),
        ("Customer & Competitor Research", 180),
        ("Content Strategy", 210),
        ("SEO Fundamentals", 240),
        ("Social Media Marketing", 210),
        ("Email Marketing", 180),
        ("Paid Advertising", 240),
        ("Marketing Analytics", 210),
        ("Campaign Portfolio Project", 240)
    ],

    "graphic designer": [
        ("Design Principles", 180),
        ("Typography", 180),
        ("Color Theory", 180),
        ("Layout & Composition", 210),
        ("Adobe Creative Tools", 300),
        ("Brand Identity Design", 240),
        ("Print & Digital Design", 210),
        ("Client Presentation Skills", 150),
        ("Graphic Design Portfolio", 300)
    ],

    "cybersecurity analyst": [
        ("Networking Fundamentals", 240),
        ("Linux & Command Line", 210),
        ("Security Principles", 180),
        ("Threats & Vulnerability Management", 240),
        ("Security Tools & Monitoring", 240),
        ("Identity & Access Management", 180),
        ("Incident Response", 210),
        ("Security Policies & Risk", 180),
        ("Security Operations Project", 300)
    ],

    "cloud devops engineer": [
        ("Linux & Networking", 240),
        ("Git & GitHub", 120),
        ("Cloud Fundamentals", 240),
        ("Docker & Containers", 210),
        ("CI/CD Pipelines", 210),
        ("Infrastructure as Code", 240),
        ("Kubernetes Basics", 300),
        ("Monitoring & Reliability", 210),
        ("Cloud Deployment Project", 300)
    ],

    "business analyst": [
        ("Business Analysis Fundamentals", 180),
        ("Stakeholder & Requirements Elicitation", 210),
        ("Process Mapping", 180),
        ("Excel for Analysis", 210),
        ("SQL for Business Data", 240),
        ("Data Visualization", 180),
        ("Documentation & User Stories", 180),
        ("Presentation & Communication", 150),
        ("Business Case Study Portfolio", 240)
    ]
}


def get_topics(goal):

    goal = goal.lower().strip()

    aliases = {
        "ui ux": "ui/ux design",
        "ux designer": "ui/ux design",
        "ui designer": "ui/ux design",
        "frontend": "frontend developer",
        "front end": "frontend developer",
        "backend": "backend developer",
        "back end": "backend developer",
        "full stack developer": "software developer",
        "full stack": "software developer",
        "fullstack developer": "software developer",
        "pm": "product manager",
        "marketing": "digital marketing",
        "graphic design": "graphic designer",
        "cyber security": "cybersecurity analyst",
        "cybersecurity": "cybersecurity analyst",
        "devops": "cloud devops engineer",
        "cloud engineer": "cloud devops engineer",
        "business analyst": "business analyst"
    }

    for alias, career in aliases.items():
        if alias in goal:
            return ROADMAPS[career]

    for career, topics in ROADMAPS.items():

        if career in goal or goal in career:
            return topics

    return [
        ("Fundamentals", 180),
        ("Core Concepts", 240),
        ("Practice", 240),
        ("Mini Project", 300),
        ("Revision", 120)
    ]


# =========================
# TIME FUNCTIONS
# =========================

def add_minutes(time_string, minutes):

    current = datetime.strptime(
        time_string,
        "%H:%M"
    )

    new_time = current + timedelta(
        minutes=minutes
    )

    return new_time.strftime("%H:%M")


# =========================
# TASK GENERATOR
# =========================

def generate_tasks(request):

    topics = get_topics(request.goal)

    known = {
        skill.lower().strip()
        for skill in request.known_skills
    }

    topics = [
        topic
        for topic in topics
        if topic[0].lower() not in known
    ]

    sessions = []

    for topic, total_minutes in topics:

        remaining = total_minutes

        while remaining > 0:

            session_time = min(
                remaining,
                request.daily_minutes
            )

            sessions.append(
                (topic, session_time)
            )

            remaining -= session_time

    tasks = []

    today = datetime.now().date()

    session_index = 0

    for day_number in range(
        1,
        request.days + 1
    ):

        current_date = (
            today +
            timedelta(days=day_number - 1)
        )

        weekday = current_date.strftime("%A")

        if weekday not in request.study_days:
            continue

        if session_index >= len(sessions):
            break

        current_time = request.start_time

        remaining_daily_time = request.daily_minutes

        while (
            remaining_daily_time > 0
            and session_index < len(sessions)
        ):

            topic, duration = sessions[session_index]

            duration = min(
                duration,
                remaining_daily_time
            )

            end_time = add_minutes(
                current_time,
                duration
            )

            tasks.append({
                "day_number": day_number,
                "date": current_date.isoformat(),
                "title": topic,
                "start_time": current_time,
                "end_time": end_time,
                "completed": False
            })

            current_time = end_time

            remaining_daily_time -= duration

            session_index += 1

    return tasks


# =========================
# HOME
# =========================

@app.get("/")
def home():

    return {
        "message": "🚀 PathPilot API is running!"
    }


# =========================
# CREATE PLAN
# =========================

@app.post("/api/plans")
def create_plan(request: PlanRequest):

    tasks = generate_tasks(request)

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO plans
        (
            goal,
            level,
            days,
            daily_minutes,
            start_time,
            study_days,
            known_skills,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (

        request.goal,
        request.level,
        request.days,
        request.daily_minutes,
        request.start_time,
        json.dumps(request.study_days),
        json.dumps(request.known_skills),
        datetime.now().isoformat()

    ))

    plan_id = cursor.lastrowid

    for task in tasks:

        cursor.execute("""
            INSERT INTO tasks
            (
                plan_id,
                day_number,
                date,
                title,
                start_time,
                end_time,
                completed
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (

            plan_id,
            task["day_number"],
            task["date"],
            task["title"],
            task["start_time"],
            task["end_time"],
            0

        ))

        # IMPORTANT
        # Save database ID into task
        task["id"] = cursor.lastrowid

    conn.commit()

    conn.close()

    return {
        "plan_id": plan_id,
        "tasks": tasks,
        "total_tasks": len(tasks)
    }


# =========================
# GET PLAN
# =========================

@app.get("/api/plans/{plan_id}")
def get_plan(plan_id: int):

    conn = get_connection()

    conn.row_factory = sqlite3.Row

    plan = conn.execute(
        """
        SELECT *
        FROM plans
        WHERE id=?
        """,
        (plan_id,)
    ).fetchone()

    tasks = conn.execute(
        """
        SELECT *
        FROM tasks
        WHERE plan_id=?
        ORDER BY day_number, start_time
        """,
        (plan_id,)
    ).fetchall()

    conn.close()

    if not plan:

        return {
            "error": "Plan not found"
        }

    return {

        "plan": dict(plan),

        "tasks": [
            dict(task)
            for task in tasks
        ]

    }


# =========================
# COMPLETE TASK
# =========================

@app.patch("/api/tasks/{task_id}/complete")
def complete_task(task_id: int):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE tasks
        SET completed=1
        WHERE id=?
        """,
        (task_id,)
    )

    changed = cursor.rowcount

    conn.commit()

    conn.close()

    return {

        "success": changed > 0,

        "task_id": task_id,

        "completed": True

    }


# =========================
# UNDO TASK
# =========================

@app.patch("/api/tasks/{task_id}/undo")
def undo_task(task_id: int):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE tasks
        SET completed=0
        WHERE id=?
        """,
        (task_id,)
    )

    changed = cursor.rowcount

    conn.commit()

    conn.close()

    return {

        "success": changed > 0,

        "task_id": task_id,

        "completed": False

    }


# =========================
# PLAN STATISTICS
# =========================

@app.get("/api/plans/{plan_id}/stats")
def get_plan_stats(plan_id: int):

    conn = get_connection()

    plan = conn.execute(
        "SELECT study_days FROM plans WHERE id=?",
        (plan_id,)
    ).fetchone()

    tasks = conn.execute(
        """
        SELECT date, completed
        FROM tasks
        WHERE plan_id=?
        ORDER BY date
        """,
        (plan_id,)
    ).fetchall()

    conn.close()

    if not plan:
        return {"error": "Plan not found"}

    study_days = set(json.loads(plan[0] or "[]"))

    total = len(tasks)

    completed = sum(
        1
        for task in tasks
        if task[1] == 1
    )

    # =========================
    # COMPLETED DATES
    # =========================

    completed_dates = sorted({
        datetime.strptime(
            task[0],
            "%Y-%m-%d"
        ).date()

        for task in tasks

        if task[1] == 1
    })

    # Count backwards through selected study days, ignoring rest days.

    streak = 0

    if completed_dates:

        completed_set = set(completed_dates)
        current = completed_dates[-1]

        while current in completed_set:
            streak += 1
            current -= timedelta(days=1)
            while current.strftime("%A") not in study_days:
                current -= timedelta(days=1)

    # =========================
    # PROGRESS
    # =========================

    progress = 0

    if total > 0:

        progress = round(
            (completed / total) * 100
        )

    return {

        "total": total,

        "completed": completed,

        "progress": progress,

        "streak": streak,

        "study_days": list(study_days)

    }


@app.get("/api/plans/{plan_id}/analytics")
def get_plan_analytics(plan_id: int):

    conn = get_connection()

    plan = conn.execute(
        "SELECT id FROM plans WHERE id=?",
        (plan_id,)
    ).fetchone()

    tasks = conn.execute(
        "SELECT date, completed FROM tasks WHERE plan_id=? ORDER BY date",
        (plan_id,)
    ).fetchall()

    conn.close()

    if not plan:
        return {"error": "Plan not found"}

    today = datetime.now().date()
    week_start = today - timedelta(days=today.weekday())
    days = []

    for offset in range(7):
        date = week_start + timedelta(days=offset)
        day_tasks = [task for task in tasks if task[0] == date.isoformat()]
        days.append({
            "date": date.isoformat(),
            "label": date.strftime("%a"),
            "total": len(day_tasks),
            "completed": sum(task[1] == 1 for task in day_tasks)
        })

    return {
        "week_start": week_start.isoformat(),
        "days": days
    }