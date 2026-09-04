from datetime import datetime

from backend.main import PlanRequest, generate_tasks, get_topics


def test_unknown_goal_uses_original_roadmap():
    topics = get_topics("Quantum computing")

    names = [name for name, _ in topics]

    assert len(topics) >= 6
    assert any("Fundamentals" in name or "Foundation" in name for name in names)
    assert any("Core Concept" in name for name in names)
    assert any("Practice" in name or "Hands-on" in name for name in names)
    assert any("Project" in name or "Portfolio" in name for name in names)


def test_academic_plan_schedules_each_subject_with_end_time_duration():
    request = PlanRequest(
        goal="",
        days=1,
        daily_minutes=30,
        start_time="18:00",
        end_time="20:00",
        study_days=[datetime.now().strftime("%A")],
        plan_type="academic",
        subjects=["Mathematics", "Physics"],
        exam_days=1,
    )

    tasks = generate_tasks(request)

    assert [task["title"] for task in tasks] == [
        "Mathematics revision",
        "Physics revision",
    ]
    assert tasks[0]["start_time"] == "18:00"
    assert tasks[0]["end_time"] == "19:00"
    assert tasks[1]["start_time"] == "19:00"
    assert tasks[1]["end_time"] == "20:00"
