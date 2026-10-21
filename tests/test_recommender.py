from services.recommender import recommend_projects


def test_beginner_only_gets_beginner_projects():
    projects = [
        {"name": "Basic", "level": "Beginner", "category": "AI / ML",
         "time": "1-2 weeks", "skills": ["Python"]},
        {"name": "Advanced", "level": "Advanced", "category": "AI / ML",
         "time": "1-2 weeks", "skills": ["Python", "ML"]}
    ]
    result = recommend_projects(
        projects, ["AI / ML"], "Beginner", "Any", ["Python"]
    )
    assert [project["name"] for project in result] == ["Basic"]


def test_skill_gaps_are_identified():
    projects = [
        {"name": "Test", "level": "Beginner", "category": "AI / ML",
         "time": "1-2 weeks", "skills": ["Python", "Pandas"]}
    ]
    result = recommend_projects(
        projects, ["AI / ML"], "Beginner", "Any", ["Python"]
    )
    assert result[0]["matched_skills"] == ["Python"]
    assert result[0]["skill_gaps"] == ["Pandas"]


def test_interest_filter_works():
    projects = [
        {"name": "Planner", "level": "Beginner",
         "category": "Productivity", "time": "1-2 weeks",
         "skills": ["Python"]}
    ]
    result = recommend_projects(
        projects, ["AI / ML"], "Beginner", "Any", ["Python"]
    )
    assert result == []
